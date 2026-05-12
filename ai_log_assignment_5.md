# AI Usage Log — Assignment 5: Job Fit Analyzer

**Name:** Fong Lieu

\---

**Tool:** Claude

**Task:** I wanted to understand how LangChain works before deciding whether to use it.

**Prompt used:**

> "Can you explain how LangChain works and how it connects to LLMs?"

**What AI suggested:**
AI explained that LangChain is a framework that chains together components like document loaders, text splitters, embedding models, vector stores, and LLM calls into a single pipeline using built-in abstractions like RetrievalQA and PromptTemplate.

**What I used:**
I read through the explanation but ultimately did not use LangChain. Loading documents with plain Python file and calling OpenAI directly was simpler and easier to debug. 

**What I modified:**
I replaced all LangChain components with native Python and the OpenAI SDK directly.

**Why I modified it:**
The professor confirmed LangChain was no longer required, and the direct approach matched the RAG notebook structure more closely.

**What I learned:**
LangChain is useful for production pipelines but adds unnecessary complexity for a project of this scope. Understanding it helped me appreciate what each step in the RAG pipeline actually does under the hood.

**AI errors found:**
None.

\---

**Tool:** Claude

**Task:** I needed to understand what chunk size and overlap do before deciding on final settings.

**Prompt used:**

> "What does chunk size do in text chunking and how does changing it affect retrieval quality?"

**What AI suggested:**
AI explained that chunk size controls how many characters are in each segment. Smaller chunks are more granular but risk cutting sentences mid-thought. Larger chunks preserve more context but may dilute the relevance of a retrieval result. Overlap helps maintain continuity across chunk boundaries.

**What I used:**
I used this to justify changing from the professor's default of 300 characters to 600. At 300, the fixed-size splitter was cutting job description requirements mid-sentence. At 600, chunks captured full requirement sections.

**What I modified:**
I updated both chunking functions to use chunk\_size=600 and overlap=75 instead of 300/50.

**Why I modified it:**
The comparison table showed Strategy 1 at 300 produced a minimum chunk size of 33 characters, which confirmed fragments were being created. 600 produced a minimum of 220 characters with complete sentences throughout.

**What I learned:**
Chunk size should be chosen based on the natural structure of the documents being chunked, not a fixed default.

**AI errors found:**
None.

\---

**Tool:** Claude

**Task:** I needed to set up an OpenAI API key to run the LLM calls.

**Prompt used:**

> "How do I get an OpenAI API key and use it in Python?"

**What AI suggested:**
AI walked me through creating an account at platform.openai.com, navigating to the API keys section, generating a new key, and loading it in Python using os.environ and python-dotenv.

**What I used:**
I followed the instructions and created a key. I also had to add credits to my account since the free tier did not include API access. Total cost for the full assignment was under $1.00.

**What I modified:**
Nothing. I followed the setup exactly as described.

**What I learned:**
OpenAI requires a paid credit balance even for low-volume use. The gpt-4o-mini model is cheap enough that $5 of credits covers hundreds of analyses.

**AI errors found:**
None.

\---

**Tool:** Claude

**Task:** I wanted to store my API key securely without pasting it directly into the notebook.

**Prompt used:**

> "How do I use my OpenAI API key in a Colab notebook?"

**What AI suggested:**
AI suggested two options: using Google Colab's built-in Secrets manager (the key icon in the sidebar) with userdata.get(), or storing the key in a .env file and loading it with python-dotenv.

**What I used:**
I used the Colab Secrets approach for the notebook and a .env file for the Streamlit app.

**What I modified:**
For the Streamlit app I ended up needing to specify the dotenv path explicitly using load\_dotenv(dotenv\_path=".env") because the default load\_dotenv() was not finding the file in my local directory.

**Why I modified it:**
The default behavior assumed a specific file location that did not match where my file was saved.

**What I learned:**
Never paste API keys directly into a notebook or commit them to GitHub. Colab Secrets is the cleanest solution for notebooks and .env files work well for local apps.

**AI errors found:**
None.

\---

**Tool:** Claude

**Task:** I needed to choose between ChromaDB and FAISS for my vector store.

**Prompt used:**

> "What is the difference between ChromaDB and FAISS for a RAG pipeline? Which should I use?"

**What AI suggested:**
AI explained that FAISS is a pure similarity search library from Meta that requires manual management of document storage and metadata. ChromaDB is a full vector database that handles document storage, metadata, and similarity search together. ChromaDB also has a Python-native API that is easier to work with for small to medium projects.

**What I used:**
I chose ChromaDB because it handled metadata storage natively, which I needed to track which chunks came from which job description. FAISS would have required separate data structures to manage that.

**What I modified:**
Nothing. I used ChromaDB exactly as suggested with cosine similarity via the hnsw:space parameter.

**Why I modified it:**
N/A.

**What I learned:**
FAISS is faster at scale but ChromaDB is more practical for projects where metadata and document management matter as much as retrieval speed.

