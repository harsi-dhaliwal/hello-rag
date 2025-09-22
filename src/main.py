import argparse
from chunk import simple_split
from config import settings

def main():
    parser = argparse.ArgumentParser("Print text chunks from a file.")
    parser.add_argument("path", help="Path to a .txt or .md file")
    parser.add_argument("--size",type=int,default=settings.chunk_size, help="Chunk size")
    parser.add_argument("--overlap",type=int,default=settings.chunk_overlap,help="Chunk Overlap")
    args = parser.parse_args()

    settings.validate(require_api=True)
    with open(args.path,"r",encoding="utf-8",errors="ignore")as f:
        text = f.read()

    for chunk in simple_split(text,args.size,args.overlap):
        print(chunk)
        print("-"*40)



if __name__ == "__main__":
    main()