import argparse
import os
from typing import List, Tuple
from embed import get_client
from search import search

def build_prompt(query: str, results: List[Tuple[float, str, str]]) -> tuple[str, list[str]]:
    ctx_lines, uniq_sources = [], []
    for _, chunk, src in results:
        ctx_lines.append(f"[{src}] {chunk}")
        root = src.split("#", 1)[0]
        if root not in uniq_sources:
            uniq_sources.append(root)

    context = "\n\n".join(ctx_lines)
    prompt = f"""You are a helpful assistant. Use ONLY the context below.
        If the answer is not clearly in the context, reply: "I don't know based on the provided documents."
        Context:{context}
        Question: {query}
        Guidelines:
            - Keep the answer concise (3-6 sentences).
            - When you rely on a chunk, cite it inline like [filename].
    Answer:"""
    return prompt, uniq_sources

def main():
    p = argparse.ArgumentParser(description="Ask a question over the indexed chunks.")
    p.add_argument("query")
    p.add_argument("--index", default="data/processed/index.pkl")
    p.add_argument("-k", type=int, default=4)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--model", default=os.getenv("CHAT_MODEL", "gpt-4o-mini"))
    args = p.parse_args()

    results = search(args.query, args.index, args.k)
    if not results:
        raise SystemExit("No results. Build the index first or check your data/processed path.")

    prompt, uniq_sources = build_prompt(args.query, results)

    client = get_client()
    resp = client.chat.completions.create(
        model=args.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=args.temperature,
    )
    answer = resp.choices[0].message.content
    print(answer)
    print("\n---\nSources:", ", ".join(uniq_sources))

if __name__ == "__main__":
    main()
