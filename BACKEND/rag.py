"""
AI Vaidya — Offline RAG Backend
Loads PDFs from pdf_database/, chunks them, embeds with SentenceTransformers,
stores in ChromaDB, and answers queries using retrieved context only.
"""

import os
import shutil
import hashlib
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# ── Config ──────────────────────────────────────────────────────
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", "pdf_database"))
CHROMA_DIR = os.path.abspath(os.path.join(_THIS_DIR, "chroma_db"))
EMBED_MODEL = "all-MiniLM-L6-v2"  # fast, ~80MB, runs on CPU
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 3


# ── 1. Load all PDFs ───────────────────────────────────────────
def load_pdfs(folder: str) -> list:
    """Load all PDF files from the given folder and return LangChain Documents."""
    folder = os.path.abspath(folder)
    docs = []
    pdf_files = sorted(Path(folder).glob("*.pdf"))

    if not pdf_files:
        print(f"[!] No PDF files found in {folder}")
        return docs

    for pdf_path in pdf_files:
        print(f"[>>] Loading: {pdf_path.name}")
        try:
            loader = PyPDFLoader(str(pdf_path))
            pages = loader.load()
            # Tag each page with the source filename
            for page in pages:
                page.metadata["source_file"] = pdf_path.name
            docs.extend(pages)
        except Exception as e:
            print(f"   [!] Failed to load {pdf_path.name}: {e}")

    print(f"[OK] Loaded {len(docs)} pages from {len(pdf_files)} PDFs\n")
    return docs


# ── 2. Split into chunks ──────────────────────────────────────
def split_documents(docs: list) -> list:
    """Split documents into smaller chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"[OK] Split into {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})\n")
    return chunks


# ── 3. Build / Load vector store ──────────────────────────────
def _compute_pdf_hash(folder: str) -> str:
    """Hash all PDF filenames + sizes to detect changes."""
    folder = os.path.abspath(folder)
    entries = []
    for f in sorted(Path(folder).glob("*.pdf")):
        entries.append(f"{f.name}:{f.stat().st_size}")
    return hashlib.md5("|".join(entries).encode()).hexdigest()


def get_vectorstore() -> Chroma:
    """
    Build the ChromaDB vector store from PDFs.
    Re-uses existing store if PDFs haven't changed.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    hash_file = os.path.join(CHROMA_DIR, ".pdf_hash")
    current_hash = _compute_pdf_hash(PDF_FOLDER)

    # Check if we can reuse existing DB
    if os.path.exists(CHROMA_DIR) and os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            stored_hash = f.read().strip()
        if stored_hash == current_hash:
            print("[CACHE] Reusing existing ChromaDB (PDFs unchanged)\n")
            return Chroma(
                persist_directory=CHROMA_DIR,
                embedding_function=embeddings,
            )

    # Build fresh
    print("[BUILD] Building new ChromaDB index...\n")
    docs = load_pdfs(PDF_FOLDER)
    if not docs:
        raise FileNotFoundError(f"No PDFs found in {os.path.abspath(PDF_FOLDER)}")

    chunks = split_documents(docs)

    # Remove old DB if exists
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )

    # Save hash so we skip next time
    os.makedirs(CHROMA_DIR, exist_ok=True)
    with open(hash_file, "w") as f:
        f.write(current_hash)

    print(f"[OK] ChromaDB index built with {len(chunks)} chunks\n")
    return vectorstore


# ── 4. Format answer (no LLM) ─────────────────────────────────
import re

