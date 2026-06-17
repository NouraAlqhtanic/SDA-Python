from llm import evaluate_resume

result = evaluate_resume(
    job_description="We are looking for a Python developer with FastAPI experience.",
    prompt="Focus on technical skills only.",
    resume_text="Nora has Python experience and built APIs using FastAPI and SQLModel.",
)

print(result)