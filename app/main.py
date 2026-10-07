from pathlib import Path

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Certificate, GenerationJob
from .schemas import (
    CertificateResponse,
    GenerationJobResponse,
    GenerationRequest,
)
from .services.certificate import generate_certificate


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bulk Certificate Generator API",
    description="Backend API for bulk certificate generation - AEREO SDE Intern Assignment",
    version="1.0.0",
)


def process_generation_job(
    job_id: int,
    recipients: list[dict],
) -> None:
    db = next(get_db())

    try:
        job = db.query(GenerationJob).filter(
            GenerationJob.id == job_id
        ).first()

        if not job:
            return

        job.status = "processing"
        db.commit()

        for recipient in recipients:
            certificate = Certificate(
                job_id=job_id,
                recipient_name=recipient["name"],
                recipient_email=recipient["email"],
                course_name=recipient["course_name"],
                status="processing",
            )

            db.add(certificate)
            db.commit()
            db.refresh(certificate)

            try:
                path = generate_certificate(
                    recipient_name=recipient["name"],
                    course_name=recipient["course_name"],
                    certificate_id=certificate.id,
                )

                certificate.certificate_path = path
                certificate.status = "completed"
                job.successful += 1

            except Exception as exc:
                certificate.status = "failed"
                certificate.error_message = str(exc)
                job.failed += 1

            db.commit()

        job.status = "completed"
        db.commit()

    except Exception:
        job.status = "failed"
        db.commit()

    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


@app.post(
    "/jobs",
    response_model=GenerationJobResponse,
    status_code=201,
)
def create_generation_job(
    request: GenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    job = GenerationJob(
        status="queued",
        total=len(request.recipients),
        successful=0,
        failed=0,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    recipients = [
        recipient.model_dump()
        for recipient in request.recipients
    ]

    background_tasks.add_task(
        process_generation_job,
        job.id,
        recipients,
    )

    return GenerationJobResponse(
        job_id=job.id,
        status=job.status,
        total=job.total,
        successful=job.successful,
        failed=job.failed,
    )


@app.get(
    "/jobs/{job_id}",
    response_model=GenerationJobResponse,
)
def get_generation_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found",
        )

    return GenerationJobResponse(
        job_id=job.id,
        status=job.status,
        total=job.total,
        successful=job.successful,
        failed=job.failed,
    )


@app.get(
    "/jobs/{job_id}/certificates",
    response_model=list[CertificateResponse],
)
def get_job_certificates(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found",
        )

    certificates = db.query(Certificate).filter(
        Certificate.job_id == job_id
    ).all()

    return certificates


@app.get("/certificates/{certificate_id}")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
):
    certificate = db.query(Certificate).filter(
        Certificate.id == certificate_id
    ).first()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found",
        )

    if certificate.status != "completed":
        raise HTTPException(
            status_code=409,
            detail="Certificate is not available",
        )

    if not certificate.certificate_path:
        raise HTTPException(
            status_code=404,
            detail="Certificate file path not found",
        )

    file_path = Path(certificate.certificate_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Certificate file does not exist",
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=file_path.name,
    )