def _clean_text(text: str) -> str:
    """Remove citation noise, DOI links, references, and normalize whitespace."""
    # Remove DOI patterns
    text = re.sub(r'10\.\d{4,}/[^\s]+', '', text)
    # Remove bracketed reference numbers [1], [2-5], [1,3,7]
    text = re.sub(r'\[\d+[\-,\d]*\]', '', text)
    # Remove year citations (2016), (2003)
    text = re.sub(r'\(\d{4}\)', '', text)
    # Remove volume:page patterns like 30:1605-14, 86:75-89
    text = re.sub(r'\d+:\d+[\-–]\d+', '', text)
    # Remove "Page X" metadata
    text = re.sub(r'\[Page \d+\]', '', text)
    # Remove author citation patterns: "Surname AB, Surname CD, et al.:"
    text = re.sub(r'[A-Z][a-z]+ [A-Z]{1,2},\s*(?:[A-Z][a-z]+ [A-Z]{1,2},?\s*)+(?:et al\.?)?:', '', text)
    text = re.sub(r'[A-Z][a-z]+ [A-Z]{1,2},\s*(?:[A-Z][a-z]+ [A-Z]{1,2},?\s*)+(?:et al\.?)?\.?', '', text)
    # Remove "StatPearls, Treasure Island" and similar publisher refs
    text = re.sub(r'StatPearls.*?(?:\.|;)', '', text)
    # Remove journal-style fragments
    text = re.sub(r'(?:Br |Med |ACS |J |Am |Int |Phytother )[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\.', '', text)
    # Remove source headers (NIA / CCRAS / AYUSH lines, URLs)
    text = re.sub(r'Sources?:.*', '', text)
    text = re.sub(r'Ayurveda Knowledge Compilation[^.]*\.?', '', text)
    text = re.sub(r'SECTION \d+:[^\n]*', '', text)
    text = re.sub(r'National Institute of Ayurveda[^.]*\.?', '', text)
    text = re.sub(r'Standardization of[^.]*\.?', '', text)
    text = re.sub(r'(?:nia|niimh|ayush|ijcrt|ayushdhara)\.\w+\.\w+', '', text)
    text = re.sub(r'Generated \d{4}-\d{2}-\d{2}', '', text)
    # Remove "― IJCRT Vol..." type citations
    text = re.sub(r'[―–—]\s*(?:IJCRT|MMM|Vol).*?(?:\.|$)', '', text)
    # Remove "STAR*D report" and similar noise
    text = re.sub(r'STAR\*D[^.]*\.?', '', text)

    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or len(stripped) < 30:
            continue
        # Skip lines that are mostly non-alpha (reference lists)
        alpha_chars = sum(1 for c in stripped if c.isalpha())
        if alpha_chars / max(len(stripped), 1) < 0.5:
            continue
        clean_lines.append(stripped)
    text = ' '.join(clean_lines)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()


def _deduplicate_sentences(text: str) -> list[str]:
    """Split text into sentences and remove near-duplicates."""
    # Split on period followed by space or newline
    raw_sentences = re.split(r'(?<=[.!?])\s+', text)
    seen = set()
    unique = []
    for sent in raw_sentences:
        sent = sent.strip()
        if len(sent) < 15:
            continue
        # Normalize for dedup comparison
        key = re.sub(r'[^a-z0-9]', '', sent.lower())[:80]
        if key not in seen:
            seen.add(key)
            unique.append(sent)
    return unique


def _format_as_bullets(sentences: list[str], max_bullets: int = 8) -> str:
    """Format unique sentences as clean markdown bullet points."""
    bullets = []
    for sent in sentences[:max_bullets]:
        # Ensure sentence ends with period
        if sent and sent[-1] not in '.!?':
            sent += '.'
        # Capitalize first letter
        sent = sent[0].upper() + sent[1:] if sent else sent
        bullets.append(f"- {sent}")
    return '\n'.join(bullets)


