# 🤖 Personal AI Assistant – AI-Powered Chatbot

An AI-powered chatbot built using **Python, Streamlit, LangChain, Google Gemini and ChromaDB**. It allows users to ask questions about their personal documents as well as general topics such as Python, Artificial Intelligence, Machine Learning and other technical concepts.

The project uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from uploaded documents and generate accurate, context-aware responses using Google Gemini.

## 🚀 Features

- **Personal Document Q&A:** Ask questions about personal information, education, academic marks, skills, projects, experience and certificates.
- **RAG-Based Question Answering:** Retrieves relevant information from documents using semantic similarity search.
- **Multiple Document Support:** Supports PDF, DOCX and TXT files.
- **Intelligent Question Classification:** Automatically identifies whether a question is personal or general.
- **General Knowledge Assistance:** Answers general questions directly using Google Gemini.
- **Vector Database Integration:** Stores document embeddings in ChromaDB for efficient retrieval.
- **Interactive Chat Interface:** Provides a conversational interface using Streamlit.
- **Chat History:** Maintains conversation messages during the application session.
- **Clear Chat Option:** Allows users to clear previous conversations.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Streamlit | Interactive chatbot interface |
| LangChain | LLM integration and RAG workflow |
| Google Gemini 2.5 Flash | Question classification and response generation |
| Gemini Embeddings | Converts text into vector representations |
| ChromaDB | Stores and retrieves document embeddings |
| PyPDF | Extracts text from PDF documents |
| Docx2txt | Extracts text from Word documents |
| Python-dotenv | Manages environment variables |

## 🏗️ Project Architecture

The project consists of three main Python files.

```text
Personal-AI-Assistant/
│
├── app.py                  # Streamlit user interface
├── chatbot.py              # Chatbot logic and RAG implementation
├── ingest.py               # Document processing and ingestion
│
├── documents/              # Personal documents
│   ├── education.pdf
│   ├── resume.pdf
│   └── certificates.pdf
│
├── database/               # ChromaDB vector database
│
├── .env                    # Gemini API key
├── .gitignore
└── requirements.txt
```

## ⚙️ How It Works

The application follows two major workflows.

### 1. Document Ingestion Workflow

The ingestion process converts personal documents into searchable vector embeddings.

**Steps:**

1. **Document Loading:** Loads PDF, DOCX and TXT files from the documents folder.
2. **Text Extraction:** Extracts readable text from the uploaded documents.
3. **Text Chunking:** Splits large documents into smaller chunks using RecursiveCharacterTextSplitter.
4. **Embedding Generation:** Converts each text chunk into numerical vector representations using Google's embedding model.
5. **Vector Storage:** Stores the embeddings and associated document metadata in ChromaDB.

**Chunking configuration:**
- Chunk size: 1200 characters.
- Chunk overlap: 200 characters.

This overlap helps preserve contextual information between consecutive chunks.

### 2. Question-Answering Workflow

When a user enters a question, the chatbot follows these steps:

1. **User Input:** Receives a question through the Streamlit chat interface.
2. **Question Classification:** Uses Gemini to classify the question into PERSONAL or GENERAL.
3. **Query Routing:** Routes the question to the appropriate answering function.

**For PERSONAL questions:**

- Searches the ChromaDB vector database.
- Retrieves the top 8 relevant document chunks.
- Combines the retrieved information into context.
- Sends the question and context to Gemini.
- Generates an answer based only on the retrieved document information.

**For GENERAL questions:**

- Sends the question directly to Google Gemini.
- Generates a response without searching personal documents.

4. **Response Generation:** Returns the generated response to the Streamlit interface.
5. **Chat History:** Displays and maintains the conversation during the session.

## 🔄 Architecture Flow

