import io
from typing import List, Tuple
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageEnhance
from ..core import ChepyCore, ChepyDecorators


class Multimedia(ChepyCore):
    """The `Multimedia` class is used predominantly to handle image and 
    audio file processing. All the methods within the `Multimedia` class 
    are available in the main **Chepy** class. For coverage, it is important 
    to understand that this class will sometimes coerce non RGBA to RGB and 
    RGB to RGBA formats.
    
    Examples:
        To use the Multimedia class as a standalone, import with
        
        >>> from chepy.modules.multimedia import Multimedia
        >>> m = Multimedia("/path/to/image.png").load_file()
        This will load the image as bytes into Chepy.

        Advanced example using the Multimedia class. We will take 
        our loaded image, convert it split out the RGB color channels, 
        get the blue image, blur it and finally write it to disk. 

        >>> from chepy.modules.multimedia import Multimedia
        >>> m = Multimedia("/path/to/image.png").load_file()
        >>> m.split_color_channels("png")
        {'red': '...', 'blue': '...', 'green': '...'}
        >>> m.get_by_key("blue")
        b"...PNG..."
        >>> m.blur_image("png")
        >>> m.write("/path/to/file.png", as_binary=True)

        This whole operation can be done in one line also.

        >>> from chepy.modules.multimedia import Multimedia
        >>> m = Multimedia("/path/to/image.png").load_file().split_color_channels("png").get_by_key("blue").blur_image().write("/path/to/file.png", as_binary=True)
    """

    def _force_rgba(self, image):  # pragma: no cover
        if image.mode != "RGBA":
            new = image.convert("RGBA")
            return new
        else:
            return image

    def _force_rgb(self, image):  # pragma: no cover
        if image.mode != "RGB":
            new = image.convert("RGB")
            return new
        else:
            return image

    @ChepyDecorators.call_stack
    def resize_image(
        self,
        width: int,
        height: int,
        extension: str = "png",
        resample: str = "nearest",
        quality: int = 100,
    ):
        """Resize an image. 
        
        Args:
            width (int): Required. Width in pixels
            height (int): Required. Height in pixels
            extension (str, optional): File extension of loaded image. Defaults to png
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
        resized = image.resize((width, height), resample=resample)
        resized.save(fh, extension, quality=quality)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def split_color_channels(self, extension: str = "png"):
        """Split an image into its red, green and blue channels

        Args:
            extension (str, optional): File extension of loaded image. Defaults to png
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            Write the blue image to disk in this example

            >>> c = Chepy("logo.png").load_file()
            >>> c.split_color_channels("png")
            {'red': b'...', 'green': b'...', 'blue': b'...'}
            >>> c.get_by_key("blue").write("/path/to/file.png", as_binary=True)
        """
        hold = {}
        image = Image.open(self._load_as_file())
        image = self._force_rgba(image)
        data = image.getdata()

        red = []
        green = []
        blue = []
        for d in data:
            red.append((d[0], 0, 0))
            green.append((0, d[1], 0))
            blue.append((0, 0, d[2]))

        red_fh = io.BytesIO()
        image.putdata(red)
        image.save(red_fh, extension)
        hold["red"] = red_fh.getvalue()

        green_fh = io.BytesIO()
        image.putdata(green)
        image.save(green_fh, extension)
        hold["green"] = green_fh.getvalue()

        blue_fh = io.BytesIO()
        image.putdata(blue)
        image.save(blue_fh, extension)
        hold["blue"] = blue_fh.getvalue()

        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def rotate_image(self, rotate_by: int, extension: str = "png"):
        """Rotate an image
        
        Args:
            rotate_by (int): Required. Roate by degrees
            extension (str, optional): File extension of loaded image. Defaults to png
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            To flip an image horizontally, we can:

            >>> c = Chepy("logo.png").load_file().rotate_image(180, "png")
            >>> c.write('/path/to/file.png', as_binary=True)
        """
        image = Image.open(self._load_as_file())
        fh = io.BytesIO()
        rotated = image.rotate(rotate_by)
        rotated.save(fh, extension)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def blur_image(
        self, extension: str = "png", gaussian: bool = False, radius: int = 2
    ):
        """Blur an image
        
        Args:
            extension (str, optional): File extension of loaded image. Defaults to png
            gaussian (bool, optional): If Gaussian blur is to be applied. Defaults to False.
            radius (int, optional): Radius for Gaussian blur. Defaults to 2.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("logo.png").load_file().blur_image("png")
            >>> >>> c.write('/path/to/file.png', as_binary=True)

            To apply Gaussian blur, use:

            >>> c = Chepy("logo.png").load_file()
            >>> c.blur_image(extension="png", gaussian=True, radius=4)
            >>> >>> c.write('/path/to/file.png', as_binary=True)
        """
        image = Image.open(self._load_as_file())
        fh = io.BytesIO()
        if gaussian:
            blurred = image.filter(ImageFilter.GaussianBlur(radius=radius))
        else:
            blurred = image.filter(ImageFilter.BLUR)
        blurred.save(fh, extension)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def grayscale_image(self, extension: str = "png"):
        """Grayscale an image
        
        Args:
            extension (str, optional): File extension of loaded image. Defaults to png
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("logo.png").load_file().grayscale_image("png")
            >>> >>> c.write('/path/to/file.png', as_binary=True)
        """
        image = Image.open(self._load_as_file())
        fh = io.BytesIO()
        gray = image.convert("LA")
        gray.save(fh, extension)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def invert_image(self, extension: str = "png"):
        """Invert the colors of the image
        
        Args:
            extension (str, optional): File extension of loaded image. Defaults to png
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("logo.png").load_file().invert_image("png")
            >>> >>> c.write('/path/to/file.png', as_binary=True)
        """
        image = Image.open(self._load_as_file())
        image = self._force_rgb(image)
        fh = io.BytesIO()
        inverted = ImageOps.invert(image)
        inverted.save(fh, extension)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def image_opacity(self, level: int, extension: str = "png"):
        """Change the opacity of an image
        
        Args:
            level (int): Required. Level of opacity. Half is 128
            extension (str, optional): File extension of loaded image. Defaults to png
        
        Returns:
            Chepy: The Chepy object. 
        """
        image = Image.open(self._load_as_file())
        image = self._force_rgba(image)
        fh = io.BytesIO()
        image.putalpha(level)
        image.save(fh, extension)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def image_contrast(self, factor: int, extension: str = "png"):
        """Change image contrast
        
        Args:
            factor (int): Factor to increase the contrast by
            extension (str, optional): File extension of loaded image. Defaults to "png"
        
        Returns:
            Chepy: The Chepy object. 
        """
        image = Image.open(self._load_as_file())
        image = self._force_rgb(image)
        fh = io.BytesIO()
        enhanced = ImageEnhance.Contrast(image).enhance(factor)
        enhanced.save(fh, extension)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def image_brightness(self, factor: int, extension: str = "png"):
        """Change image brightness
        
        Args:
            factor (int): Factor to increase the brightness by
            extension (str, optional): File extension of loaded image. Defaults to "png"
        
        Returns:
            Chepy: The Chepy object. 
        """
        image = Image.open(self._load_as_file())
        image = self._force_rgb(image)
        fh = io.BytesIO()
        enhanced = ImageEnhance.Brightness(image).enhance(factor)
        enhanced.save(fh, extension)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def image_sharpness(self, factor: int, extension: str = "png"):
        """Change image sharpness
        
        Args:
            factor (int): Factor to increase the sharpness by
            extension (str, optional): File extension of loaded image. Defaults to "png"
        
        Returns:
            Chepy: The Chepy object. 
        """
        image = Image.open(self._load_as_file())
        image = self._force_rgb(image)
        fh = io.BytesIO()
        enhanced = ImageEnhance.Sharpness(image).enhance(factor)
        enhanced.save(fh, extension)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def image_color(self, factor: int, extension: str = "png"):
        """Change image color
        
        Args:
            factor (int): Factor to increase the color by
            extension (str, optional): File extension of loaded image. Defaults to "png"
        
        Returns:
            Chepy: The Chepy object. 
        """
        image = Image.open(self._load_as_file())
        image = self._force_rgb(image)
        fh = io.BytesIO()
        enhanced = ImageEnhance.Color(image).enhance(factor)
        enhanced.save(fh, extension)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def image_to_asciiart(
        self,
        art_width: int = 120,
        chars: List[str] = ["B", "S", "#", "&", "@", "$", "%", "*", "!", ":", "."],
    ):  # pragma: no cover
        """Convert image to ascii art

        `Reference: <https://dev.to/anuragrana/generating-ascii-art-from-colored-image-using-python-4ace>`__
        
        Args:
            art_width (int, optional): Width of the ascii art. Higher values 
                show more details. Defaults to 120.
            chars (List[str], optional): A list of chars to build the ascii art with
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("pythonlogo.png").load_file()
            >>> c.image_to_asciiart().o
            .::.:..................................................:.::.
            .::......................................................::.
            :.......................&SSSSSSSSSS!.......................:
            ...................*SSSSSSSSSSSSSSSSSSSS....................
            ..................SSSS$@SSSSSSSSSSSSSSSSSS..................
            .................:SSS....SSSSSSSSSSSSSSSSSS.................
            .................:SSS....SSSSSSSSSSSSSSSSSS.................
            .................:SSSSSSSSSSSSSSSSSSSSSSSSS.................
            ..................SSSSSSSSSSSSSSSSSSSSSSSSS.................
            ..............................SSSSSSSSSSSSS.*****!..........
            ........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.*********.......
            ......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.**********......
            .....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.***********.....
            .....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS..************....
            ....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS..************....
            ....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS...*************....
            ....SSSSSSSSSSSSSSSS.....................***************....
            ....SSSSSSSSSSSSS....***********************************....
            ....SSSSSSSSSSSS...*************************************....
            .....SSSSSSSSSSS..**************************************....
            .....SSSSSSSSSSS..*************************************.....
            ......SSSSSSSSSS..************************************......
            .......SSSSSSSSS..**********************************!.......
            ..........SSSSSS..************..............................
            ..................*************************.................
            ..................*************************.................
            ..................******************...****.................
            ..................*****************.....***.................
            ..................******************:.****..................
            ....................*********************...................
            :.......................!***********:......................:
            .::......................................................::.
            .::.:..................................................:.::.
        """
        img = Image.open(self._load_as_file())

        width, height = img.size
        aspect_ratio = height / width
        new_width = art_width
        new_height = aspect_ratio * new_width * 0.55
        img = img.resize((new_width, int(new_height)))
        img = img.convert("L")

        pixels = img.getdata()

        new_pixels = [chars[pixel // 25] for pixel in pixels]
        new_pixels = "".join(new_pixels)

        new_pixels_count = len(new_pixels)
        ascii_image = [
            new_pixels[index : index + new_width]
            for index in range(0, new_pixels_count, new_width)
        ]
        self.state = "\n".join(ascii_image)
        return self

    @ChepyDecorators.call_stack
    def convert_image(self, format_to: str):
        """Change image format. 

        Example, convert png to jpeg
        
        Args:
            format_to (str): Required. A valid image format extension
        
        Returns:
            Chepy: The Chepy object

        Examples:
            For example, to change a png image to a jpeg image, and save it:

            >>> c = Chepy("logo.png").load_file().convert_image("jpeg")
            b'\\xff\\xd8\\xff\\xe0...'
            >>> c.write("/path/to/file.jpeg", as_binary=True)
        """
        image = Image.open(self._load_as_file())
        fh = io.BytesIO()

        if image.mode != "RGB":
            new = image.convert("RGB")
        else:  # pragma: no cover
            new = image

        new.save(fh, format_to)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def image_add_text(
        self,
        text: str,
        extension: str = "png",
        coordinates: Tuple[int, int] = (0, 0),
        color: Tuple[int, int, int] = (0, 0, 0),
    ):
        """Add text to an image
        
        Args:
            text (str): Required. Text to add
            extension (str, optional): File extension of loaded image. Defaults to png
            coordinates (Tuple[int, int], optional): Coordinates of image where to add text. 
                Defaults to (0, 0).
            color (Tuple[int, int, int], optional): Color of text. 
                Defaults to (0, 0, 0) which is black.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("logo.png").load_file().image_add_text("some text")
            b'\\xff\\xd8\\xff\\xe0...'
            >>> c.write("/path/to/file.jpeg", as_binary=True)
        """
        image = Image.open(self._load_as_file())
        fh = io.BytesIO()

        if image.mode != "RGB":
            new = image.convert("RGB")
        else:  # pragma: no cover
            new = image

        ImageDraw.Draw(new).text(coordinates, text, color)
        new.save(fh, extension)
        self.state = fh.getvalue()
        return self

    @ChepyDecorators.call_stack
    def lsb_dump_by_channel(self, channel: str = "r", column_first: bool = False): # pragma: no cover
        """Dump LSB from a specific color channel
        
        Args:
            channel (str, optional): Color channel. r, g, b. Defaults to 'r'.
            column_first (bool, optional): Order by column first. Defaults to False.
        
        Returns:
            Chepy: The Chepy object. 
        """
        channels = ["r", "g", "b"]
        assert channel in channels, "Valid channels are {}".format("".join(channels))
        if channel == "r":
            index = 0
        elif channel == "g":
            index = 1
        elif channel == "b":
            index = 2
        image = Image.open(self._load_as_file())
        pixels = image.load()
        if column_first:
            height, width = image.size
        else:
            width, height = image.size

        data = ""
        for y in range(height):
            for x in range(width):
                try:
                    pix = pixels[x, y][index]
                    lsb = bin(pix).zfill(8)[-1]
                    data += lsb
                except IndexError:
                    break

        self.state = data
        return self

    @ChepyDecorators.call_stack
    def msb_dump_by_channel(self, channel: str = "r", column_first: bool = False): # pragma: no cover
        """Dump MSB from a specific color channel
        
        Args:
            channel (str, optional): Color channel. r, g, b. Defaults to 'r'.
            column_first (bool, optional): Order by column first. Defaults to False.
        
        Returns:
            Chepy: The Chepy object. 
        """
        channels = ["r", "g", "b"]
        assert channel in channels, "Valid channels are {}".format("".join(channels))
        if channel == "r":
            index = 0
        elif channel == "g":
            index = 1
        elif channel == "b":
            index = 2
        image = Image.open(self._load_as_file())
        pixels = image.load()
        if column_first:
            height, width = image.size
        else:
            width, height = image.size

        data = ""
        for x in range(height):
            for y in range(width):
                val = pixels[x, y][index]
                data += ((bin(val)[2:]).zfill(8))[0]

        self.state = data
        return self
