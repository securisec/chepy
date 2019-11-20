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
