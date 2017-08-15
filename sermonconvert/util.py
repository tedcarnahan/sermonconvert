import math
import re

def timecode_to_secs(time_tc) -> int:
    m = re.search("(\d\d):(\d\d):(\d\d\.?\d?\d?)", time_tc)
    return int(m[1])*3600 + int(m[2])*60 + math.ceil(float(m[3]))

def secs_to_timecode(time_s) -> str:
    hours = time_s // 3600
    time_s -= (hours*3600)
    mins = time_s // 60
    time_s -= (mins*60)
    return "{0:02d}:{1:02d}:{2:02d}".format(int(hours), int(mins), int(time_s))
