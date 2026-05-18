"""Quick test of the formatted RAG output."""
from rag import ask

queries = [
    "What are the three doshas in Ayurveda?",
    "How does turmeric help in healing?",
]

for q in queries:
    print("=" * 60)
    print(f"Q: {q}")
    print("=" * 60)
    r = ask(q)
    print(r["answer"])
    print()
    for s in r["sources"]:
        print(f"  >> {s['file']} - Page {s['page']} (relevance: {s['relevance']})")
    print()
