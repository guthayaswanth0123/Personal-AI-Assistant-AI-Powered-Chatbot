
import os
from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ----------------------------------
# 1. API CONFIGURATION
# ----------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# ----------------------------------
# 2. INITIALIZE GEMINI
# ----------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=api_key
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    api_key=api_key
)


# ----------------------------------
# 3. LOAD VECTOR DATABASE
# ----------------------------------

vectorstore = Chroma(
    collection_name="personal_documents",
    persist_directory="database",
    embedding_function=embeddings
)


# ----------------------------------
# 4. EXTRACT TEXT FROM GEMINI
# ----------------------------------

def extract_text(response):

    content = response.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))

            elif isinstance(item, str):
                text_parts.append(item)

        return "\n".join(text_parts).strip()

    return str(content).strip()


# ----------------------------------
# 5. CLASSIFY USER QUESTION
# ----------------------------------

def classify_question(question):

    prompt = f"""
    You are a question classification assistant.

    Classify the user's question into exactly one category.

    PERSONAL:
    Questions about the user's own information,
    education, marks, CGPA, skills, projects,
    experience, resume, certificates and personal documents.

    GENERAL:
    Questions about programming, Python, Java,
    artificial intelligence, machine learning,
    mathematics, science, technology and other
    general knowledge topics.

    If the question asks about the user's personal
    information, classify it as PERSONAL.

    If the question asks for an explanation or
    general knowledge, classify it as GENERAL.

    Return ONLY one word:
    PERSONAL or GENERAL.

    Question: {question}

    Category:
    """

    response = llm.invoke(prompt)

    result = extract_text(response).upper()

    if "PERSONAL" in result:
        return "PERSONAL"

    return "GENERAL"


# ----------------------------------
# 6. ANSWER PERSONAL QUESTIONS USING RAG
# ----------------------------------

def answer_personal_question(question):

    print("\nSearching personal documents...")

    results = vectorstore.similarity_search_with_relevance_scores(
        question,
        k=8
    )

    if not results:
        return "I couldn't find this information in your documents."

    # Print retrieval results for debugging
    for doc, score in results:

        print("\nSource:", doc.metadata.get("source"))
        print("Relevance score:", score)
        print("Content:", doc.page_content)

    # Prepare retrieved context
    context = "\n\n".join(
        doc.page_content for doc, score in results
    )

    prompt = ChatPromptTemplate.from_template("""
    You are a personal AI assistant.

    Answer the user's question using ONLY the
    information available in the provided documents.

    Instructions:

    1. Carefully examine all the retrieved context.
    2. Match names, subject names, marks, grades,
       percentages, dates and other details.
    3. Understand different ways of asking the
       same question.
    4. If the answer is present, provide it directly.
    5. Never invent personal information.
    6. If the answer is not available in the context,
       say:
       "I couldn't find this information in your documents."
    7. Give a clear and natural answer.

    Context:
    {context}

    User Question:
    {question}

    Answer:
    """)

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return extract_text(response)


# ----------------------------------
# 7. ANSWER GENERAL QUESTIONS USING GEMINI
# ----------------------------------

def answer_general_question(question):

    print("\nAnswering general question using Gemini...")

    response = llm.invoke(question)

    return extract_text(response)


# ----------------------------------
# 8. MAIN CHATBOT FUNCTION
# ----------------------------------

def ask_question(question):

    if not question or not question.strip():
        return "Please enter a question."

    print("\nUser Question:", question)

    # Classify question
    category = classify_question(question)

    print("Question Category:", category)

    # Route to the correct answering system
    if category == "PERSONAL":

        answer = answer_personal_question(question)

    else:

        answer = answer_general_question(question)

    return answer
