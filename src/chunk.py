import re

from collections.abc import Iterator

_sentence_splitter = re.compile(r'(?<=[.!?])\s+')

def sentence_split(text: str)->list[str]:
    return _sentence_splitter.split(text.strip())

def simple_split(text:str, size:int =800,overlap:int =120)->Iterator[str]:
    sentences = sentence_split(text)
    chunk,length = [],0
    for sent in sentences:
        if length+len(sent)>size and chunk:
            yield " ".join(chunk)
            overlap_sents = chunk[-1:]
            chunk = overlap_sents + [sent]
            length = sum(len(s) for s in chunk)
        else:
            chunk.append(sent)
            length += len(sent)
    if chunk:
        yield " ".join(chunk)
