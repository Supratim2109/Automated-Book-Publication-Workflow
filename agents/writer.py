from agents.llm_utils import call_llm
def writer_agent(content: str) -> str:
    prompt = f"""You are an AI writer. Give a "spin" to the following content to make it more engaging and polished:
    {content} 
    """
    return call_llm(prompt)
