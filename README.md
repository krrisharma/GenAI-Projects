# 🎥 YouTube Chatbot (RAG + LangChain + Groq)

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about any YouTube video using its transcript.

Instead of relying on the LLM's memory, the chatbot retrieves relevant transcript chunks using FAISS vector search and generates answers grounded in the video's content.

---

## Features

- Paste any YouTube URL or Video ID
- Automatically fetches transcript
- Creates embeddings using HuggingFace BGE
- Stores embeddings in FAISS
- Retrieves relevant transcript chunks
- Answers questions using Groq Llama 3.3 70B
- Refuses to hallucinate outside transcript context
- Streamlit web interface

---

## Tech Stack

- Python
- LangChain
- HuggingFace Embeddings
- FAISS
- Groq API
- Streamlit
- YouTube Transcript API

---

## Architecture

```
YouTube Video
      │
      ▼
Transcript Extraction
      │
      ▼
Text Splitting
      │
      ▼
HuggingFace Embeddings
      │
      ▼
FAISS Vector Database
      │
      ▼
Retriever
      │
      ▼
Prompt Template
      │
      ▼
Groq Llama 3.3 70B
      │
      ▼
Answer
```

---

## Installation

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env`

```
GROQ_API_KEY=your_groq_api_key
```

Run

```bash
streamlit run app.py
```

---

## Example Questions

- What are the speaker's views on reinforcement learning?
- Why does the speaker think current AI is different from humans?
- What examples does the speaker use?
- What concerns does the speaker have about AI?
- Give me 5 key takeaways.

---

## Project Structure

```
app.py
chatbot.py
requirements.txt
README.md
.env.example
```

---

## Future Improvements

- Chat history memory
- PDF export
- Timestamp citations
- Multi-video RAG
- Multiple embedding models
- YouTube playlist support
- Hybrid search
- Source chunk display

---

## License

MIT License
