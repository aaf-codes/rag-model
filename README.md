📚 RAG Citation Assistant

An AI-powered RAG (Retrieval-Augmented Generation) research assistant that enables users to upload multiple research papers, perform semantic search using vector embeddings, and generate AI-based related work summaries with citation-aware retrieval and research evidence visualization.

## ✨ Features
- **Upload Research Papers:** Support for uploading multiple PDF documents simultaneously.
- **Semantic Search:** Uses advanced vector embeddings to find exactly what you need across all uploaded papers.
- **AI-Powered Summaries:** Generates related work summaries and answers research queries using context retrieved directly from your documents.
- **Citation-Aware:** Provides clear citations pointing back to the specific papers and sections where the information was found.
- **Evidence Visualization:** Displays the extracted context to ensure transparency and accuracy.

## 🛠️ Technology Stack
### Backend
- **FastAPI:** High-performance web framework for the API.
- **LangChain:** Framework for developing applications powered by LLMs.
- **ChromaDB:** Open-source vector database for storing and querying embeddings.
- **OpenAI:** Used for generating embeddings and AI completions.
- **PyPDF / PyMuPDF:** For robust parsing and extraction of text from PDF documents.

### Frontend
- **Vanilla HTML/CSS/JS:** Lightweight, fast, and responsive user interface without the overhead of heavy frameworks.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- OpenAI API Key

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend` directory and add your API keys (e.g., `OPENAI_API_KEY=your_key_here`).
5. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Simply open `frontend/index.html` in your favorite web browser. 
   *(Alternatively, you can serve it using a local static server like Live Server in VS Code or python's `http.server`.)*

## 🤝 Contributing
Contributions are always welcome! Feel free to open an issue or submit a pull request if you have ideas for improvements or new features.