**AI errors found:**
None.

\---

**Tool:** Claude

**Task:** I needed to convert my job description text into clean .txt files formatted consistently.

**Prompt used:**

> "Can you turn this job description into a clean text file format?"

**What AI suggested:**
AI reformatted each job description with consistent section headers (About the Company, About the Role, Key Responsibilities, Qualifications, Preferred Skills) and saved them as .txt files.

**What I used:**
I used the formatted .txt files directly as my JD corpus. The consistent section structure improved chunking quality since the sentence-aware splitter could follow natural paragraph breaks.

**What I modified:**
I reviewed each file and made minor edits to fix formatting inconsistencies across the 10 JDs.

**Why I modified it:**
A few files had inconsistent header names or missing sections that I wanted to standardize.

**What I learned:**
Consistent document formatting upstream significantly improves chunking and retrieval quality.

**AI errors found:**
None.

**Tool:** Claude

**Task:** My Streamlit app was throwing an API key not found error even though the key file existed.

**Prompt used:**

> "My Streamlit app says OPENAI\_API\_KEY not found even though my .env file exists. How do I fix it?"

**What AI suggested:**
AI suggested the file was either named incorrectly, in the wrong directory, or that load\_dotenv() was not finding it because the working directory differed from the file location. It suggested explicitly passing the path using load\_dotenv(dotenv\_path="env.txt").

**What I used:**
I updated the loading line to specify the path explicitly and the app picked up the key correctly.

**What I modified:**
I changed load\_dotenv() to load\_dotenv(dotenv\_path="env.txt") at the top of streamlit\_app.py.

**Why I modified it:**
The default load\_dotenv() searches for .env in the current working directory, which did not match where my file was saved when running from the Downloads folder.

**What I learned:**
Always specify the dotenv path explicitly when running Streamlit locally to avoid working directory issues.

**AI errors found:**
None.

\---

**Tool:** Claude

**Task:** I was setting up Streamlit and needed to know what files were required to run the app.

**Prompt used:**

> "What files do I need to run a Streamlit app locally?"

**What AI suggested:**
AI listed streamlit\_app.py, requirements.txt, and a .env file for storing the API key.

**What I used:**
I used all three. However I did not realize that .env was an actual file type with no extension rather than just a naming convention. I had created a file called env.txt instead which caused the app to throw an API key not found error.

**What I modified:**
I renamed the file and updated the dotenv loading line to load\_dotenv(dotenv\_path="env.txt") since Windows was not allowing me to save a file with no extension.

**Why I modified it:**
Windows requires a file extension so I kept the .txt extension and pointed dotenv to that filename explicitly.

**What I learned:**
On Windows, creating a true .env file with no extension requires either using the command line or a code editor like VS Code.

**AI errors found:**
The explanation could have been more clear, but nothing was conventionally wrong.

\---

**Tool:** Claude

**Task:** I wanted to display my evaluation results as a formatted markdown table instead of a raw pandas DataFrame.

**Prompt used:**

> "Can you convert this evaluation table into markdown format so it displays nicely?"

**What AI suggested:**
AI converted the DataFrame structure into a properly formatted markdown table with aligned columns and header separators.

**What I used:**
I used the markdown table directly in my test\_results.md evaluation file.

**What I modified:**
I updated the scores and faithfulness ratings based on my actual outputs before finalizing the table.

**Why I modified it:**
The initial table had placeholder values that needed to be replaced with real scores from manually reviewing each of the 9 analysis outputs.

**What I learned:**
Markdown tables are significantly more readable than raw DataFrame output for documentation purposes, especially when the audience includes non-technical readers.

**AI errors found:**
None.

\---

**Tool:** Claude

**Task:** I needed to add edge case testing to my retrieval pipeline.

**Prompt used:**

> "Can you give me code to test edge cases in my ChromaDB similarity search, like very short queries, unrelated queries, and ambiguous queries that could match multiple JDs?"

**What AI suggested:**
AI provided a loop that ran four test queries through the search function: a standard query, a very short single-word query, a completely unrelated query, and an ambiguous query that could match multiple JDs. Each result printed the matched company, chunk preview, and cosine distance.

**What I used:**
I used the suggested structure directly and added it as a dedicated cell in Section 4 of the notebook after the standard similarity search verification cell.

**What I modified:**
I customized the test queries to be relevant to my specific corpus, using queries that I knew would stress-test the retrieval across my 10 JDs.

**Why I modified it:**
AI's example used generic queries. I wanted the edge cases to reflect real ambiguities in my dataset, like queries that overlap between Goldman Sachs and Bayview since both are financial services data roles.

**What I learned:**
The unrelated query test revealed that ChromaDB still returns results even when nothing in the corpus is relevant, since it always returns the top k results regardless of distance. This is a limitation worth noting since the system has no threshold for rejecting low-confidence retrievals.

**AI errors found:**
None.

