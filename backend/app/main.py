from fastapi import FastAPI, File, UploadFile, HTTPException
import speech_recognition as sr
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import logging
import tempfile

app = FastAPI()

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)

def convert_audio_to_text(audio_io: BytesIO) -> str:
    """
    Convert audio file-like object to text using Google's Speech Recognition API.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_io) as audio_file:
        audio = recognizer.record(audio_file)
        try:
            # Recognize speech using Google API
            text = recognizer.recognize_google(audio)
            logging.info(f"Transcription successful: {text}")
            return text
        except sr.UnknownValueError:
            logging.error("Speech was not clear enough to be understood.")
            raise HTTPException(status_code=400, detail="Speech not clear enough.")
        except sr.RequestError as e:
            logging.error(f"Google Speech Recognition API error: {e}")
            raise HTTPException(status_code=503, detail=f"Google Speech Recognition service unavailable: {e}")

def create_pdf(text: str) -> BytesIO:
    """
    Generate a PDF file from the provided text.
    """
    pdf_io = BytesIO()
    c = canvas.Canvas(pdf_io, pagesize=letter)
    width, height = letter

    # Write the text to the PDF
    c.drawString(100, height - 100, text)
    c.showPage()
    c.save()
    pdf_io.seek(0)  # Move to the beginning of the BytesIO buffer
    return pdf_io

@app.post("/speech-to-text/")
async def speech_to_text(file: UploadFile = File(...)):
    """
    Endpoint to accept an audio file and return its transcription.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    try:
        audio_data = await file.read()
        audio_io = BytesIO(audio_data)
        text = convert_audio_to_text(audio_io)
        return {"transcription": text}

    except Exception as e:
        logging.error(f"Error processing the file: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while processing audio.")

@app.post("/text-to-pdf/")
async def text_to_pdf(text: str):
    """
    Endpoint to accept text and generate a PDF.
    """
    if not text:
        raise HTTPException(status_code=400, detail="No text provided.")

    try:
        pdf_io = create_pdf(text)
        return {
            "pdf_file": pdf_io.getvalue()  # Return the PDF content as bytes
        }

    except Exception as e:
        logging.error(f"Error generating PDF: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while generating PDF.")
