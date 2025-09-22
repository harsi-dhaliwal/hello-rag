import pickle,math
from typing import List,Tuple
from embed import embed_texts

def cosine(a:List[float],b:List[float])->float:
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    return 0.0 if na == 0 or nb == 0 else dot/(na*nb)

def load_index(path:str):
    with open(path,'rb') as f:
       data= pickle.load(f)
    return data["embeddings"], data["chunks"],data["sources"]

def search(query:str,index_path:str,k:int =4)-> List[Tuple[float,str,str]]:
    embs,chunks,sources = load_index(index_path)
    q = embed_texts([query])[0]
    scored = [(cosine(q,v), chunks[i],sources[i]) for i,v in enumerate(embs)]
    scored.sort(key= lambda t: t[0],reverse=True)
    return scored[:k]