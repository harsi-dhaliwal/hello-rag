import pickle
from pathlib import Path
from chunk import simple_split
from embed import embed_texts
from config import settings

def read_texts(raw_dir:str)-> list[tuple[str,str]]:
    out = []
    for doc in Path(raw_dir).glob("**/*"):
        if (doc.suffix.lower()in {".txt",".md"}):
            out.append((doc.name,doc.read_text(encoding="utf-8",errors="ignore")))
    return out

def build_index(raw_dir:str = "data",out_path: str = "data/processed/index.pkl",size:int = 600,overlap:int= 80)->None:
    docs = read_texts(raw_dir=raw_dir)
    chunks, sources = [],[]
    for fname,text in docs:
        for i,ch in enumerate(simple_split(text=text,size=size,overlap=overlap)):
            chunks.append(ch)
            sources.append(f"{fname}#chunk{i}")
    if not chunks:
        raise SystemExit("No text files found to index. Put .txt or .md in data/")
    vecs = embed_texts(chunks)
    Path(out_path).parent.mkdir(parents=True,exist_ok=True)

    with open(out_path,"wb") as f:
        pickle.dump({"embeddings":vecs,"chunks":chunks,"sources":sources},f)
    print(f"Indexed {len(chunks)} chunks from {len(docs)} file(s) -> {out_path}")

def main():
    build_index()

if __name__ == "__main__":
    main()