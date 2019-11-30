import io
import os
import logging
import pathlib
import tempfile
import pprint

import exiftool
from hachoir.core.log import Logger
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from hachoir.subfile.search import SearchSubfile
from hachoir.stream import FileInputStream
from hachoir.metadata.metadata_item import QUALITY_BEST
import hachoir.core.config as hachoir_config

from ..core import ChepyCore, ChepyDecorators


class Forensics(ChepyCore):
    hachoir_config.quiet = True

    def _temp_file(self) -> str:
        """Get a random temporary file. os.urandom is used here 
        because of permission issues using tempfile on Windows. 
        The state is then saved in this temp file.
        
        Returns:
            str: cross platform temporary file
        """
        temp_file = str(pathlib.Path(tempfile.gettempdir()) / os.urandom(24).hex())
        with open(temp_file, "wb") as f:
            f.write(self._convert_to_bytes())
        return temp_file

    @ChepyDecorators.call_stack
    def get_mime(self, set_state: bool = False):
        """Detect the file type based on magic.

        Args:
            set_state (bool, optional): Save the output to state. Defaults to False.
        
        Returns:
            Chepy: The Chepy object. 
        """
        filename = self._temp_file()
        parser = createParser(filename)
        if not parser:
            mimetype = "text/plain"
            logging.info(mimetype)
        else:
            mimetype = str(parser.mime_type)
            logging.info(mimetype)
        if set_state:
            self.state = mimetype
        # pathlib.Path(filename).unlink()
        return self

    @ChepyDecorators.call_stack
    def get_metadata(self, set_state: bool = False):
        """Get metadata from a file
        
        Args:
            set_state (bool, optional): Save the output to state. Defaults to False.
        
        Returns:
            Chepy: The Chepy object. 
        """
        filename = self._temp_file()
        filename, realname = filename, filename
        parser = createParser(filename, realname)
        if not parser:  # pragma: no cover
            logging.warning("Unable to parse file")

        metadata = extractMetadata(parser, quality=QUALITY_BEST)

        if metadata is not None:
            meta = metadata.exportDictionary()["Metadata"]
            if set_state:
                self.state = meta
            else:  # pragma: no cover
                logging.info(pprint.pformat(meta))
        # pathlib.Path(filename).unlink()
        return self

    @ChepyDecorators.call_stack
    def embedded_files(self, extract_path: str = None):
        """Search for embedded files and extract them

        This method does not change the state. 
        
        Args:
            extract_path (str, optional): Path to extract files to. Defaults to None.
        
        Returns:
            Chepy: The Chepy object. 
        """
        filename = self._temp_file()
        inp = FileInputStream(filename)
        subfile = SearchSubfile(inp)
        if extract_path is not None:  # pragma: no cover
            subfile.setOutput(extract_path)
        subfile.loadParsers()
        subfile.main()
        # pathlib.Path(filename).unlink()
        return self

    @ChepyDecorators.call_stack
    def get_exif(self):  # pragma: no cover
        """Extract EXIF data from a file
        
        Returns:
            Chepy: The Chepy object. 
        """
        filename = self._temp_file()
        with exiftool.ExifTool() as et:
            exif = et.get_metadata(filename)
            if exif:
                self.state = exif
        # pathlib.Path(filename).unlink()
        return self
