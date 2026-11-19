
import os
from pathlib import Path
import shutil

from dotenv import load_dotenv

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DOCUMENT_FOLDER = "documents"
DATABASE_FOLDER = "database"


# ----------------------------------
# 1. LOAD DOCUMENTS
# ----------------------------------

def load_documents():

    documents = []

    folder = Path(DOCUMENT_FOLDER)

    if not folder.exists():
        raise FileNotFoundError(
            f"{DOCUMENT_FOLDER} folder does not exist."
        )

    for file_path in folder.rglob("*"):

        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            loader = PyPDFLoader(str(file_path))

        elif extension == ".docx":
            loader = Docx2txtLoader(str(file_path))

        elif extension == ".txt":
            loader = TextLoader(
                str(file_path),
                encoding="utf-8"
            )

        else:
            continue

        loaded_docs = loader.load()

        for doc in loaded_docs:
            doc.metadata["source"] = file_path.name

        documents.extend(loaded_docs)

        print(f"Loaded: {file_path.name}")

    return documents


# ----------------------------------
# 2. CREATE VECTOR DATABASE
# ----------------------------------

def create_vector_database():

    print("Reading documents...")

    documents = load_documents()

    if not documents:
        print("No supported documents found.")
        return

    print("\nTotal pages/documents:", len(documents))

    # Check extracted text
    print("\nChecking extracted text...")

    for doc in documents:

        print("\nSource:", doc.metadata.get("source"))
        print("Page:", doc.metadata.get("page"))
        print(doc.page_content[:1000])

    # ----------------------------------
    # 3. TEXT CHUNKING
    # ----------------------------------

    print("\nSplitting documents...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(documents)

    print("Total chunks:", len(chunks))

    # ----------------------------------
    # 4. INITIALIZE EMBEDDINGS
    # ----------------------------------

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in .env file"
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        api_key=api_key
    )

    # ----------------------------------
    # 5. REMOVE OLD DATABASE
    # ----------------------------------

    if os.path.exists(DATABASE_FOLDER):
        shutil.rmtree(DATABASE_FOLDER)

    # ----------------------------------
    # 6. STORE VECTORS IN CHROMA
    # ----------------------------------

    print("\nCreating Chroma vector database...")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DATABASE_FOLDER,
        collection_name="personal_documents"
    )

    print("\nVector database created successfully!")

    # ----------------------------------
    # 7. TEST RETRIEVAL
    # ----------------------------------

    print("\nTesting document retrieval...")

    test_question = "How many marks did I get in 10th Telugu?"

    results = vectorstore.similarity_search(
        test_question,
        k=5
    )

    for result in results:

        print("\nRetrieved:", result.metadata.get("source"))
        print(result.page_content)

    print("\nIngestion completed!")


if __name__ == "__main__":
    create_vector_database()
