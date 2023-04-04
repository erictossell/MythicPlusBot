import bisect

from objects.raiderIO.scoreColor import ScoreColor


def binary_search_score_colors(score_color_list, item):
    if not isinstance(item, int):
        raise TypeError("item must be an integer")
    for i in range(len(score_color_list) - 1):
        if score_color_list[i].score < score_color_list[i + 1].score:
            raise ValueError("score_color_list must be sorted in descending order by score")
    index = bisect.bisect_left(score_color_list, ScoreColor(item, None))
    if index == len(score_color_list):
        return score_color_list[-1].color
    if score_color_list[index].score == item:
        return score_color_list[index].color
    low_bound = score_color_list[index].score
    high_bound = score_color_list[index - 1].score
    if low_bound <= item <= high_bound:
        return score_color_list[index].color
    return score_color_list[-1].color
    