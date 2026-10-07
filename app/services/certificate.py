from pathlib import Path

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path("app/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_certificate(
    recipient_name: str,
    course_name: str,
    certificate_id: int,
) -> str:
    filename = f"certificate_{certificate_id}.pdf"
    file_path = OUTPUT_DIR / filename

    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(str(file_path), pagesize=landscape(A4))

    # Border
    pdf.setLineWidth(3)
    pdf.rect(
        30,
        30,
        page_width - 60,
        page_height - 60,
    )

    # Title
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 120,
        "CERTIFICATE OF PARTICIPATION",
    )

    # Subtitle
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 160,
        "This certificate is proudly presented to",
    )

    # Recipient
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 220,
        recipient_name,
    )

    # Course
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 270,
        f"for successful participation in {course_name}",
    )

    # Certificate ID
    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(
        page_width / 2,
        75,
        f"Certificate ID: {certificate_id}",
    )

    pdf.save()

    return str(file_path)