from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# UPDATED: Signature now accepts lists for chunks and metadata references directly
def generate_related_work(chunks: list[str], references: list[dict]) -> str:
    
    # NEW: Formats the dictionary data into a clean text block for the LLM to read
    ref_block = "\n".join(
        f"- {r['authors']} ({r['year']}). {r['title']}."
        for r in references
    )
    
    # UPDATED: Trainer's strict academic prompt structure
    prompt = f"""You are writing a related work section for an academic paper.
Use only the information in the provided excerpts.
Cite using the references listed below — do not invent authors or years.
Available references:
{ref_block}

Excerpts:
{chr(10).join(chunks)}

Write 2–3 paragraphs with inline citations like (Authors, Year)."""

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