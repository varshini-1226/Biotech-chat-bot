import sqlite3
import os
from groq import Groq
from Bio import Entrez

DB_PATH = "biotech_chatbot.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT,
        answer TEXT
    )
    """)

    conn.commit()
    conn.close()



init_db()

# Required by NCBI
Entrez.email = "dolavarshinipriya@gmail.com"

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_llm(question: str) -> str:
    prompt = f"""
You are a biotechnology assistant.
Answer clearly and simply for a student.

Question: {question}
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def normalize(text: str) -> str:
    return text.lower().strip()


# 🔬 NEW: Fetch MeSH definition
def get_mesh_definition(term):
    try:
        search_handle = Entrez.esearch(db="mesh", term=term, retmax=1)
        search_record = Entrez.read(search_handle)
        search_handle.close()

        if not search_record["IdList"]:
            return None

        mesh_id = search_record["IdList"][0]

        fetch_handle = Entrez.efetch(db="mesh", id=mesh_id, retmode="xml")
        records = Entrez.read(fetch_handle)
        fetch_handle.close()

        descriptor = records[0]["DescriptorRecord"]
        name = descriptor["DescriptorName"]["String"]
        definition = descriptor.get("ScopeNote", "No definition available.")

        return f"🔬 MeSH Definition:\n\n{name}: {definition}"

    except Exception:
        return None


def get_answer(question: str) -> str:
    q = normalize(question)

    # Intent words → go to AI directly
    intent_words = [
        "methods", "types", "procedure", "process",
        "explain", "steps", "how", "techniques"
    ]

    if any(word in q for word in intent_words):
        return ask_llm(question)

    # 1️⃣ Check local database first
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT keyword, answer FROM faq")
    rows = cur.fetchall()
    conn.close()

    for keyword, answer in rows:
        k = normalize(keyword)
        if q == k or q.startswith(k):
            return answer

    # 2️⃣ Check MeSH (NCBI)
    mesh_result = get_mesh_definition(question)
    if mesh_result:
        return mesh_result

    # 3️⃣ Fallback to LLM
    return ask_llm(question)