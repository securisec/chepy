from typing import List, Union


def detect_delimiter(
    data: Union[str, bytes],
    delimiters: List[Union[str, bytes]] = [
        " ",
        ";",
        ".",
        "-",
        "\\",
        ":",
        "/",
        ",",
        "\n",
        "\\x",
        "\\0x",
    ],
    default_delimiter: str = " ",
) -> Union[str, bytes, None]:
    """Detect delimiter

    Args:
        data (Union[str, bytes]): Data
        delimiters (List[Union[str, bytes]], optional): Array of delimiters. Defaults to [" ", ";", ".", "-", "\"].
        default_delimiter (str): The default delimiter

    Returns:
        Union[str, bytes, None]: Delimiter or None if one is not found
    """
    is_bytes = False
    if isinstance(data, bytes):  # pragma: no cover
        delimiters = [d.encode() for d in delimiters]
        is_bytes = True

    for delimiter in delimiters:
        parts = data.split(delimiter)
        if len(parts) > 1 and all(part.strip() for part in parts):
            return delimiter

    if default_delimiter: # pragma: no cover
        return default_delimiter.encode() if is_bytes else default_delimiter
    else:
        return None
