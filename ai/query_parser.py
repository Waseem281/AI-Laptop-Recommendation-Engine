import json
import re

from ai.groq_client import client
from config import MODEL_NAME


def parse_query(user_query: str):
    """
    Uses Groq to convert a natural language query
    into structured search parameters.
    """

    prompt = f"""
You are an AI Laptop Recommendation Assistant.

Extract the following information from the user's query.

Return ONLY valid JSON.

Fields:
- budget
- brand
- purpose
- processor
- gpu

Rules:
1. budget should be a number only.
2. If a field is missing, return an empty string.
3. Do not return markdown.
4. Do not explain anything.
5. Return JSON only.

Example 1

User:
Gaming laptop under 70000

Output:

{{
    "budget":70000,
    "brand":"",
    "purpose":"gaming",
    "processor":"",
    "gpu":""
}}

Example 2

User:
HP Ryzen laptop under 60000

Output:

{{
    "budget":60000,
    "brand":"HP",
    "purpose":"",
    "processor":"Ryzen",
    "gpu":""
}}

Example 3

User:
Laptop with RTX graphics

Output:

{{
    "budget":"",
    "brand":"",
    "purpose":"gaming",
    "processor":"",
    "gpu":"RTX"
}}

User Query:

{user_query}
"""

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response.choices[0].message.content.strip()

        # Remove markdown if Groq returns ```json
        answer = re.sub(r"^```json", "", answer)
        answer = re.sub(r"^```", "", answer)
        answer = re.sub(r"```$", "", answer)
        answer = answer.strip()

        data = json.loads(answer)

        return {
            "budget": data.get("budget", ""),
            "brand": data.get("brand", ""),
            "purpose": data.get("purpose", ""),
            "processor": data.get("processor", ""),
            "gpu": data.get("gpu", "")
        }

    except Exception as e:

        print("Groq Error:", e)

        return {
            "budget": "",
            "brand": "",
            "purpose": "",
            "processor": "",
            "gpu": ""
        }