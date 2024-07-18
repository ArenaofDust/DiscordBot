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

def get_response(message: str, knowledge: dict) -> str:
    best_match: str | None = get_best_match(message, knowledge)

    if best_match and (answer := knowledge.get(best_match)):
        return answer
    else:
        return get_response_from_openai(message)

def get_response_from_openai(message: str) -> str:
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ],
    max_tokens=150)
    return response.choices[0].message.content.strip()


def load_knowledge(file: str) -> dict:
    with open(file, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    test_knowledge: dict = load_knowledge('knowledge.json')
    test_response: str = get_response('hello', knowledge=test_knowledge)

    print(test_response)


