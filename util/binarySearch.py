from typing import List
from objects.raiderIO.scoreColor import ScoreColor

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
        print(mid)
        if score_color_list[mid].score == input_score:
            return score_color_list[mid].color
        elif score_color_list[mid].score > input_score:
            left = mid + 1
        else:
            right = mid -1
        if nearest is None or abs(score_color_list[mid].score - input_score) < abs(nearest.score - input_score):
            nearest = score_color_list[mid]
    return nearest.color
    