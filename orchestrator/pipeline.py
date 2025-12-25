from agents.writer import writer_agent
from agents.reviewer import reviewer_agent

def run_pipeline(content: str) -> str:
    print("Running Writer Agent...")
    rewritten=writer_agent(content)
    print("Running Reviwer Agent... ")
    reviewed=reviewer_agent(rewritten)
    return rewritten, reviewed