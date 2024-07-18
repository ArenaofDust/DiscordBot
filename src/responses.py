from difflib import get_close_matches
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_best_match(user_question: str, questions: dict) -> str | None:
    questions: list[str] = [q for q in questions]
    knowledge_matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)

    if knowledge_matches:
        return knowledge_matches[0]


