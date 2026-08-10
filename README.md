# 📄 RAG PDF Chatbot

A highly efficient, end-to-end Retrieval-Augmented Generation (RAG) application that allows users to upload and converse with any PDF document seamlessly. 

Designed with a focus on clean architecture, this application utilizes **LangChain** for robust LCEL (LangChain Expression Language) pipelines, **in-memory document processing** for privacy and speed, and **multi-provider LLM fallbacks** for high availability.

## ✨ Features

* **In-Memory Processing:** PDFs are processed directly in RAM using `BytesIO` and `pypdf`, ensuring zero leftover files on disk and enhanced data privacy.
* **Intelligent Routing & Fallbacks:** Engineered with LangChain's fallback mechanisms, dynamically routing requests from Groq's high-speed models to Google's Gemini API in case of rate limits or service disruptions.
* **Side-by-Side UI:** A responsive Streamlit interface featuring a 70/30 split—allowing users to read the document preview and interact with the chatbot simultaneously without switching tabs.
* **Conversational Memory:** Maintains full chat history within the session state for natural, multi-turn interactions.
* **Local Vector Retrieval:** Utilizes HuggingFace's lightweight embedding models (`all-MiniLM-L6-v2`) and FAISS for fast, local semantic search.

---

## 📸 Screenshots

### 1. Home / Upload Screen
*(Upload your PDF securely. No data is saved to disk.)*
<img width="957" height="417" alt="image" src="https://github.com/user-attachments/assets/0ef58bb6-7646-471c-8ca4-1437560cbea8" />


### 2. Chat Interface & Document Preview
*(Chat window alongside the interactive PDF viewer.)*
![Chat Interface](docs/images/placeholder_chat.png)

---

## 🛠️ Tech Stack

* **UI Framework:** [Streamlit](https://streamlit.io/)
* **Orchestration:** [LangChain](https://www.langchain.com/) (LCEL)
* **LLMs:** Groq (`gpt-oss-120b`), Google Gemini (`gemini-3.5-flash`)
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **Vector Store:** [FAISS](https://faiss.ai/) (Facebook AI Similarity Search)
* **PDF Processing:** `pypdf`, `streamlit-pdf-viewer`

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/pdf-chatbot-rag.git
cd pdf-chatbot-rag
```

### 2. Set up a virtual environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.streamlit` folder in the root directory and add a `secrets.toml` file to securely store your API keys.

```bash
mkdir .streamlit
touch .streamlit/secrets.toml
```

Add the following keys to your `secrets.toml` (make sure `.streamlit/` is in your `.gitignore`!):
```toml
GROQ_API_KEY = "your_groq_api_key_here"
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 🧠 Architecture Overview
1. **Document Ingestion:** User uploads a PDF. The file stream is passed directly into memory.
2. **Chunking & Embedding:** The text is extracted, split using a `SemanticChunker`, and embedded locally using HuggingFace sentence transformers.
3. **Indexing:** The vector embeddings are stored in a temporary FAISS index linked to the session state.
4. **Retrieval & Generation:** User queries trigger a similarity search in FAISS. The relevant chunks are piped into a ChatPromptTemplate alongside the user's query, routed to Groq (or Gemini via fallback), and returned as a streamed string via `StrOutputParser`.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/YOUR_USERNAME/pdf-chatbot-rag/issues).
