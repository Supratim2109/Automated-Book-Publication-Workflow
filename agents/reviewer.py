from agents.llm_utils import call_llm
def reviewer_agent(content: str) -> str:
    prompt = f"""You are an AI Reviewer. Review the following rewritten chapter for clarity, grammar, and flow. Make improvements where needed, but preserve the writer's tone and creativity.
    {content}
    """
    return call_llm(prompt)

