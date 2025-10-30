"""decomposition_test.py

Reads user questions from an Excel file and runs only the MAG-SQL decomposer
(the `decomposition_node`) for each question. Results are printed and saved to
an output JSON file.

Usage (PowerShell):
    python decomposition_test.py --input questions.xlsx --output decomposition_results.json

Notes:
 - This module imports `app` from `graph.py` (as requested) and also imports
   `decomposition_node` from `base.py` to execute the decomposer directly.
 - The script forces decomposition by building a small `ComplexityAnalysis`
   instance with `needs_decomposition=True` before calling the node.
"""

from __future__ import annotations

import argparse
import json
import os
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

import pandas as pd
import warnings
import logging
import os

# Environment tweaks to quiet third-party libraries
# Disable tokenizer parallelism warnings and reduce transformers verbosity
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

# Suppress common warning categories
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=ImportWarning)

# Configure logging: set root level to WARNING and make noisy libs ERROR
logging.getLogger().setLevel(logging.WARNING)
noisy_loggers = (
    "langchain",
    "langchain_core",
    "sentence_transformers",
    "chromadb",
    "transformers",
    "urllib3",
    "openai",
    "sqlalchemy",
    "llm_config",
)
for name in noisy_loggers:
    logging.getLogger(name).setLevel(logging.ERROR)

# Pandas: disable chained-assignment warnings
try:
    pd.options.mode.chained_assignment = None  # type: ignore[attr-defined]
except Exception:
    pass

# Import the compiled app per your request (graph.py contains `app = workflow.compile()`)
try:
    from graph import app  # noqa: F401
except Exception:
    # If graph import fails, we still proceed because we call decomposition_node directly
    app = None

# Suppress prints coming from other modules: replace builtins.print with a diagnostic wrapper
import builtins, inspect, sys
from collections import defaultdict
_original_print = builtins.print

# Log file for suppressed print origins
_print_origins_log = os.path.join(os.path.dirname(__file__), "print_origins.log")
_print_count = defaultdict(int)
_PRINT_LIMIT_PER_CALLER = 20

def _diagnostic_print(*args, **kwargs):
    """Allow prints only when caller is this file; otherwise log the origin.

    To diagnose where noisy prints originate from, this wrapper records
    the caller file/line/function and a short stack excerpt to
    `print_origins.log` (limited per caller to avoid log explosion).
    """
    try:
        # Check the immediate call stack for an allowed caller
        stack = inspect.stack()
        allowed = False
        caller_frame = None
        for frame_info in stack[1:8]:
            caller_file = frame_info.filename or ''
            if caller_file.endswith('decomposition_test.py'):
                allowed = True
                break
            # remember last frame for logging
            if caller_frame is None:
                caller_frame = frame_info

        if allowed:
            return _original_print(*args, **kwargs)

        # If not allowed, log the origin (limited per caller)
        if caller_frame is not None:
            caller_key = f"{os.path.basename(caller_frame.filename)}:{caller_frame.lineno} in {caller_frame.function}"
        else:
            caller_key = "unknown"

        if _print_count[caller_key] < _PRINT_LIMIT_PER_CALLER:
            try:
                with open(_print_origins_log, 'a', encoding='utf-8') as f:
                    f.write(f"Origin: {caller_key}\n")
                    # Write a short representation of the printed message
                    try:
                        msg = ' '.join(map(str, args))
                    except Exception:
                        msg = str(args)
                    f.write(f"Message: {msg[:400]}\n")
                    f.write("Stack excerpt:\n")
                    for fi in stack[1:6]:
                        f.write(f"  File \"{fi.filename}\", line {fi.lineno}, in {fi.function}\n")
                    f.write("-"*60 + "\n")
            except Exception:
                # ignore logging failures
                pass
            _print_count[caller_key] += 1

        # Suppress the actual print
        return None

    except Exception:
        # On any inspection error, fall back to original print
        return _original_print(*args, **kwargs)

# Install the diagnostic print wrapper
builtins.print = _diagnostic_print

# Also wrap sys.stdout.write and sys.stderr.write to capture direct writes
_orig_stdout_write = sys.stdout.write
_orig_stderr_write = sys.stderr.write

def _wrap_write(orig_write, stream_name):
    def _w(s):
        try:
            # Only log if the write comes from outside this file
            stack = inspect.stack()
            for frame_info in stack[1:8]:
                if (frame_info.filename or '').endswith('decomposition_test.py'):
                    return orig_write(s)
            # Log a short excerpt
            with open(_print_origins_log, 'a', encoding='utf-8') as f:
                f.write(f"Direct write to {stream_name}: {str(s)[:400]}\n")
            return None
        except Exception:
            return orig_write(s)
    return _w

