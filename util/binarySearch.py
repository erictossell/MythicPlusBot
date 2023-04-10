def binary_search_score_colors(score_color_list, input_score):
        
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
    