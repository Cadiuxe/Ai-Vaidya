"""
AI Vaidya — Flask API
Wraps rag.py to expose a REST API for the React frontend.
Run with:  python api.py
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from rag import init, get_answer

app = Flask(__name__)
CORS(app)

# Load vector store once at startup
print("[API] Loading Ayurveda knowledge base...")
vectorstore = init()
print("[API] Knowledge base ready!\n")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat queries from the React frontend."""
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Get chat context if provided (for follow-up questions)
    chat_context = data.get("chat_context", [])

    try:
        result = get_answer(query, vectorstore, chat_context=chat_context)
        chakras = result.get("chakras", [])
        print(f"[API] Query: {query[:50]}, Chakras: {len(chakras)} items, Answer: {len(result.get('answer',''))} chars")
        return jsonify({
            "answer": result["answer"],
            "sources": result["sources"],
            "chakras": chakras,
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[!] Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "AI Vaidya API is running"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
