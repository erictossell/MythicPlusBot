

def convertMillis(millis):
    seconds=(millis/1000)%60
    minutes=(millis/(1000*60))%60
    hours=(millis/(1000*60*60))%24
    return "%d:%02d:%02d" % (hours, minutes, seconds)