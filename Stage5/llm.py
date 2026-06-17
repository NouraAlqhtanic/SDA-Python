import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def evaluate_resume(job_description: str, prompt: str, resume_text: str) -> str:
    system_prompt = """
You are an expert HR assistant.
Evaluate how well a candidate's resume matches a job description.

Structure your response clearly:
1. Match Score from 0 to 10
2. Key Strengths
3. Gaps or Missing Skills
4. Overall Recommendation

Be specific, professional, and concise.
"""

    user_message = f"""
Job Description:
{job_description}

Resume Text:
{resume_text}

Additional User Prompt:
{prompt if prompt else "No additional prompt provided."}
"""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=700,
    )

    return response.choices[0].message.content