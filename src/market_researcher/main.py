#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from market_researcher.crew import BSEMarketResearcher, HinduUPSCNotesCrew
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

def train():
    """Train the crew for a given number of iterations."""
    if len(sys.argv) < 4:
        print("Usage: python main.py train <n_iterations> <output_filename>")
        sys.exit(1)
    inputs = {
        "topic": "Bombay Stock Exchange",
        'current_year': str(datetime.now().year)
    }
    try:
        BSEMarketResearcher().crew().train(
            n_iterations=int(sys.argv[2]),
            filename=sys.argv[3],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """Replay the crew execution from a specific task."""
    if len(sys.argv) < 3:
        print("Usage: python main.py replay <task_id>")
        sys.exit(1)
    try:
        BSEMarketResearcher().crew().replay(task_id=sys.argv[2])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """Test the crew execution and returns the results."""
    if len(sys.argv) < 4:
        print("Usage: python main.py test <n_iterations> <eval_llm>")
        sys.exit(1)
    inputs = {
        "topic": "Bombay Stock Exchange",
        "current_year": str(datetime.now().year)
    }
    try:
        BSEMarketResearcher().crew().test(
            n_iterations=int(sys.argv[2]),
            eval_llm=sys.argv[3],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def open_report(path=None):
    # Open the Markdown report in the default browser or viewer
    report_path = os.path.abspath(path)
    if os.path.exists(report_path):
        # For HTML: convert and open, for MD: open in browser or editor
        webbrowser.open(f"file://{report_path}")
    else:
        print("Report file not found.")

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
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python main.py [run|train|replay|test] ...")
        sys.exit(1)