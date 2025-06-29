#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from market_researcher.crew import BSEMarketResearcher, HinduUPSCNotesCrew, MCQGenerationCrew
from dotenv import load_dotenv
import os
import webbrowser

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
load_dotenv()

def run():
    """Run the crew."""
    inputs = {
        'topic': 'Bombay Stock Exchange',
        'current_year': str(datetime.now().year)
    }
    try:
        BSEMarketResearcher().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def run_the_hindu():
    """Run the Hindu UPSC Notes crew."""
    inputs = {
        'topic': 'Hindu News',
        'current_year': str(datetime.now().year)
    }
    try:
        HinduUPSCNotesCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the Hindu UPSC Notes crew: {e}")
    
def run_mcqg():
    """Run the MCQ Generator crew."""
    inputs = {
        "pdf_path" : r"knowledge\PolityNotes.pdf"
    }
    try:
        MCQGenerationCrew().crew().kickoff(inputs=inputs)
    except ImportError:
        raise ImportError("MCQ Generation crew is not implemented yet. Please implement it in the crew.py file.")

def open_report(path=None):
    # Open the Markdown report in the default browser or viewer
    report_path = os.path.abspath(path)
    if os.path.exists(report_path):
        # For HTML: convert and open, for MD: open in browser or editor
        webbrowser.open(f"file://{report_path}")
    else:
        print("Report file not found.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [run|train|replay|test] ...")
        sys.exit(1)
    command = sys.argv[1].lower()
    if command == "run":
        run()
        open_report("bse_report.md")
    elif command == "run_hindu":
        run_the_hindu()
        open_report("upsc_notes.md")
    elif command == "run_mcqg":
        run_mcqg()
        open_report("mcqs.md")
    else:
        print(f"Unknown command: {command}")
        print("Usage: python main.py [run|train|replay|test] ...")
        sys.exit(1)