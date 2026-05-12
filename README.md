# Job Fit Analyzer — BSAN 6200 Assignment 5, Option B
**Student:** Fong Lieu

---

## Project Description

This project builds a RAG-powered Job Fit Analyzer that compares a candidate's
resume against real job descriptions and produces structured fit analyses. The
system chunks and embeds job description text into a vector database, retrieves
relevant sections at query time, and passes them to an LLM to generate three types
of analysis: a Skill Gap Report, a Keyword Alignment table, and a Fit Summary
narrative. The pipeline is deployed as an interactive Streamlit app where a user
can select any job description, choose an analysis type, and receive results in
seconds.

---

## Setup Instructions

1. Clone the repository:

   git clone https://github.com/fonglieu/bsan6200-assignment5.git
   cd bsan6200-assignment5

2. Install dependencies:

   pip install -r requirements.txt

3. Set up your API key. Create a file called .env in the project root and add:

   OPENAI_API_KEY=your-openai-api-key-here

   Get a key at https://platform.openai.com/api-keys

4. Run the Streamlit app:

   streamlit run streamlit_app.py

5. Or open the notebook:

   notebooks/Assignment_5_LLM.ipynb

   Note: the notebook was built in Google Colab. If running locally, update
   BASE_DIR to point to your local data/ folder.

---

## Models and Tools Used

- **LLM:** OpenAI GPT-4o-mini via the OpenAI Python SDK
- **Embeddings:** ChromaDB built-in embedding model using cosine similarity
- **Vector Store:** ChromaDB (in-memory)
- **PDF Parsing:** pypdf
- **App Framework:** Streamlit
- **Language:** Python 3.12

---

## Paid vs. Free Path

This project uses the **paid path** via the OpenAI API (GPT-4o-mini).
Estimated total cost for running all analyses is under $1.00.

If you prefer the free path, you can swap the LLM for a HuggingFace Inference
API model by replacing the call_llm() function in both the notebook and the
Streamlit app with a HuggingFace Inference Client call. See the HuggingFace
docs at https://huggingface.co/docs/api-inference for setup instructions.

---

## Key Findings

- The Skill Gap Report was the most actionable output across all three target
  roles, consistently producing specific recommendations like real certifications,
  courses, and tools rather than generic advice.
- Keyword Alignment was the easiest to verify since every claim is a discrete
  table row that can be checked against the source documents directly, but it
  scored lower on actionability since it does not recommend next steps.
- Job descriptions with specific, technical requirements like Bayview Asset
  Management produced the most accurate analyses. Roles with softer or
  preference-based requirements like Goldman Sachs produced weaker results with
  some loose inferences.
- Both Goldman Sachs and Bayview Fit Summaries called the candidate a strong
  fit despite only 53% keyword match rates, pointing to a limitation in the
  fit summary prompt not being grounded in the quantitative alignment score.
- Sentence-aware chunking outperformed fixed-size chunking by preserving
  complete requirements within each chunk, which improved retrieval quality
  across all analyses.

---

## File Descriptions

| File | Description |
|---|---|
| streamlit_app.py | Streamlit web app for running live job fit analyses |
| requirements.txt | All Python dependencies needed to run the project |
| env.example | Template for setting up your API key |
| .gitignore | Excludes API keys and cache files from version control |
| memo.md | Technical memo addressed to a hiring manager describing the system, results, and recommendations |
| ai_log.md | Log of all AI tool usage throughout the project with dates, prompts, and modifications |
| notebooks/Assignment_5_LLM.ipynb | Full RAG pipeline notebook including data loading, chunking, embedding, analysis, prompt iterations, zero-shot vs few-shot comparison, and evaluation |
| data/jd_metadata.csv | Metadata for all 10 job descriptions including company, title, source URL, and date collected |
| data/Fong_Lieu_Resume.pdf | Resume used as the candidate document for all analyses |
| data/jd_01_amend_sales_analyst.txt | AMEND Consulting — Sales Analyst job description |
| data/jd_02_att_strategy_analyst.txt | AT&T — Strategy Analyst job description |
| data/jd_03_spotify_data_analyst.txt | Spotify — Data Analyst II job description |
| data/jd_04_delta_data_analyst.txt | Delta Air Lines — Senior Analyst job description |
| data/jd_05_northrop_grumman_data_analyst.txt | Northrop Grumman — Data Insight Analyst job description |
| data/jd_06_transformlabs_business_analyst.txt | Transform Labs — Business Analyst job description |
| data/jd_07_qualifiedhealth_product_intern.txt | Qualified Health — Product Intern job description |
| data/jd_08_capgemini_junior_ba.txt | Capgemini — Junior Business Analyst job description |
| data/jd_09_bayview_data_ops_analyst.txt | Bayview Asset Management — Data Operations Analyst job description |
| data/jd_10_goldmansachs_data_office_analyst.txt | Goldman Sachs — Data Office Analyst job description |
| evaluation/test_results.md | Evaluation table and analysis for all 9 analyses across the top 3 target roles |
