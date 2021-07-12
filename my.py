import re


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


print(findWholeWord('rambler')("1966 Rambler Classic 770"))
