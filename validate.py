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