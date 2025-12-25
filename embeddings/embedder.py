from google import  genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment.")

client = genai.Client(api_key= api_key)

def get_embedding(text: str) -> list:
    result= client.models.embed_content(
        model = "gemini-embedding-exp-03-07",
        contents= text
    )
    return result

