from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ray import serve

import shutil
import os
import tempfile
import soundfile as sf

from nlp_service import NLPService
from transcription_service import TranscriptionService

# Create FastAPI app
app = FastAPI()

# Add CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@serve.deployment(num_replicas=2)
@serve.ingress(app)
class VoiceWaveAPI:
    def __init__(self):
        self.transcription_service = TranscriptionService(model_size="base")
        self.nlp_service = NLPService(model_name="google/flan-t5-small")
        os.makedirs("tmp", exist_ok=True)

    @app.get("/")
    async def root(self):
        return {"message": "VoiceWave API is running!"}

    @app.post("/process/")
    async def process_audio(self, file: UploadFile = File(...)):
        temp_path = os.path.join("tmp", file.filename)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcription = self.transcription_service.split_and_transcribe(temp_path)
        response = self.nlp_service.handle_instruction(transcription)

        return {
            "transcription": transcription,
            "response": response
        }

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    buffer_audio = b""
    counter = 0
    service = TranscriptionService(model_size="base")

    while True:
        try:
            data = await websocket.receive_bytes()
            buffer_audio += data
            counter += 1

            if counter >= 5:
                transcription = await process_audio_buffer(buffer_audio, service)
                await websocket.send_text(transcription)
                buffer_audio = b""
                counter = 0

        except Exception as e:
            print(f"WebSocket error: {e}")
            break

async def process_audio_buffer(audio_bytes, service):
    try:
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        print(temp_file)
        with open(temp_file.name, "wb") as f:
            f.write(audio_bytes)
            print(audio_bytes)

        text = service.transcribe(temp_file.name)
        return text
    except Exception as e:
        return f"Error processing: {str(e)}"
