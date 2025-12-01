# Rater Guidelines – Human Evaluation of LLM Experimental Designs

## 1. Goal

We evaluate how well LLM-generated experimental designs match the human gold designs
for agricultural QAG papers. We follow good practice in NLG evaluation:
- Clear rating criteria
- Multiple raters
- Consistent scales
- Pilot + calibration
- Reported reliability (Cohen’s Kappa).

Each rater must read this document carefully before scoring.

## 2. Items to Rate

For each (paper_id, model, condition) we compare:

- HUMAN GOLD DESIGN: data/human_gold/pXX_gold_txt.txt
- LLM OUTPUT:       llm_outputs/<model>/pXX_methods.txt

We rate only the LLM output, but always in comparison to the gold.

## 3. Dimensions (1–5 each)

1. objective_score  
   - Does the LLM clearly and correctly state the experimental objective?

2. dataset_score  
   - Does it accurately describe the dataset(s) used (source, domain, size if given)?

3. model_score  
   - Does it correctly describe the main models/architectures (LLMs, retrievers, classifiers, etc.)?

4. procedure_score  
   - Are the experimental steps (data prep → model training → evaluation) correct, ordered, and reasonably complete?

5. evaluation_score  
   - Are metrics, baselines, and test sets described in a way that matches the gold design?

6. strengths_score  
   - Are realistic strengths identified without inventing fake advantages?

7. limitations_score  
   - Are real limitations identified without hallucinating problems not implied by the gold?

8. overall_alignment  
   - Overall, how close is the entire LLM design to the human gold design?

## 4. Scoring Scale (same for all dimensions)

5 = Excellent: Very close to gold, accurate and complete, no important errors.  
4 = Good: Mostly correct, only minor omissions or issues.  
3 = Fair: Mixed; some correct content but noticeable gaps or vagueness.  
2 = Poor: Major omissions or clear mismatches with the gold.  
1 = Very Poor: Mostly wrong, hallucinated, or unusable.

## 5. General Rules

- Base scores ONLY on comparison with the gold design.
- Do NOT reward nice writing style if content is wrong.
- Penalise hallucinations: invented datasets, models, baselines, metrics.
- Be consistent: if two outputs have similar quality, give similar scores.
- If unsure between two scores (e.g. 3 vs 4), we will pick the lower one (be conservative).

## 6. Rater Workflow (for each item)

1. Read the human gold design (pXX_gold_txt.txt) fully.
2. Read the LLM output fully.
3. Decide scores for each of the 8 dimensions using the 1–5 rubric.
4. Enter your scores into your rating sheet (CSV) with the correct paper_id, model, condition, rater.
5. Take a short note if something is weird or surprising (helpful for later analysis).

## 7. Pilot & Calibration

Before full scoring:
- All raters jointly score p01-deepseek-methods.
- Discuss differences, clarify guidelines.
- Optionally independently score p01-gemini-methods and compare.
Adjust your understanding of the scale, but do NOT change the rubric text.

After calibration, start the full evaluation.

## 8. Avoid Bias

- Ideally, hide system identities (label outputs as System A/System B). 
  If this is not possible, at least do not “favour” a model you personally like.
- Focus on factual correctness and completeness, not how famous the model is.

## 9. Reliability

Some items (e.g., p01 and p02) will be rated by multiple raters.
These will be used to compute Cohen’s Kappa. We will not discuss these items with other raters until after evaluation is finished.
