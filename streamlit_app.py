"""
Job Fit Analyzer -- Streamlit App
BSAN 6200: Text Mining & Social Media Analytics | Spring 2026
Student: Fong Lieu

Run with: streamlit run streamlit_app.py

Setup:
    pip install streamlit openai pypdf pandas chromadb sentence-transformers python-dotenv

    Create .env file with:
        OPENAI_API_KEY=your-key-here

    Place your data files in a folder called data/ next to this file:
        data/
            jd_metadata.csv
            jd_01_amend_sales_analyst.txt
            jd_02_att_strategy_analyst.txt
            ... (all 10 JD .txt files)
            Fong_Lieu_Resume.pdf
"""

import os
import re
import pandas as pd
from pypdf import PdfReader
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv(dotenv_path="env.txt")

st.set_page_config(
    page_title="Job Fit Analyzer",
    page_icon="📄",
    layout="wide"
)

# ── Config ──
DATA_DIR = "data"
MODEL_ID = "gpt-4o-mini"


# ══════════════════════════════════════════
# Pipeline functions (from notebook)
# ══════════════════════════════════════════

def load_text_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf(filepath):
    reader = PdfReader(filepath)
    return "\n".join([
        page.extract_text() for page in reader.pages
        if page.extract_text()
    ])


def chunk_text_by_sentences(text, chunk_size=600, overlap=75):
    """Sentence-aware chunking (Strategy 2 from notebook)."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            words = current_chunk.split()
            overlap_text = " ".join(words[-10:]) if len(words) > 10 else current_chunk
            current_chunk = overlap_text + " " + sentence
        else:
            current_chunk += (" " if current_chunk else "") + sentence
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks


def search(collection, query, k=3):
    """Search the vector store and return top-k results with metadata."""
    results = collection.query(query_texts=[query], n_results=k)
    docs      = results["documents"][0]
    sources   = [m["source"]  for m in results["metadatas"][0]]
    companies = [m["company"] for m in results["metadatas"][0]]
    distances = results["distances"][0]
    return list(zip(docs, sources, companies, distances))


def call_llm(client, prompt):
    """Send a prompt to OpenAI and return the response text."""
    response = client.chat.completions.create(
        model=MODEL_ID,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def skill_gap_report(client, jd_text, resume_text):
    prompt = f"""
You are a career coach analyzing a candidate's resume against a job description.

JOB DESCRIPTION:
{jd_text}

CANDIDATE RESUME:
{resume_text}

Produce a structured Skill Gap Report with exactly three sections:

MATCHING SKILLS:
- List each skill or experience the candidate has that directly matches a JD requirement.
- Be specific, citing evidence from the resume (tool name, project, or role).

MISSING SKILLS:
- List each requirement from the JD that is absent or insufficiently demonstrated in the resume.
- Be specific about what is missing.

RECOMMENDED ACTIONS:
- For each missing skill, provide one concrete, actionable step the candidate can take
  (e.g., specific course, project idea, certification, or tool to learn).

Use bullet points. Be concise and factual. Do not invent skills not present in either document.
"""
    return call_llm(client, prompt)


def keyword_alignment(client, jd_text, resume_text):
    prompt = f"""
You are a resume keyword analyst.

JOB DESCRIPTION:
{jd_text}

CANDIDATE RESUME:
{resume_text}

Step 1 — Extract the 15 most important keywords and phrases from the job description
(focus on required skills, tools, technologies, and domain terms).

Step 2 — For each keyword, determine if it appears or is semantically equivalent in the resume.
Mark each as: MATCH, PARTIAL MATCH, or MISSING.

Step 3 — Calculate: match rate = (MATCH + 0.5 * PARTIAL MATCH) / 15

Output format:

KEYWORD TABLE:
| Keyword | Status | Evidence from Resume |
|---------|--------|----------------------|
...

MATCH RATE: X%

SUMMARY: One sentence interpreting the match rate and what it means for this application.
"""
    return call_llm(client, prompt)


def fit_summary(client, jd_text, resume_text):
    prompt = f"""
You are a hiring consultant writing a brief fit assessment.

JOB DESCRIPTION:
{jd_text}

CANDIDATE RESUME:
{resume_text}

Write a 3-4 sentence narrative Fit Summary assessing how well this candidate fits the role.

- Sentence 1: State overall fit level (Strong / Moderate / Weak) and primary reason,
  citing specific evidence from both documents.
- Sentence 2: Highlight the candidate's single strongest relevant qualification for this role.
- Sentence 3: Identify the most significant gap between the candidate and the role's requirements.
- Sentence 4 (optional): One specific recommendation to strengthen the application.

