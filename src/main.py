import argparse
from chunk import simple_split
def main():
    parser = argparse.ArgumentParser("Print text chunks from a file.")
    parser.add_argument("path", help="Path to a .txt or .md file")
    parser.add_argument("--size",type=int,default=800, help="Chunk size")
    parser.add_argument("--overlap",type=int,default=120,help="Chunk Overlap")
    args = parser.parse_args()

    with open(args.path,"r",encoding="utf-8",errors="ignore")as f:
        text = f.read()

    for chunk in simple_split(text,args.size,args.overlap):
        print(chunk)



if __name__ == "__main__":
    main()