```text
             User Question
                   |
                   v
            Streamlit App
                   |
                   v
          Question Classification
                   |
            +------+------+
            |             |
            v             v
         PERSONAL       GENERAL
            |             |
            v             v
       ChromaDB        Google Gemini
       Similarity      Direct Query
        Search             |
            |              |
            v              |
      Retrieve Top 8       |
      Relevant Chunks      |
            |              |
            v              |
      Context + Query      |
            |              |
            v              |
       Google Gemini       |
            |              |
            +------+-------+
                   |
                   v
             Final Answer
                   |
                   v
             Streamlit UI
```

## 🧠 Key AI Concepts Implemented

### 1. Retrieval-Augmented Generation (RAG)

RAG combines information retrieval with generative AI.

Instead of relying only on the LLM's pretrained knowledge, the system retrieves relevant information from external documents and provides it as context to the LLM.

**RAG consists of three major steps:**

- Retrieval – Finds relevant document chunks.
- Augmentation – Adds retrieved information to the prompt.
- Generation – Uses the LLM to generate the final response.

### 2. Embeddings

Embeddings convert text into numerical vectors that represent semantic meaning.

They help identify documents that are conceptually similar to a user's question, even when the exact words are different.

### 3. Vector Database

ChromaDB stores document embeddings and enables similarity-based retrieval.

The chatbot uses these embeddings to find relevant information from personal documents.

### 4. Semantic Similarity Search

The system compares the question embedding with stored document embeddings and retrieves the most relevant chunks.

### 5. Question Classification

Gemini classifies incoming questions into two categories:

- PERSONAL – Questions related to personal documents.
- GENERAL – Questions related to general knowledge and technical concepts.

This allows the chatbot to use different answering strategies depending on the question.

## 💻 Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/guthayaswanth0123/Personal-AI-Assistant-AI-Powered-Chatbot.git

cd Personal-AI-Assistant-AI-Powered-Chatbot
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Gemini API Key

Create a `.env` file in the project root directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Get an API key from:

https://aistudio.google.com/apikey

### Step 5: Add Personal Documents

Create a folder named `documents` in the project directory.

Add your personal PDF, DOCX or TXT documents.

### Step 6: Run Document Ingestion

Execute:

```bash
python ingest.py
```

This processes the documents, generates embeddings and stores them in the ChromaDB database.

Run ingestion again whenever you add or update documents.

### Step 7: Launch the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📦 Requirements

Create a `requirements.txt` file with the following dependencies:

```text
streamlit
python-dotenv
langchain
langchain-core
langchain-community
langchain-google-genai
langchain-chroma
langchain-text-splitters
chromadb
pypdf
docx2txt
```

Install them using:

```bash
pip install -r requirements.txt
```

## 🧪 Example Questions

**Personal Questions:**
- What is my 10th class school name?
- What marks did I get in Telugu?
- What are my technical skills?
- Explain my academic projects.
- What is my educational qualification?

**General Questions:**
- What is Artificial Intelligence?
- Explain Python decorators.
- What is Retrieval-Augmented Generation?
- Explain machine learning algorithms.
- What are embeddings in AI?

## 🔮 Future Enhancements

- Support for Excel, CSV and PowerPoint documents.
- Conversation-aware question answering.
- Improved document retrieval using hybrid search.
- Metadata filtering for more accurate retrieval.
- Source citations showing which document contains the answer.
- Document upload functionality directly through Streamlit.
- Improved error handling and API rate-limit management.
- Support for multiple LLM providers.
- Deployment using Streamlit Community Cloud.

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Building LLM-powered applications using Python.
- Implementing Retrieval-Augmented Generation (RAG).
- Working with Google Gemini APIs.
- Generating and storing vector embeddings.
- Integrating LangChain with ChromaDB.
- Implementing semantic search and document retrieval.
- Building interactive applications using Streamlit.
- Designing AI-based question classification and routing workflows.

## 👨‍💻 Author

**Gutha Yaswanth**

GitHub: https://github.com/guthayaswanth0123

---

**Project:** Personal AI Assistant – AI-Powered Chatbot

**Domain:** Artificial Intelligence | Generative AI | Large Language Models | RAG