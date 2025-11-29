EVALUATION FOLDER - OVERVIEW

This folder contains all evaluation artefacts for the project:

"Evaluation of Experimental Design Quality of LLM-Generated Experimental Setups
for Question Answering Generation (QAG) in the Agricultural Domain."

We use several evaluation techniques:

1) Human Rating Evaluation (primary technique)
2) Error Category Annotation (for RQ2)
3) Inter-Annotator Agreement (Cohen's Kappa)
4) System Comparison (Paired t-test between DeepSeek and Gemini)
5) LLM-as-a-Judge (automatic evaluation)
6) Correlation between Human Scores and Judge Scores
7) Optional: Prompt Condition Analysis (methods vs metadata)


HOW TO APPROACH EVALUATION (ORDER OF STEPS)
-------------------------------------------

Step 1: HUMAN RATING EVALUATION (Technique 1)
---------------------------------------------
- Each group member reads:
  - the human gold experimental design (data/human_gold/pXX_gold.txt)
  - the LLM-generated design (llm_outputs/deepseek or llm_outputs/gemini)
- They then score the LLM output on an 8-dimensional 1–5 scale.
- Scores and brief comments are added to human_scores.csv.
- This is the primary evidence for RQ1 and RQ2.


Step 2: ERROR CATEGORY ANNOTATION (Technique 2)
-----------------------------------------------
- For each LLM output, raters also indicate which error types are present:
  - Missing information
  - Hallucinations
  - Incorrect details
  - Structural errors
  - Clarity issues
- These annotations are saved in error_analysis/pXX_errors.txt
  and also summarized in the error-related columns in human_scores.csv.
- This directly answers RQ2 (what common flaws occur?).

Step 3: INTER-ANNOTATOR AGREEMENT (Technique 3)
-----------------------------------------------
- For a subset of items, at least two raters score the same outputs.
- Overall alignment scores are converted into coarse labels (e.g., good vs not_good).
- Cohen's Kappa is computed using a script in src/analysis/.
- This shows how consistent the human ratings are.

Step 4: SYSTEM COMPARISON (Technique 4)
---------------------------------------
- For each paper, model, and condition, we compute the mean human scores.
- We compare DeepSeek vs Gemini using a paired t-test over papers.
- This tells us whether one model is significantly better under our criteria.

Step 5: LLM-AS-A-JUDGE (Technique 5)
------------------------------------
- A strong external LLM (judge) is given:
  - the human gold design
  - the LLM-generated design
- It returns 1–5 quality scores and short justifications.
- These scores are stored in judge_scores/ as JSON or CSV.

Step 6: CORRELATION ANALYSIS (Technique 6)
------------------------------------------
- We compute correlations between:
  - human overall scores
  - LLM-judge overall scores
- This shows how well LLM-as-a-Judge approximates human evaluation.

Step 7: PROMPT CONDITION ANALYSIS (Optional Technique)
------------------------------------------------------
- For models that have both conditions (methods vs metadata),
  we compare performance across conditions.
- This helps us understand how input format affects LLM design quality.

