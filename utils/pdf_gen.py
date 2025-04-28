from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(summary, transcript, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    text = c.beginText(40, height - 40)
    text.setFont("Helvetica", 12)

    text.textLine("Meeting Summary:")
    text.textLines(summary)
    text.textLine("")
    text.textLine("Transcript:")
    text.textLines(transcript)

    c.drawText(text)
    c.save()