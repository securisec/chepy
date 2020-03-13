from string import ascii_lowercase, ascii_uppercase, digits


def base64_char_sets() -> dict:
    """Get various combinations of base64 character sets
    
    Returns:
        dict: Dict of various char sets
    """
    return {
        "standard": ascii_uppercase + ascii_lowercase + digits + "+/=",  # A-Za-z0-9+/=
        "url_safe": ascii_uppercase + ascii_lowercase + digits + "-_",  # A-Za-z0-9-_
        "filename_safe": ascii_uppercase
        + ascii_lowercase
        + digits
        + "+\\-=",  # A-Za-z0-9+\-=
        "itoa64": "./"
        + digits
        + ascii_uppercase
        + ascii_lowercase
        + "=",  # ./0-9A-Za-z=
        "xml": ascii_uppercase + ascii_lowercase + digits + "_.",  # A-Za-z0-9_.
        "y64": ascii_uppercase + ascii_lowercase + digits + "._-",  # A-Za-z0-9._-
        "z64": digits + ascii_lowercase + ascii_uppercase + "+/=",  # 0-9a-zA-Z+/=
        "radix64": digits + ascii_uppercase + ascii_lowercase + "+/=",  # 0-9A-Za-z+/=
        "uuencoding": " -_",
        "xxencoding": "+\\-"
        + digits
        + ascii_uppercase
        + ascii_lowercase,  # +\-0-9A-Za-z
        "unix_crypt": "./" + digits + ascii_uppercase + ascii_lowercase,  # ./0-9A-Za-z
    }
