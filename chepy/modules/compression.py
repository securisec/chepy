import binascii
import bz2
import gzip
import io
import lzma
import tarfile
import zipfile
import zlib
import stat
from typing import TypeVar
import lazy_import
from .internal.helpers import LZ77Compressor

LZ4 = lazy_import.lazy_module("lz4.frame")

from ..core import ChepyCore, ChepyDecorators

CompressionT = TypeVar("CompressionT", bound="Compression")


class Compression(ChepyCore):
    def __init__(self, *data):
        super().__init__(*data)

    def __tar_modes(self, mode):  # pragma: no cover
        assert mode in ["gz", "bz2", "xz", ""], "Valid modes are gz, bz2, xz"

    @ChepyDecorators.call_stack
    def fix_zip_header(self: CompressionT) -> CompressionT:
        """Fix the first 4 bytes of a zip file

        Returns:
            Chepy: The Chepy object.
        """
        data = bytearray(binascii.hexlify(self._convert_to_bytes()))
        data[0:8] = b"504b0304"
        self.state = binascii.unhexlify(data)
        return self

    @ChepyDecorators.call_stack
    def zip_info(self) -> CompressionT:
        """Gets various information about a zip file

        This includes information about all the files inside the
        archive.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("/path/to/example.zip")
            >>> c.load_file().zip_info()
            [{'CRC': 1779821815, '_compresslevel': None, '_raw_time': 19712,...}]
        """
        z = zipfile.ZipFile(self._load_as_file())
        self.state = list(
            map(
                lambda x: dict(x, encrypted=True)
                if x["flag_bits"] & 0x1
                else dict(x, encrypted=False),
                self._pickle_class(z.infolist()),
            )
        )
        z.close()
        return self

    @ChepyDecorators.call_stack
    def zip_list_files(self) -> CompressionT:
        """Get a list of files inside the zip archive

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some.zip").load_file().zip_list_files().o
            ['somefile', 'some_dir/some_file'...]
        """
        with zipfile.ZipFile(self._load_as_file()) as z:
            self.state = list(i.filename for i in z.infolist())
        return self

    @ChepyDecorators.call_stack
    def unzip_one(self, file: str, password: str = None) -> CompressionT:
        """Unzip one file from zipfile

        Use zip_list_files to get all the filenames within the zip archive

        Args:
            file (str): Required. Path of file inside the archive
            password (str, optional): Password if zip is encrypted. Defaults to None.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("/path/to/zip.zip").load_file()
            >>> c.zip_info()
            ['somefile.txt', 'some_dir/some_file'...]
            >>> c.unzip_one("somefile.txt")
            b"Hello World!"
        """
        z = zipfile.ZipFile(self._load_as_file())
        if password is not None:
            z.setpassword(password.encode())
        self.state = z.read(file)
        z.close()
        return self

    @ChepyDecorators.call_stack
    def unzip_all(self, password: str = None) -> CompressionT:
        """Unzip all files from zipfile into the state

        Args:
            password (str, optional): Password if zip is encrypted. Defaults to None.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("/path/to/zip.zip").load_file()
            >>> c.unzip_all()
            [b"Hello World!", b"haha"]
        """
        z = zipfile.ZipFile(self._load_as_file())
        if password is not None:
            z.setpassword(password.encode())
        self.state = list(z.read(f) for f in z.infolist())
        z.close()
        return self

    @ChepyDecorators.call_stack
    def create_zip_file(self, file_name: str) -> CompressionT:
        """Create a zip archive with data from state

        Args:
            file_name (str): File name for file inside zip archive

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("some data").create_zip_file()
            >>> c.write("/some/path/file.zip", as_binary=True)
        """
        mf = io.BytesIO()
        z = zipfile.ZipFile(mf, mode="w", compression=zipfile.ZIP_DEFLATED)
        z.writestr(file_name, self.state)
        z.close()
        self.state = mf.getvalue()
        return self

    @ChepyDecorators.call_stack
    def zip_compress(self, file_name: str) -> CompressionT:
        """Compress the state as a zipfile

        Args:
            filename (str): File name

        Returns:
            Chepy: The Chepy object.
        """
        out = io.BytesIO()
        zipInfo = zipfile.ZipInfo(file_name)
        with zipfile.ZipFile(out, mode="w") as z:
            z.writestr(zipInfo, self._convert_to_bytes())
        self.state = out.getvalue()
        return self

    @ChepyDecorators.call_stack
    def zip_compress_symlink(
        self: CompressionT, file_name: str, target_file: str
    ) -> CompressionT:
        """Create a zipfile with a symlink pointer. For unix

        Args:
            filename (str): File name
            target_file (str): Target system file

        Returns:
            Chepy: The Chepy object.
        """
        out = io.BytesIO()
        zipInfo = zipfile.ZipInfo(file_name)
        zipInfo.create_system = (
            3  # System which created ZIP archive, 3 = Unix; 0 = Windows
        )
        unix_st_mode = (
            stat.S_IFLNK
            | stat.S_IRUSR
            | stat.S_IWUSR
            | stat.S_IXUSR
            | stat.S_IRGRP
            | stat.S_IWGRP
            | stat.S_IXGRP
            | stat.S_IROTH
            | stat.S_IWOTH
            | stat.S_IXOTH
        )
        zipInfo.external_attr = (
            unix_st_mode << 16
        )  # The Python zipfile module accepts the 16-bit "Mode" field (that stores st_mode field from struct stat, containing user/group/other permissions, setuid/setgid and symlink info, etc) of the ASi extra block for Unix as bits 16-31 of the external_attr
        zipOut = zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED)
        zipOut.writestr(zipInfo, target_file)
        zipOut.close()
        self.state = out.getvalue()
        return self

    @ChepyDecorators.call_stack
    def tar_list_files(self, mode: str = "") -> CompressionT:
        """Get file information inside a tar archive

        Args:
            mode (str, optional): Mode to open tar file as. Defaults to "".

        Returns:
            Chepy: The Chepy object.
        """
        self.__tar_modes(mode)
        if mode:
            mode = "r:{}".format(mode)
        else:
            mode = "r"
        tar = tarfile.open(fileobj=self._load_as_file(), mode=mode)
        self.state = [t.name for t in tar.getmembers()]
        return self

    @ChepyDecorators.call_stack
    def tar_extract_one(self, filename: str, mode: str = "") -> CompressionT:
        """Extract one file from inside a tar archive

        Args:
            filename (str): Required. File name inside archive.
            mode (str, optional): Mode to open tar file as. Defaults to "".

        Returns:
            Chepy: The Chepy object.
        """
        self.__tar_modes(mode)
        if mode:
            mode = "r:{}".format(mode)
        else:
            mode = "r"
        tar = tarfile.open(fileobj=self._load_as_file(), mode=mode)
        self.state = tar.extractfile(filename).read()
        return self

    @ChepyDecorators.call_stack
    def tar_extract_all(self, mode: str = "") -> CompressionT:
        """Extract one file from inside a tar archive

        Args:
            mode (str, optional): Mode to open tar file as. Defaults to "".

        Returns:
            Chepy: The Chepy object.
        """
        self.__tar_modes(mode)
        if mode:
            mode = "r:{}".format(mode)
        else:
            mode = "r"
        tar = tarfile.open(fileobj=self._load_as_file(), mode=mode)
        self.state = {t.name: tar.extractfile(t).read() for t in tar.getmembers()}
        return self

    @ChepyDecorators.call_stack
    def tar_compress(self, filename: str, mode: str = "gz") -> CompressionT:
        """Compress the state into a tar compressed object.

        Args:
            filename (str): A file name for the tar object
            mode (str, optional): Compression mode. Defaults to "gz".

        Returns:
            Chepy: The Chepy object.
        """
        self.__tar_modes(mode)
        if mode:
            mode = "w:{}".format(mode)
        else:
            mode = "w"
        fh = io.BytesIO()
        with tarfile.open(fileobj=fh, mode=mode) as tar:
            info = tarfile.TarInfo(name=filename)
            info.size = len(self._convert_to_bytes())
            tar.addfile(info, io.BytesIO(self._convert_to_bytes()))
        self.state = fh.getvalue()
        fh.close()
        return self

    @ChepyDecorators.call_stack
    def gzip_compress(self, file_name: str = None) -> CompressionT:
        """Create a gz archive with data from state

        Args:
            file_name (str, optional): File name for file inside zip archive.
                Defaults to None.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("some data").gzip_compress()
            >>> c.write("/some/path/file.zip", as_binary=True)
        """
        mf = io.BytesIO()
        g = gzip.GzipFile(filename=file_name, mode="w", fileobj=mf)
        g.write(self._convert_to_bytes())
        g.close()
        self.state = mf.getvalue()
        return self

    @ChepyDecorators.call_stack
    def gzip_decompress(self) -> CompressionT:
        """Decompress a gzip archive

        Returns:
            Chepy: The Chepy object.
        """
        self.state = gzip.decompress(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def bzip_compress(self) -> CompressionT:
        """Compress the state into bz2 archive

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("some data").bzip_compress()
            b'BZh91AY&SY\\x9f\\xe2\\xaa\\x9d\\x00\\x00\\x03...

            We can now write this as a bz2 file with
            >>> c.write("/path/to/file.bz2", as_binary=True)
        """
        mf = io.BytesIO()
        b = bz2.BZ2File(mf, mode="w")
        b.write(self._convert_to_bytes())
        b.close()
        self.state = mf.getvalue()
        return self

    @ChepyDecorators.call_stack
    def bzip_decompress(self) -> CompressionT:
        """Decompress a bz2 archive

        Returns:
            Chepy: The Chepy object.
        """
        self.state = bz2.decompress(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def zlib_compress(self, level: int = 9) -> CompressionT:
        """Compress using zlib

        Args:
            level (int, optional): Level of compression. 0-9. Defaults to 9.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some text").zlib_compress().to_hex().o
            b"78da2bcecf4d552849ad28010011e8039a"
        """
        self.state = zlib.compress(self._convert_to_bytes(), level=level)
        return self

    @ChepyDecorators.call_stack
    def zlib_decompress(self) -> CompressionT:
        """Zlib decompression

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("789c0580a10d000008c35ee1b9ca05c104e737b761ca5711e8039a")
            >>> c.hex_to_bytes()
            >>> c.zlib_decompress()
            >>> c.out
            b"some text"
        """
        self.state = zlib.decompress(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def lzma_compress(self) -> CompressionT:
        """Compress using xz lzma

        Returns:
            Chepy: The Chepy object.
        """
        self.state = lzma.compress(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def lzma_decompress(self) -> CompressionT:
        """Decompress lzma compressed data

        Returns:
            Chepy: The Chepy object.
        """
        self.state = lzma.decompress(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def raw_inflate(self) -> CompressionT:
        """Raw inflate data

        Returns:
            Chepy: The Chepy object.
        """
        self.state = zlib.decompress(self._convert_to_bytes(), -15)
        return self

    @ChepyDecorators.call_stack
    def raw_deflate(self) -> CompressionT:
        """Raw deflate data

        Returns:
            Chepy: The Chepy object.
        """
        self.state = zlib.compress(self._convert_to_bytes())[2:-4]
        return self

    @ChepyDecorators.call_stack
    def lz4_compress(self) -> CompressionT:
        """LZ4 compress

        Returns:
            Chepy: The Chepy object.
        """
        self.state = LZ4.compress(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def lz4_decompress(self) -> CompressionT:
        """LZ4 decompress

        Returns:
            Chepy: The Chepy object.
        """
        self.state = LZ4.decompress(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def lz77_compress(self, window_size: int = 13, lookahead_buffer_size: int = 6):
        """To LZ77 compression

        Args:
            window_size (int, optional): Window size. Defaults to 13.
            lookahead_buffer_size (int, optional): Lookahead. Defaults to 6.

        Returns:
            Chepy: The Chepy object.
        """
        self.state = LZ77Compressor(window_size, lookahead_buffer_size).compress(
            self._convert_to_str()
        )
        return self

    def lz77_decompress(self, window_size: int = 13, lookahead_buffer_size: int = 6):
        """From LZ77 compression

        Args:
            window_size (int, optional): Window size. Defaults to 13.
            lookahead_buffer_size (int, optional): Lookahead. Defaults to 6.

        Returns:
            Chepy: The Chepy object.
        """
        assert isinstance(self.state, list), "State is not a list"
        self.state = LZ77Compressor(window_size, lookahead_buffer_size).decompress(
            self.state
        )
        return self
