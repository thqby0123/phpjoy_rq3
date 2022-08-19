import os
import re


def unserialize(str):
    str.replace('"','\"')
    f = os.popen(f"php unserilize.php {str}","r")
    result = f.read()
    print(result)


def judge_sink(s,sinks):
    for sink in sinks:
        pattern = f"{sink} .* "
        v = re.findall(pattern,s)
        if len(v)>0:
            return True
    return False

def judge_source(s):
    v1 = re.findall(f"gpc_get.*\(.*\)", s)
    # v1 = re.findall(f"_GET\[.*\]", s)
    # v2 = re.findall(f"_POST\[.*\]", s)
    if len(v1) > 0:
    #if len(v1) > 0 or len(v2) > 0:
        return True
    else:
        return False
