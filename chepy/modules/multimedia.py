import io
from PIL import Image
from ..core import Core


class Multimedia(Core):
    def resize_image(
        self,
        width: int,
        height: int,
        extension: str,
        resample: str = "nearest",
        quality: int = 100,
    ):
        """Resize an image. 
        
        Args:
            Core ([type]): [description]
            width (int): Width in pixels
            height (int): Height in pixels
            extension (str): File extension of loaded image
            resample (str, optional): Resample rate. Defaults to "nearest".
            quality (int, optional): Quality of output. Defaults to 100.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("image.png").load_file().resize_image(256, 256, "png")
            >>> c.write_to_file("/path/to/file.png", as_binary=True)
        """
        fh = io.BytesIO()
        if resample == "nearest":
            resample = Image.NEAREST
        elif resample == "antialias":
            resample = Image.ANTIALIAS
        elif resample == "bilinear":
            resample = Image.BILINEAR
        elif resample == "box":
            resample = Image.BOX
        elif resample == "hamming":
            resample = Image.HAMMING
        else:  # pragma: no cover
            raise TypeError(
                "Valid resampling options are: nearest, antialias, bilinear, box and hamming"
            )
        image = Image.open(self._load_as_file())
        resized = image.resize((width, height))
        resized.save(fh, extension, quality=quality)
        self.state = fh.getvalue()
        return self

    def split_color_channels(self):
        """Split an image into its red, green and blue channels
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            Write the red image to disk in this example

            >>> c = Chepy("logo.png").load_file()
            >>> c.split_color_channels()
            {'red': b'...', 'green': b'...', 'blue': b'...'}
            >>> c.get_by_key("blue").write("/path/to/file.png", as_binary=True)
        """
        hold = {}
        image = Image.open(self._load_as_file())
        data = image.getdata()

        red = [(d[0], 0, 0) for d in data]
        green = [(0, d[1], 0) for d in data]
        blue = [(0, 0, d[2]) for d in data]

        red_fh = io.BytesIO()
        image.putdata(red)
        image.save(red_fh, "png")
        hold["red"] = red_fh.getvalue()

        green_fh = io.BytesIO()
        image.putdata(green)
        image.save(green_fh, "png")
        hold["green"] = green_fh.getvalue()

        blue_fh = io.BytesIO()
        image.putdata(blue)
        image.save(blue_fh, "png")
        hold["blue"] = blue_fh.getvalue()

        self.state = hold
        return self

    def rotate_image(self, rotate_by: int):
        """Rotate an image
        
        Args:
            rotate_by (int): Roate by degrees
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            To flip an image horizontally, we can:

            >>> c = Chepy("logo.png").load_file().rotate_image(180)
            >>> c.write('/path/to/file.png', as_binary=True)
        """
        image = Image.open(self._load_as_file())
        fh = io.BytesIO()
        rotated = image.rotate(70)
        rotated.save(fh, "png")
        self.state = fh.getvalue()
        return self
