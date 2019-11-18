import ujson
from lxml import etree
from ..core import Core


class CodeTidy(Core):
    def minify_json(self):
        """Minify JSON string
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("/path/to/file.json").load_file()
            >>> print(c.minify_json())
        """
        self.state = ujson.dumps(ujson.loads(self._convert_to_str()))
        return self

    def beautify_json(self, indent: int = 2):
        """Beautify minified JSON
        
        Args:
            indent (int, optional): Indent level. Defaults to 2.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("/path/to/file.json").load_file()
            >>> print(c.beautify_json(indent=4))
        """
        self.state = ujson.dumps(ujson.loads(self._convert_to_str()), indent=indent)
        return self

    def minify_xml(self):
        """Minify XML string
        
        Returns:
            Chepy: The Chepy object. 
        
        Examples:
            >>> c = Chepy("/path/to/file.xml").load_file()
            >>> print(c.minify_xml())
        """
        parser = etree.XMLParser(remove_blank_text=True)
        self.state = etree.tostring(
            etree.fromstring(self._convert_to_bytes(), parser=parser)
        )
        return self

    def beautify_xml(self):
        """Beautify compressed XML
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("/path/to/file.xml").load_file()
            >>> print(c.beautify_json())
        """
        parser = etree.XMLParser(remove_blank_text=True)
        self.state = etree.tostring(
            etree.fromstring(self._convert_to_bytes()), pretty_print=True
        )
        return self
