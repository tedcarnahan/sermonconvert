import math
import re

def timecode_to_secs(time_tc):
    m = re.search("(\d\d):(\d\d):(\d\d\.?\d?\d?)", time_tc)
    return int(m[1])*3600 + int(m[2])*60 + math.ceil(float(m[3]))

def secs_to_timecode(time_s):
    pass