sys.stdout.write = _wrap_write(_orig_stdout_write, 'stdout')
sys.stderr.write = _wrap_write(_orig_stderr_write, 'stderr')

# Import the decomposer node and model classes
from base import decomposition_node
from models import ComplexityAnalysis


def read_questions_from_excel(path: str, question_col: Optional[str] = None) -> List[Dict[str, Any]]:
    """Read questions from an Excel file.

    If `question_col` is provided, use that column name. Otherwise, use the
    first column in the sheet as the question column.
    """
    df = pd.read_excel(path, engine="openpyxl")
    if df.empty:
        return []

    if question_col and question_col in df.columns:
        col = question_col
    else:
        # Fallback: pick the first column name
        col = df.columns[0]

    questions = []
    for _, row in df.iterrows():
        q = row.get(col)
        if pd.isna(q):
            continue
        questions.append({"question": str(q).strip(), "row": row.to_dict()})
    return questions


def run_decomposer_for_question(question: str, conversation: Optional[List[Dict]] = None) -> Dict[str, Any]:
    """Run the MAG-SQL decomposition_node for a single question.

    We force decomposition by supplying a ComplexityAnalysis with
    needs_decomposition=True. The function returns the raw node output and a
    serializable decomposition plan when available.
    """
    if conversation is None:
        conversation = []

    # Force decomposition by creating a ComplexityAnalysis instance
    complexity_obj = ComplexityAnalysis(
        needs_decomposition=True,
        complexity_score=0.9,
        complexity_reasons=["forced decomposition for testing"],
        suggested_approach="iterative",
    )

    state = {
        "question": question,
        "conversation": conversation,
        "table_metadata": "",
        "complexity_analysis": complexity_obj,
    }

    # Call the decomposer node directly
    try:
        result = decomposition_node(state)
    except Exception as e:
        result = {"error": f"Exception while running decomposer: {e}"}

    return result

def _make_serializable(obj: Any) -> Any:
    """Attempt to convert objects (pydantic models, namespaces, etc.) into
    JSON-serializable structures.
    """
    # pydantic BaseModel has .dict()
    try:
        dict_method = getattr(obj, "dict", None)
        if callable(dict_method):
            return dict_method()
    except Exception:
        pass

    # SimpleNamespace or objects with __dict__
    if isinstance(obj, SimpleNamespace):
        return vars(obj)

    if hasattr(obj, "__dict__"):
        try:
            return {k: _make_serializable(v) for k, v in vars(obj).items()}
        except Exception:
            pass

    # Lists and dicts
    if isinstance(obj, list):
        return [_make_serializable(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}

    # Fallback to str
    try:
        return str(obj)
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description="Run MAG-SQL decomposer on questions from an Excel file")
    parser.add_argument("--input", "-i", required=True, help="Path to input Excel file (e.g. questions.xlsx)")
    parser.add_argument("--output", "-o", default="decomposition_results.json", help="Path to write JSON results")
    parser.add_argument("--output-excel", "-e", dest="output_excel", help="Optional path to write Excel results (defaults to same name as JSON with .xlsx)")
    parser.add_argument("--question-col", help="Optional column name containing questions (defaults to first column)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
        return

    print(f"Reading questions from {args.input}...")
    questions = read_questions_from_excel(args.input, question_col=args.question_col)
    if not questions:
        print("No questions found in the input file.")
        return

    results = []
    for i, item in enumerate(questions, 1):
        q = item["question"]
        print(f"[{i}/{len(questions)}] Running decomposer for question: {q}")
        res = run_decomposer_for_question(q, conversation=item.get("row", {}).get("conversation", []))
        # print(f"Decomposition result Check: {res.get('decomposition_plan') or res.get('raw_result')}")
        results.append(res)

    # Save results (JSON)í
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved decomposition results to {args.output}")

    # Save results to Excel (two columns: Question, Decomposition output)
    excel_path = args.output_excel if args.output_excel else os.path.splitext(args.output)[0] + ".xlsx"
    try:
        rows = []
        for r in results:
            # question = 
        
            # Prefer the parsed decomposition plan; fallback to raw_result
            decomp = r
            # Serialize non-string objects to JSON for Excel cell
            if isinstance(decomp, (dict, list)):
                decomp_str = json.dumps(decomp, ensure_ascii=False)
            else:
                decomp_str = str(decomp) if decomp is not None else ""
            rows.append({ "Decomposition output": decomp_str})

        df_out = pd.DataFrame(rows)
        df_out.to_excel(excel_path, index=False, engine="openpyxl")
        print(f"Saved decomposition results to Excel: {excel_path}")
    except Exception as e:
        print(f"Failed to write Excel file {excel_path}: {e}")


if __name__ == "__main__":
    main()
