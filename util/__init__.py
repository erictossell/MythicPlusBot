from typing import Tuple, List
from raiderIO.scoreColor import ScoreColor

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



def binary_search_score_colors(score_color_list: List[ScoreColor], input_score: int):
    """Search for the color that corresponds to the input score.

    Args:
        score_color_list (List[ScoreColor]): A list of ScoreColor objects.
        input_score (int): A score to search for.

    Returns:
        ScoreColor: The ScoreColor object with the nearest value to the input score.
    """

    left = 0
    right = len(score_color_list) - 1
    nearest = None
    
    while left <= right:
        mid = (left + right) // 2
        if score_color_list[mid].score == input_score:
            return score_color_list[mid].color
        elif score_color_list[mid].score > input_score:
            left = mid + 1
        else:
            right = mid -1
        if nearest is None or abs(score_color_list[mid].score - input_score) < abs(nearest.score - input_score):
            nearest = score_color_list[mid]
    return nearest.color