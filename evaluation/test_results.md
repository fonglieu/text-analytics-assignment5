## Evaluation Results

### BSAN 6200: Text Mining \& Social Media Analytics — Spring 2026

### Assignment 5 — Option B: Job Fit Analyzer

**Student:** Fong Lieu

\---

### Overview

I ran all three analysis types (Skill Gap Report, Keyword Alignment, and Fit Summary) on my top 3 target job descriptions: Goldman Sachs, Bayview Asset Management, and Delta Air Lines. That produced 9 total analyses which I evaluated across four criteria.

\---

### Evaluation Table

|Company|Analysis Type|Retrieval Relevance|Skill ID Accuracy|Actionability (1-5)|Faithfulness|
|-|-|-|-|-|-|
|Goldman Sachs|Skill Gap|Yes|5/6 correct|4|Partial|
|Goldman Sachs|Keyword Alignment|Yes|11/15 correct|3|Faithful|
|Goldman Sachs|Fit Summary|Yes|N/A|4|Faithful|
|Bayview Asset Management|Skill Gap|Yes|7/8 correct|4|Faithful|
|Bayview Asset Management|Keyword Alignment|Yes|10/15 correct|3|Partial|
|Bayview Asset Management|Fit Summary|Yes|N/A|4|Faithful|
|Delta Air Lines|Skill Gap|Yes|4/5 correct|4|Faithful|
|Delta Air Lines|Keyword Alignment|Yes|11/15 correct|3|Faithful|
|Delta Air Lines|Fit Summary|Yes|N/A|4|Faithful|

\---

### Scoring Notes

**Retrieval Relevance (Yes/Partial/No)**
All 9 analyses returned Yes because every output correctly referenced the target JD's specific requirements. Goldman Sachs outputs cited data governance and private markets. Bayview outputs cited ETL tools and mortgage data operations. Delta outputs cited AWS, ETL pipelines, and aviation industry experience.

**Skill ID Accuracy (count correct vs incorrect)**
Fit Summary rows are marked N/A since the output is a narrative rather than a discrete list of skills. For Skill Gap and Keyword Alignment, I manually verified each identified skill or keyword against the actual resume and JD text.

The one incorrect match in the Goldman Sachs Skill Gap was "Stakeholder Engagement," which the model flagged as a match based on the candidate's teaching role. That connection is too loose given the role specifically requires engaging with investment professionals and compliance teams.

The five incorrect keywords in the Bayview Keyword Alignment included "Communication skills: MISSING" which was wrong — communication skills are explicitly listed in the resume's Technical Skills section and the entire teaching role demonstrates them.

**Actionability (1-5)**
Skill Gap and Fit Summary both scored 4 across all three companies. Recommendations named real certifications (DAMA Certified Data Management Professional), real platforms (Coursera, AWS), and specific tools (Apache Airflow, Talend) rather than giving generic advice.

Keyword Alignment scored 3 across the board because it identifies gaps but does not recommend what to do about them. It reports a match rate and a one sentence summary but leaves next steps to the user.

**Faithfulness (Faithful/Partial/Hallucinated)**
Goldman Sachs Skill Gap was marked Partial because the model listed "Project Support" as a matching skill based on the candidate tracking timelines as a teaching facilitator. Managing a classroom schedule is not equivalent to supporting a data project at a financial firm.

Bayview Keyword Alignment was marked Partial because of the communication skills error described above.

All other outputs were faithful to the document content with no hallucinated qualifications or fabricated requirements.

\---

### Analysis

**Which analysis type worked best?**
The Skill Gap Report worked best across all three companies. The three-section structure made outputs easy to verify manually, and the recommended actions were specific enough to be actionable, naming real certifications, platforms, and tools. It scored a 4 out of 5 on actionability across all three companies.

Keyword Alignment was the easiest to verify since every claim is a discrete table row I could check directly against the resume and JD. It scored lower on actionability (3 out of 5) because it identifies gaps but does not recommend what to do about them. Fit Summary was readable and well structured after the final prompt iteration but harder to score for accuracy since it is a narrative rather than a checklist.

**Which JDs produced the best/worst results?**
Bayview produced the strongest results because the JD was specific. It named actual ETL tools, required data warehouse design explicitly, and listed cloud technologies as a hard requirement. That gave the model clear criteria to compare against the resume, and 7 out of 8 matching skills held up when I verified them manually.

Goldman Sachs produced the weakest results. The JD mixes hard technical requirements with soft preferences like "interest in private markets" and "curiosity about AI" which are hard to evaluate from a resume. The model made loose inferences as a result. It listed "Stakeholder Engagement" as a match based on the teaching role, then the keyword alignment output flagged the same skill as missing. Same data, opposite conclusions from two different prompts.

Delta fell in the middle. The candidate has real skill overlap with what Delta needs, and the keyword alignment table correctly identified logistics experience as partially relevant to Delta's transportation industry preference. The main weakness was the fit summary calling the candidate a "strong fit" despite no aviation-specific experience.

**Where did the system hallucinate or produce inaccurate results?**
The clearest error was in the Bayview Keyword Alignment output which marked "Communication skills: MISSING" despite the skill being explicitly listed in the resume and the candidate's entire teaching role demonstrating it. The model searched for the exact string rather than matching semantically.

The Goldman Sachs Skill Gap report listed "Project Support" as a match based on the candidate tracking timelines as a teaching facilitator. That is too loose a connection given the role is about supporting data projects at a financial firm.

The Bayview Fit Summary also called the candidate a "Strong" fit while the keyword alignment analysis on the same JD produced a 46.67% match rate. Those two outputs directly contradict each other.

**What would you improve?**
The biggest improvement would be filtering retrieval by JD filename so only chunks from the target document are returned. Right now all 10 JDs sit in the same ChromaDB collection, which creates a risk of pulling content from the wrong JD during retrieval, especially for similar roles like Goldman Sachs and Bayview.

I would also update the keyword alignment prompt to check for semantic equivalents before marking a skill as missing, which would have caught the communication skills error. And for the fit summary, I would pass in the keyword match rate as context so the fit verdict is grounded in a quantitative score rather than the model making its own holistic judgment.

