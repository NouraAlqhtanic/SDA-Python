from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from auth_utils import get_current_user
from llm import evaluate_resume
from pdf_utils import extract_text_from_pdf
from schemas import EvaluateResponse

router = APIRouter()


@router.post("/", response_model=EvaluateResponse)
async def evaluate(
    job_description: str = Form(...),
    prompt: str = Form(""),
    resume: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
):
    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted"
        )

    file_content = await resume.read()
    resume_text = extract_text_from_pdf(file_content)

    if not resume_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not extract text from the PDF. Make sure it is a text-based PDF, not a scanned image."
        )

    result = evaluate_resume(job_description, prompt, resume_text)

    return EvaluateResponse(result=result)