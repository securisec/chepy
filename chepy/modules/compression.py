import io
import zipfile
from ..core import Core


class Compression(Core):
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
        return self

    def unzip_one(self, file: str, password: str = None):
        """Unzip one file from zipfile

        Use zip_info to get all the filenames within the zip archive
        
        Args:
            file (str): Path of file inside the archive
            password (str, optional): Password if zip is encrypted. Defaults to None.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("/path/to/zip.zip").load_file()
            >>> c.zip_info()
            [{...filename: "somefile.txt"...}]
            >>> c.unzip_one("somefile.txt")
            b"Hello World!"
        """
        z = zipfile.ZipFile(self._load_as_file())
        if password is not None:
            z.setpassword(password.encode())
        self.state = z.read(file)
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
        data = io.BytesIO()
        z = zipfile.ZipFile(data, mode="w", compression=zipfile.ZIP_DEFLATED)
        z.writestr(file_name, self.state)
        z.close()
        self.state = data.getvalue()
        return self
