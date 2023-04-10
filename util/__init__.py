from typing import Tuple


def convert_millis(millis) -> str:
    """Convert milliseconds to hours, minutes, seconds.

    Args:
        millis (int): The time in milliseconds.

    Returns:
        str: Date time in hours, minutes, seconds.
    """
    seconds=(millis/1000)%60
    minutes=(millis/(1000*60))%60
    hours=(millis/(1000*60*60))%24
    return "%d:%02d:%02d" % (hours, minutes, seconds)

def hex_to_rgb(hex) -> Tuple[int]:
    """Convert hex to rgb.

    Args:
        hex (hex): Represents a color in hex.

    Returns:
        Tuple[int]: Returns a tuple of rgb values.
    """
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))