# ── 5. Answer a query ─────────────────────────────────────────
def get_answer(query: str, vectorstore: Chroma = None, chat_context: list = None) -> dict:
    """
    Retrieve relevant chunks and return a formatted answer.

    Args:
        query: The user's question.
        vectorstore: ChromaDB vector store instance.
        chat_context: Optional list of recent chat messages for context.
                      Each item: {"role": "user"|"assistant", "content": str}

    Returns:
        {
            "answer": str,       # cleaned, bullet-pointed answer
            "sources": [         # list of source references
                {"file": str, "page": int, "text": str},
                ...
            ]
        }
    """
    if vectorstore is None:
        vectorstore = get_vectorstore()

    # Retrieve top-K similar chunks
    results = vectorstore.similarity_search_with_score(query, k=TOP_K)

    if not results:
        return {
            "answer": "No relevant information found in the knowledge base for your question.",
            "sources": [],
        }

    # Build sources and collect raw text
    source_entries = []
    all_text_parts = []

    for doc, score in results:
        text = doc.page_content.strip()
        file_name = doc.metadata.get("source_file", "Unknown")
        page_num = doc.metadata.get("page", "?")

        all_text_parts.append(text)
        source_entries.append({
            "file": file_name,
            "page": int(page_num) + 1 if isinstance(page_num, int) else page_num,
            "text": text[:300] + "..." if len(text) > 300 else text,
            "relevance": round(1 / (1 + score), 3),
        })

    # ── Post-process: clean, dedup, bullet-point ──────────────
    combined_raw = ' '.join(all_text_parts)

    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    # Build conversation history string for context
    history_str = ""
    if chat_context:
        recent = chat_context[-6:]  # Last 3 exchanges (6 messages max)
        for msg in recent:
            role = "User" if msg["role"] == "user" else "AI Vaidya"
            history_str += f"{role}: {msg['content'][:200]}\n"

    answer = None
    if api_key and api_key != "your_api_key_here":
        try:
            from google import genai
            client = genai.Client(api_key=api_key)

            context_section = f"Context:\n{combined_raw}"
            history_section = ""
            if history_str:
                history_section = (
                    f"\nConversation History (for follow-up context only):\n{history_str}\n"
                )

            prompt = (
                f"You are an AI Vaidya (Ayurvedic expert). Based ONLY on the following retrieved context, "
                f"answer the user's query: '{query}'\n\n"
                f"Rules:\n"
                f"1. Answer ONLY using the provided context. Do not use outside knowledge.\n"
                f"2. Do not hallucinate.\n"
                f"3. Use Markdown formatting (bolding, bullet points) for readability.\n"
                f"4. Keep it concise, clean, and professional.\n"
                f"5. If the context does not contain the answer, state that there is no relevant information.\n"
                f"6. If this is a follow-up question, use the conversation history to understand what the user is referring to.\n\n"
                f"{context_section}"
                f"{history_section}"
            )
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            if response.text:
                answer = response.text
        except Exception as e:
            print(f"[!] Gemini API failed: {e}. Falling back to offline mode.")
            answer = None

    if not answer:
        # Fallback to offline extraction
        cleaned = _clean_text(combined_raw)
        sentences = _deduplicate_sentences(cleaned)
        formatted_bullets = _format_as_bullets(sentences)

        answer = (
            f"**Based on the Ayurvedic knowledge base:**\n\n"
            f"{formatted_bullets}"
        )

    return {
        "answer": answer,
        "sources": source_entries,
    }


# ── 5. Init on import (lazy) ──────────────────────────────────
_vectorstore_cache = None


def init():
    """Initialize the vector store (call once at app startup)."""
    global _vectorstore_cache
    if _vectorstore_cache is None:
        _vectorstore_cache = get_vectorstore()
    return _vectorstore_cache


def ask(query: str) -> dict:
    """Convenience wrapper: init + answer in one call."""
    vs = init()
    return get_answer(query, vs)


# ── CLI test ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  AI Vaidya — Offline RAG Test")
    print("=" * 60 + "\n")

    vs = init()

    test_queries = [
        "What are the three doshas in Ayurveda?",
        "How does turmeric help in healing?",
        "What is Panchakarma?",
    ]

    for q in test_queries:
        print(f"[Q] {q}")
        result = get_answer(q, vs)
        print(f"[A] Answer:\n{result['answer'][:500]}...\n")
        for s in result["sources"]:
            print(f"   [SRC] {s['file']} - Page {s['page']}")
        print("-" * 60 + "\n")