Be direct and evidence-based. Do not use filler phrases.
Only reference information present in the documents provided.
"""
    return call_llm(client, prompt)


# ══════════════════════════════════════════
# Cached resource loaders
# ══════════════════════════════════════════

@st.cache_resource
def load_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        st.error("OPENAI_API_KEY not found. Add it to your .env file.")
        st.stop()
    return OpenAI(api_key=api_key)


@st.cache_data
def load_metadata():
    path = os.path.join(DATA_DIR, "jd_metadata.csv")
    if not os.path.exists(path):
        st.error(f"jd_metadata.csv not found in {DATA_DIR}/")
        st.stop()
    return pd.read_csv(path)


@st.cache_resource
def load_pipeline():
    """Load JDs, resume, build vector store. Runs once and caches."""
    metadata_df = load_metadata()

    # Load JD documents
    jd_docs = {}
    for _, row in metadata_df.iterrows():
        filepath = os.path.join(DATA_DIR, row["filename"])
        if os.path.exists(filepath):
            jd_docs[row["filename"]] = {
                "text":    load_text_file(filepath),
                "company": row["company"],
                "title":   row["title"],
            }

    # Load resume
    resume_path = os.path.join(DATA_DIR, "Fong_Lieu_Resume.pdf")
    if not os.path.exists(resume_path):
        st.error("Fong_Lieu_Resume.pdf not found in data/")
        st.stop()
    resume_text = load_pdf(resume_path)

    # Build chunks
    all_chunks = []
    for filename, doc in jd_docs.items():
        for chunk in chunk_text_by_sentences(doc["text"], chunk_size=600, overlap=75):
            all_chunks.append({
                "text":    chunk,
                "source":  filename,
                "company": doc["company"]
            })
    for chunk in chunk_text_by_sentences(resume_text, chunk_size=600, overlap=75):
        all_chunks.append({
            "text":    chunk,
            "source":  "Fong_Lieu_Resume.pdf",
            "company": "resume"
        })

    # Build ChromaDB vector store
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(
        name="job_fit_analyzer",
        metadata={"hnsw:space": "cosine"}
    )
    if collection.count() == 0:
        collection.add(
            documents=[c["text"]    for c in all_chunks],
            metadatas=[{"source": c["source"], "company": c["company"]} for c in all_chunks],
            ids=[f"chunk_{i}"       for i in range(len(all_chunks))]
        )

    return jd_docs, resume_text, collection


# ══════════════════════════════════════════
# UI
# ══════════════════════════════════════════

openai_client = load_openai_client()
metadata_df   = load_metadata()
jd_docs, resume_text, collection = load_pipeline()

# ── Sidebar ──
with st.sidebar:
    st.title("📄 Job Fit Analyzer")
    st.write(
        "This app compares your resume against real job descriptions "
        "using a RAG pipeline and GPT-4o-mini."
    )
    st.divider()
    st.write(f"**JDs loaded:** {len(jd_docs)}")
    st.write(f"**Resume loaded:** Fong_Lieu_Resume.pdf")
    st.write(f"**Model:** {MODEL_ID}")
    st.divider()
    st.write("**How to use:**")
    st.write("1. Select a job description")
    st.write("2. Choose an analysis type")
    st.write("3. Click Run Analysis")
    st.caption("BSAN 6200 | Spring 2026 | Fong Lieu")

# ── Main layout ──
st.title("Job Fit Analyzer")
st.caption("Compare your resume against job descriptions using RAG + GPT-4o-mini.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Select a Job Description")

    # Build display labels for the dropdown
    jd_options = {}
    for _, row in metadata_df.iterrows():
        if row["filename"] in jd_docs:
            label = f"{row['company']} — {row['title']}"
            jd_options[label] = row["filename"]

    selected_label    = st.selectbox("Choose a JD:", list(jd_options.keys()))
    selected_filename = jd_options[selected_label]
    selected_jd_text  = jd_docs[selected_filename]["text"]

    with st.expander("Preview JD"):
        st.text(selected_jd_text[:800] + "..." if len(selected_jd_text) > 800 else selected_jd_text)

with col2:
    st.subheader("2. Choose Analysis Type")
    analysis_type = st.radio(
        "Select one:",
        ["Skill Gap Report", "Keyword Alignment", "Fit Summary"],
        help=(
            "Skill Gap Report: matching skills, missing skills, and actions to close gaps.\n\n"
            "Keyword Alignment: extracts 15 key terms from the JD and scores how many appear in your resume.\n\n"
            "Fit Summary: 3-4 sentence narrative assessment of overall fit."
        )
    )

st.divider()

# ── Run analysis ──
run_button = st.button("Run Analysis", type="primary", use_container_width=True)

if run_button:
    with st.spinner(f"Running {analysis_type} for {jd_docs[selected_filename]['company']}..."):
        try:
            if analysis_type == "Skill Gap Report":
                result = skill_gap_report(openai_client, selected_jd_text, resume_text)
            elif analysis_type == "Keyword Alignment":
                result = keyword_alignment(openai_client, selected_jd_text, resume_text)
            else:
                result = fit_summary(openai_client, selected_jd_text, resume_text)

            st.subheader(f"Results: {analysis_type}")
            st.caption(f"{jd_docs[selected_filename]['company']} — {jd_docs[selected_filename]['title']}")

            # Side-by-side view: results on left, retrieved chunks on right
            res_col, chunk_col = st.columns([3, 2])

            with res_col:
                st.markdown(result)

            with chunk_col:
                with st.expander("Retrieved JD chunks used", expanded=True):
                    retrieved = search(collection, selected_jd_text[:500], k=3)
                    for i, (text, source, company, dist) in enumerate(retrieved):
                        st.markdown(f"**Chunk {i+1}** ({company}) — distance: {dist:.3f}")
                        st.caption(text[:300] + "..." if len(text) > 300 else text)
                        st.divider()

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
