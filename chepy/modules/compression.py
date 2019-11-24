import io
import bz2
import gzip
import zlib
import zipfile
from ..core import ChepyCore


class Compression(ChepyCore):
    def zip_info(self):
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

    def zip_list_files(self):
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

    def unzip_one(self, file: str, password: str = None):
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

    def unzip_all(self, password: str = None):
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

    def create_zip_file(self, file_name: str):
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

    def gzip_compress(self, file_name: str = None):
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

    def gzip_decompress(self):
        """Decompress a gzip archive
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = gzip.decompress(self._convert_to_bytes())
        return self

    def bzip_compress(self):
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

    def bzip_decompress(self):
        """Decompress a bz2 archive
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = bz2.decompress(self._convert_to_bytes())
        return self

    def zlib_compress(self, level: int = 9):
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

    def zlib_decompress(self):
        """Zlib decompression
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("789c0580a10d000008c35ee1b9ca05c104e737b761ca5711e8039a")
            >>> c.hex_to_binary()
            >>> c.zlib_decompress()
            >>> c.out()
            b"some text"
        """
        self.state = zlib.decompress(self._convert_to_bytes())
        return self
