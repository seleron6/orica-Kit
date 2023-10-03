import re

def validateNumber(text,lLimit,uLimit):
    value = 0
    lLimit=int(lLimit)
    uLimit=int(uLimit)
    if text:
        try:
            if re.fullmatch('[0-9]+', text) is None:
                return False
            value = int(text)
        except ValueError:
            return False
    return True if lLimit <= value <= uLimit else False

def validateDecHex(text,ver):
    if text=="": return True
    if ver=="dec":
        try:
            text=hex(int(text))
        except:
            return False
        else:
            return True
    elif ver=="hex":
        if re.fullmatch('[1-9a-fA-F]+', text): return True
        if not (text.startswith("0x") or text.startswith("0X")): return False
        if text in ("0x","0X"): return True
        try:
            text=int(text,0)
        except:
            return False
        else:
            return True
    else:
        return False