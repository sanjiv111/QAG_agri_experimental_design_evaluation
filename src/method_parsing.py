import os
import re
from typing import Optional, Tuple

import fitz  # PyMuPDF


# PATH SETUP


# This file is in:  <PROJECT_ROOT>/src/method_parsing.py
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)

# PDFs live directly in:  data/AgriQAG_GroundTruthCorpus/
PDF_DIR = os.path.join(PROJECT_ROOT, "data", "AgriQAG_GroundTruthCorpus")

# We will write extracted method sections to:
OUT_DIR = os.path.join(PDF_DIR, "methods_txt")

# Log file (status of each PDF)
LOG_PATH = os.path.join(PDF_DIR, "methods_extraction_log.txt")

os.makedirs(OUT_DIR, exist_ok=True)


# HEURISTICS: HEADINGS & KEYWORDS

METHOD_HEADINGS = [
    r"method\b",
    r"methods\b",
    r"materials\s+and\s+methods",
    r"methodology",
    r"approach\b",
    r"proposed\s+approach",
    r"model\b",
    r"model\s+architecture",
    r"system\s+overview",
    r"system\s+description",
    r"framework",
    r"study\s+design",
    r"implementation\s+details?",
    r"proposed\s+method",
    r"experiment\b",
    r"experiments\b",
    r"experimental\s+setup",
    r"experimental\s+settings?",
    r"evaluation"
]

# "3 Methods", "4.2 Experiments", etc
numbered_heading_pattern = re.compile(
    r"\n\s*(\d+(\.\d+)*)\s+(" + "|".join(METHOD_HEADINGS) + r")\s*\n",
    re.IGNORECASE,
)

# "METHODS", "Experiments"
plain_heading_pattern = re.compile(
    r"\n\s*(" + "|".join(METHOD_HEADINGS) + r")\s*\n",
    re.IGNORECASE,
)

# Next numbered section like "4 Results", "5 Discussion"
next_heading_pattern = re.compile(
    r"\n\s*(\d+(\.\d+)*)\s+[A-Z][A-Za-z0-9 ,\-]{2,}\s*\n"
)

FALLBACK_KEYWORDS = [
    "dataset",
    "corpus",
    "training data",
    "evaluation metric",
    "we evaluate",
    "we evaluate our model",
    "baseline",
    "we compare against",
    "we train",
    "training setup",
    "implementation details",
    "hyperparameters",
]


# HELPER FUNCTIONS

def extract_full_text(pdf_path: str) -> str:
    """Open a PDF and return all pages as one big text string."""
    doc = fitz.open(pdf_path)
    pages = [page.get_text("text") for page in doc]
    doc.close()
    return "\n".join(pages)


def clean_text(raw: str) -> str:
    """Normalise newlines a bit."""
    text = raw.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def find_methods_by_heading(text: str) -> Tuple[Optional[str], str]:
    """
    Strategy 1/2: try to find a Methods/Experiments-like section by headings.
    Returns (methods_text, status_label).
    """
    start_idx = None
    strategy = None

    # Numbered headings like '3 Methods'
    m = numbered_heading_pattern.search(text)
    if m:
        start_idx = m.start()
        strategy = "NUMBERED_HEADING"
    else:
        # Plain headings like 'METHODS'
        m = plain_heading_pattern.search(text)
        if m:
            start_idx = m.start()
            strategy = "PLAIN_HEADING"
        else:
            return None, "NO_METHOD_HEADING_FOUND"

    # End: next numbered section heading OR end of doc
    n = next_heading_pattern.search(text, pos=m.end())
    if n:
        end_idx = n.start()
        end_label = "NEXT_HEADING_FOUND"
    else:
        end_idx = len(text)
        end_label = "TO_DOC_END"

    methods_text = text[start_idx:end_idx].strip()

    if len(methods_text) < 300:
        return methods_text, f"{strategy}_{end_label}_SECTION_SHORT"

    return methods_text, f"{strategy}_{end_label}"


def find_methods_by_keywords(text: str) -> Tuple[Optional[str], str]:
    """
    Strategy 3: fallback keyword window around first experimental keyword.
    Returns (methods_text, status_label).
    """
    low = text.lower()
    pos = None
    for kw in FALLBACK_KEYWORDS:
        idx = low.find(kw)
        if idx != -1:
            pos = idx
            break

    if pos is None:
        return None, "FALLBACK_NO_KEYWORDS_FOUND"

    window_before = 2000
    window_after = 4000
    start_idx = max(0, pos - window_before)
    end_idx = min(len(text), pos + window_after)

    methods_text = text[start_idx:end_idx].strip()
    if len(methods_text) < 200:
        return None, "FALLBACK_WINDOW_TOO_SHORT"

    return methods_text, "FALLBACK_KEYWORD_WINDOW"



# MAIN


def main():
    log_lines = []

    if not os.path.isdir(PDF_DIR):
        raise FileNotFoundError(f"PDF_DIR does not exist: {PDF_DIR}")

    pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    pdf_files.sort()

    print(f"Found {len(pdf_files)} PDF files in {PDF_DIR}")

    # Uncomment for quick testing, e.g. first 2 files only
    # pdf_files = pdf_files[:2]

    for fname in pdf_files:
        pdf_path = os.path.join(PDF_DIR, fname)
        paper_id = os.path.splitext(fname)[0]

        print(f"Processing {paper_id}...")

        try:
            raw_text = extract_full_text(pdf_path)
            text = clean_text(raw_text)

            # Strategy 1/2: by headings
            methods_text, status = find_methods_by_heading(text)

            # If no heading or None returned, try fallback
            if methods_text is None or status == "NO_METHOD_HEADING_FOUND":
                fb_text, fb_status = find_methods_by_keywords(text)
                if fb_text is not None:
                    methods_text = fb_text
                    status = fb_status
                else:
                    log_lines.append(f"{fname}\tFAIL\t{status};{fb_status}")
                    continue  # go to next PDF

            # Write extracted text (even if somewhat short)
            out_name = f"{paper_id}_methods.txt"
            out_path = os.path.join(OUT_DIR, out_name)

            with open(out_path, "w", encoding="utf-8") as f_out:
                f_out.write(methods_text)

            log_lines.append(f"{fname}\tOK\t{status}")

        except Exception as e:
            log_lines.append(f"{fname}\tERROR\t{repr(e)}")

    with open(LOG_PATH, "w", encoding="utf-8") as f_log:
        f_log.write("\n".join(log_lines))

    print("Done.")
    print(f"Extracted sections saved in: {OUT_DIR}")
    print(f"Log file written to:        {LOG_PATH}")


if __name__ == "__main__":
    main()
