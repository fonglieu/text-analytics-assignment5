# Memo

**To:** Hiring Manager
**Re:** RAG-Powered Resume Screening

\---

## Problem

Screening resumes is one of the most time-consuming parts of the hiring process.
For every open role, someone on your team has to manually read through applications,
compare each candidate's background to the job requirements, and make a judgment
call on fit for hundreds of submissions. This takes hours of work
that could be spent elsewhere, and it still leaves room for inconsistency across
reviewers. This project proposes an automated solution that handles that
first-pass screening without having to hire more people.

\---

## What I Built

I developed a Job Fit Analyzer that uses a technique called Retrieval-Augmented
Generation (RAG) to compare a candidate's resume against a job description. It
produces a structured, evidence-based fit report in seconds. The system pulls the
most relevant sections from the job description, compares them directly against the
resume, and generates three types of output that give your team an immediate read
on any applicant.

**Skill Gap Report**
Shows exactly which requirements the candidate meets with evidence from their
resume, which requirements they are missing, and specific actions they could take
to close each gap. This gives your team a clear, documented basis for screening
decisions rather than just a judgement call.

**Keyword Alignment**
Extracts the 15 most important terms from your job description, checks which ones
appear in the resume, and produces a match rate percentage. This tells you at a
glance how well a candidate's resume is aligned to your specific role requirements.

**Fit Summary**
A concise 3-4 sentence narrative that assigns an overall fit level of Strong,
Moderate, or Weak, with specific evidence cited from both documents. This is the
most readable output for a busy hiring manager who needs a quick verdict before
diving into the details.

The system runs as a simple web application. A recruiter or hiring manager selects
a job description from a dropdown, picks a report type, and gets results in
seconds. No technical background is required to navigate it, making it user-friendly.

\---

## Results

I tested the system against three roles across different industries: Goldman Sachs
Data Office Analyst, Bayview Asset Management Data Operations Analyst, and Delta
Air Lines Senior Analyst. Across all 9 analyses, the system correctly identified
the target role's requirements in every case.

The Skill Gap Report was the most useful output for screening purposes because it
gives a clear, documented breakdown that any reviewer can verify. The Keyword
Alignment report worked well for quickly flagging whether a resume was even in the
right ballpark before investing time in a deeper review. The Fit Summary was the
fastest read and worked best for initial triage.

The system performed best on roles with detailed, specific job descriptions. The
more clearly a role defines its requirements, the more accurate and useful the
output becomes. Roles with vague or preference-based requirements produced slightly
weaker results, which points to the value of writing precise job descriptions
to begin with.

\---

## Limitations

There are a few limitations to be aware of before considering broader deployment.
The system evaluates resumes against written content only, so qualities like culture
fit or communication style that come through in an interview are outside its scope.
It works best as a first-pass filter rather than a final decision tool, and hiring
decisions should still involve human judgment, particularly for senior or
specialized roles where context matters more than keyword matching.

The system also works best with specific, well-written job descriptions. Vague
requirements like "strong communication skills" or "team player" are harder to
evaluate from a resume than concrete technical requirements, and the output
reflects that. A few analyses also produced inconsistencies between report types
on the same candidate, for example a Fit Summary calling someone a strong fit while
the Keyword Alignment for the same role came back at 46%. Cross-referencing both
reports before making a screening decision is recommended.

\---

## Why This Is Worth Implementing

The business case is straightforward. If your team spends even a few hours per
week on manual resume screening, this tool pays for itself quickly. It standardizes
the screening process across all reviewers, reduces the risk of inconsistent
evaluations, and frees up your recruiting team to focus on interviews and candidate
relationships rather than document comparison. It also creates a documented record
for each screening decision, which is useful from a compliance standpoint.

The next step would be adapting the system to your specific job descriptions and
resume formats and integrating it into your existing applicant tracking workflow.
With those adjustments in place, this tool would serve as a reliable,
scalable first step in your hiring pipeline.

