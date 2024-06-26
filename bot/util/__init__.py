import datetime
from datetime import time
from typing import Tuple, List

from bot.raiderIO.models.score_color import ScoreColor


def convert_millis(millis) -> time:
    """Convert milliseconds to hours, minutes, seconds.

    Args:
        millis (int): The time in milliseconds.

    Returns:
        str: Date time in hours, minutes, seconds.
    """
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000 * 60 * 60)) % 24
    hours = int(hours)
    time = datetime.time(hours, minutes, seconds)

    return time


def hex_to_rgb(hex) -> Tuple[int]:
    """Convert hex to rgb.

    Args:
        hex (hex): Represents a color in hex.

    Returns:
        Tuple[int]: Returns a tuple of rgb values.
    """
    hex = hex.lstrip("#")
    return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))


def binary_search_score_colors(
    score_color_list: List[ScoreColor], input_score: int
) -> ScoreColor:
    """Search for the color that corresponds to the input score.

    Args:
        score_color_list (List[ScoreColor]): A list of ScoreColor objects.
        input_score (int): A score to search for.

    Returns:
        ScoreColor: The ScoreColor object with the nearest value to the input score.
    """
    if score_color_list is None or len(score_color_list) == 0:
        return None
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
            right = mid - 1
        if nearest is None or abs(score_color_list[mid].score - input_score) < abs(
            nearest.score - input_score
        ):
            nearest = score_color_list[mid]
    return nearest.color


def seconds_until(hours, minutes):
    given_time = datetime.time(hours, minutes)
    now = datetime.datetime.now()
    future_exec = datetime.datetime.combine(now, given_time)
    if (future_exec - now).days < 0:
        future_exec = datetime.datetime.combine(
            now + datetime.timedelta(days=1), given_time
        )
    return (future_exec - now).total_seconds()


def time_until_target(hour, minute) -> datetime.timedelta:
    now = datetime.datetime.now()
    target = datetime.datetime(now.year, now.month, now.day, hour, minute)

    if now > target:
        target += datetime.timedelta(days=1)

    return (target - now).total_seconds()


def time_without_leading_zeros(t: time):
    if t.hour == 0:
        if t.minute == 0:
            return f"{t.second}s"
        else:
            return f"{t.minute}m {t.second}s"
    else:
        return f"{t.hour}h {t.minute}m {t.second}s"
