from fastapi import FastAPI, File, UploadFile, HTTPException
import speech_recognition as sr
from io import BytesIO
import logging

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

@app.post("/speech-to-text/")
async def speech_to_text(file: UploadFile = File(...)):
    """
    Endpoint to accept an audio file and return its transcription.
    """
    # Validate that a file was uploaded
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    try:
        # Load the audio file from the request
        audio_data = await file.read()

        # Convert audio bytes to a file-like object
        audio_io = BytesIO(audio_data)

        # Convert the audio to text
        text = convert_audio_to_text(audio_io)

        # Return the transcription as a response
        return {"transcription": text}

    except Exception as e:
        logging.error(f"Error processing the file: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while processing audio.")

