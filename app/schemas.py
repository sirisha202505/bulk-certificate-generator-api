from pydantic import BaseModel, EmailStr, Field


class RecipientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    course_name: str = Field(..., min_length=2, max_length=200)


class GenerationRequest(BaseModel):
    recipients: list[RecipientCreate] = Field(..., min_length=1)


class GenerationJobResponse(BaseModel):
    job_id: int
    status: str
    total: int
    successful: int
    failed: int


class CertificateResponse(BaseModel):
    id: int
    job_id: int
    recipient_name: str
    recipient_email: str
    course_name: str
    status: str
    certificate_path: str | None = None
    error_message: str | None = None