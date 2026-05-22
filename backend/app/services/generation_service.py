from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_related_work(query, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an academic research assistant.

Using ONLY the retrieved research content below,
generate a professional Related Work summary.

User Research Topic:
{query}

Retrieved Research Content:
{context}

Instructions:
- Use only provided research content
- Do not invent papers or citations
- Write 2 professional paragraphs
- Add citation style references naturally
- Example:
  (Attention Is All You Need, 2017)
- Keep response concise and academic
"""

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content