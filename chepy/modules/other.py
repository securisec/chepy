from uuid import uuid4

from ..core import Core


class Other(Core):
    def generate_uuid(self) -> str:
        """Generate v4 UUID

        Generates an RFC 4122 version 4 compliant Universally Unique Identifier 
        (UUID), also known as a Globally Unique Identifier (GUID). A version 4 
        UUID relies on random numbers
        
        Returns:
            str: A random UUID

        Examples:
            >>> Chepy('').generate_uuid()
            92644a99-632a-47c1-b169-5a141172924b
        """
        self.state = str(uuid4())
        return self
