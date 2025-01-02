#!/usr/bin/env python
import sys
import warnings
from assetmanagement.crew import Assetmanagement

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

company = "Garmin"

def run():
    """
    Run the crew.
    """
    inputs = {
        'company': company
    }
    Assetmanagement().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "company": company
    }
    try:
        Assetmanagement().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Assetmanagement().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "company": company
    }
    try:
        Assetmanagement().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
