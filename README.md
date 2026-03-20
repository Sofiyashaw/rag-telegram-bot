# 🤖 RAG Telegram Bot

A Retrieval-Augmented Generation (RAG) chatbot built using:

* Telegram Bot API
* FAISS (vector search)
* Sentence Transformers (embeddings)
* Ollama (LLM inference)

---

## 🚀 Features

* Ask questions from your custom documents
* Context-aware answers using RAG
* Conversation memory (last 3 interactions)
* Response summarization
* Caching for faster responses

---

## 🧠 Models & APIs Used

* Embedding Model: `all-MiniLM-L6-v2`
* Vector DB: FAISS
* LLM: LLaMA3 via Ollama
* API: Telegram Bot API

---

## 📦 How to Run Locally

### 1. Clone repo

```bash
git clone https://github.com/your-username/rag-telegram-bot.git
cd rag-telegram-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Ollama

```bash
ollama run llama3
```

### 4. Set environment variable

```bash
export TELEGRAM_TOKEN=your_token_here   # Mac/Linux
set TELEGRAM_TOKEN=your_token_here      # Windows
```

### 5. Run bot

```bash
python app.py
```

---

## 🐳 (Optional) Docker Setup

```bash
docker-compose up --build
```

---

## 🧱 System Design

User → Telegram Bot → Retriever (FAISS) → Context
→ Generator (Ollama LLM) → Response → User

---

## 📸 Demo

See `/screenshots` folder.

---

## 📌 Commands

* `/start` → Start bot
* `/ask <question>` → Ask question
* `/summarize` → Summarize last answer

---

## ⚠️ Notes

* Make sure Ollama is running locally
* Add your documents inside `/data`
* Token should NOT be hardcoded

---

## 👩‍💻 Author

Sofiya
