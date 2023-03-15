def binary_search_score_colors(list, item):    
    if item > int(list[0].score) or item < int(list[len(list)-1].score):
       return None  
    low = 0
    high = len(list) - 1
    
    while low <= high:
        mid = (low+high)//2        
        guess = int(list[mid].score)        
        highBound = int(list[mid-1].score)
        lowBound = int(list[mid+1].score)             
        if guess == item:           
            return list[mid].color
        elif lowBound < item < highBound:            
            return list[mid].color
        elif guess > item:
            low = mid - 1
        elif guess < item:
            high = mid + 1
        else:
            return None
    return list[mid].color