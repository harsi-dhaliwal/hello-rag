import re

from collections.abc import Iterator

def simple_split(text:str, size:int =800,overlap:int =120)->Iterator[str]:
    text = re.sub(r"\s+"," ",text).strip()
    start = 0
    n = len(text)

    while start<n:
        end = min(start+size,n)
        yield text[start:end]
        start = max(end-overlap,start+1)
