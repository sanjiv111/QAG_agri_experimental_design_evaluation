HUMAN RATING EVALUATION (TECHNIQUE 1)
======================================
This README explains, step-by-step, how to perform the Human Rating Evaluation
for the project:

Human rating is the PRIMARY and MOST IMPORTANT evaluation technique in this project
and forms the foundation for techniques 2–7 (error annotation, Kappa, t-test,
LLM-as-judge, correlations, etc.).


-------------------------------------
1. PURPOSE OF HUMAN RATING
-------------------------------------
We want to evaluate:
- RQ1: How closely LLM-generated experimental designs match the human-written gold designs from agricultural QAG papers.
- RQ2: What flaws (missing info, hallucinations, errors) appear in these designs.

To do this, each rater compares:
1) The Human Gold Experimental Design  (true reference)
2) The LLM-Generated Experimental Design (DeepSeek or Gemini)

and assigns:
- Eight numeric scores (1–5 scale)
- Error-category labels (yes/no)
- A brief summary comment


-------------------------------------
2. FILES YOU NEED TO USE
-------------------------------------

Human Gold Designs:
  data/human_gold/pXX_gold.txt

LLM Outputs (methods condition):
  llm_outputs/deepseek/pXX_deepseek_output.txt
  llm_outputs/gemini/pXX_gemini_output.txt

Scoring File:
  evaluation/01_human_rating/human_scores.csv

Scoring Rules:
  evaluation/01_human_rating/rater_guidelines.md


-------------------------------------
3. SCORING DIMENSIONS (WHAT TO SCORE)
-------------------------------------
For each LLM output, assign a score from 1 to 5 for each of these dimensions:

1) objective_score
2) dataset_score
3) model_score
4) procedure_score
5) evaluation_score
6) strengths_score
7) limitations_score
8) overall_alignment

Descriptions:

objective_score
  How well does the LLM state the experimental objective?

dataset_score
  Does it correctly and completely describe the dataset(s)?

model_score
  Does it correctly describe the model/architecture(s)?

procedure_score
  Are the training/inference/evaluation steps correct and clear?

evaluation_score
  Does it include the correct metrics, baselines, test sets, etc.?

strengths_score
  Does it identify realistic strengths (not hallucinated)?

limitations_score
  Does it identify realistic weaknesses (not hallucinated)?

overall_alignment
  Overall, how close is the LLM design to the human gold design?


-------------------------------------
4. THE 1–5 SCALE (USE FOR ALL SCORES)
-------------------------------------
1 = Very Poor
    Mostly wrong, hallucinated, or missing

2 = Poor
    Major omissions or important incorrect details

3 = Fair
    Some correct content but incomplete or vague

4 = Good
    Mostly correct, minor issues only

5 = Excellent
    Accurate, complete, very close to the human gold


-------------------------------------
5. ERROR CATEGORY LABELS
-------------------------------------
In addition to numeric scores, mark whether the following error types occur:

missing_info
added_hallucinations
incorrect_details
structural_errors
clarity_issues

Use: yes / no / minor / severe / short notes


-------------------------------------
6. CSV FORMAT (DO NOT MODIFY HEADER)
-------------------------------------
The file human_scores.csv MUST include this header:

paper_id,model,condition,objective_score,dataset_score,model_score,procedure_score,evaluation_score,strengths_score,limitations_score,overall_alignment,missing_info,added_hallucinations,incorrect_details,structural_errors,clarity_issues,summary_comment

Each LLM output becomes one new row in this CSV.


-------------------------------------
7. HOW TO PERFORM A HUMAN RATING (STEP BY STEP)
-------------------------------------

STEP 1: Open the human gold design
----------------------------------
Example:
  data/human_gold/p01_gold.txt

Read the file carefully to understand:
- Objective
- Dataset
- Model
- Procedure
- Evaluation metrics/baselines
- Strengths & limitations


STEP 2: Open the LLM-generated design
-------------------------------------
Example:
  llm_outputs/deepseek/p01_deepseek_output.txt
or
  llm_outputs/gemini/p01_gemini_output.txt


STEP 3: Compare section-by-section
----------------------------------
Ask:
- Does the LLM correctly reflect the gold?
- Is anything missing?
- Is anything hallucinated?
- Is anything incorrect?
- Is it clear and structured well?


STEP 4: Assign 1–5 scores for all 7 sections
--------------------------------------------
Use the scale in Section 4.
Be strict with hallucinations or missing key content.


STEP 5: Assign the overall_alignment score
------------------------------------------
This is your global judgment of how close the LLM output is to the gold.


STEP 6: Mark error categories
------------------------------
Use yes/no/minor/severe.
These labels are essential for answering RQ2.


STEP 7: Write a summary comment
-------------------------------
Example:
"Good objective and dataset description but missing evaluation metrics; some
incorrect model details."


STEP 8: Add a row to human_scores.csv
-------------------------------------
Example row:

p01,deepseek,methods,4,4,5,3,3,4,3,4,yes,no,yes,minor,no,Good objective but missing evaluation metrics.


-------------------------------------
8. WHO SHOULD RATE WHAT?
-------------------------------------
Each of the 5 group members should rate:
- Both models (DeepSeek + Gemini)
- For all assigned papers
- Under the methods condition initially

At least ONE paper (e.g., p01) should be rated by *two* raters so that we can compute inter-annotator agreement using Cohen’s Kappa.


-------------------------------------
9. QUALITY REQUIREMENTS
-------------------------------------
To ensure scientific consistency:

- All raters MUST read rater_guidelines.md before scoring.
- Do not copy each other's scores.
- Do not change your scores after analysis begins unless documented.
- Use the same interpretation of the 1–5 scale across all papers.


-------------------------------------
10. AFTER HUMAN RATING IS COMPLETE
-------------------------------------
Once human_scores.csv is fully filled, it will be used for:

- Technique 2: Error annotation
- Technique 3: Inter-annotator agreement (Kappa)
- Technique 4: System comparison (paired t-test)
- Technique 5: LLM-as-a-Judge validation
- Technique 6: Correlation analysis
- Technique 7: Prompt condition performance analysis

Human Rating MUST be completed before ANY other evaluation technique.
