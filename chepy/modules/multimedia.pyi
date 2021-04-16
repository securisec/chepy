from ..core import ChepyCore as ChepyCore, ChepyDecorators as ChepyDecorators
from typing import Any, List, Tuple, TypeVar

MultimediaT = TypeVar('MultimediaT', bound='Multimedia')

class Multimedia(ChepyCore):
    def __init__(self, *data: Any) -> None: ...
    state: Any = ...
    def resize_image(self, width: int, height: int, extension: str=..., resample: str=..., quality: int=...) -> MultimediaT: ...
    def split_color_channels(self, extension: str=...) -> MultimediaT: ...
    def rotate_image(self, rotate_by: int, extension: str=...) -> MultimediaT: ...
    def blur_image(self, extension: str=..., gaussian: bool=..., radius: int=...) -> MultimediaT: ...
    def grayscale_image(self, extension: str=...) -> MultimediaT: ...
    def invert_image(self, extension: str=...) -> MultimediaT: ...
    def image_opacity(self, level: int, extension: str=...) -> MultimediaT: ...
    def image_contrast(self, factor: int, extension: str=...) -> MultimediaT: ...
    def image_brightness(self, factor: int, extension: str=...) -> MultimediaT: ...
    def image_sharpness(self, factor: int, extension: str=...) -> MultimediaT: ...
    def image_color(self, factor: int, extension: str=...) -> MultimediaT: ...
    def image_to_asciiart(self, art_width: int=..., chars: List[str]=...) -> MultimediaT: ...
    def convert_image(self, format_to: str) -> MultimediaT: ...
    def image_add_text(self, text: str, extension: str=..., coordinates: Tuple[int, int]=..., color: Tuple[int, int, int]=...) -> MultimediaT: ...
    def lsb_dump_by_channel(self, channel: str=..., column_first: bool=...) -> MultimediaT: ...
    def msb_dump_by_channel(self, channel: str=..., column_first: bool=...) -> MultimediaT: ...
