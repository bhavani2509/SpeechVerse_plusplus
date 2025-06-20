import whisper
import librosa
import tempfile
import os
import numpy as np
import ray
import soundfile as sf


class TranscriptionService:
    def __init__(self, model_size="base"):
        print(f"Loading Whisper model: {model_size}")
        self.model_size = model_size
        self.model = whisper.load_model(model_size)
        print("Whisper model loaded.")

    def transcribe(self, audio_file_path):
        result = self.model.transcribe(audio_file_path)
        return result["text"]

    @staticmethod
    @ray.remote
    def _transcribe_chunk(audio_array, sr, model_size="base"):
        model = whisper.load_model(model_size)
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)

        # Save chunk using soundfile (correct way)
        sf.write(temp_file.name, audio_array, sr)

        result = model.transcribe(temp_file.name)
        return result["text"]

    def split_and_transcribe(self, audio_file_path, chunk_duration=None):
        print(f"Splitting and transcribing: {audio_file_path}")
        audio, sr = librosa.load(audio_file_path, sr=None)
        total_duration = librosa.get_duration(y=audio, sr=sr)
        if chunk_duration is None:
            if total_duration <= 30:
                chunk_duration = total_duration
            elif total_duration <= 120:
                chunk_duration = 20
            else:
                chunk_duration = 30
        samples_per_chunk = int(chunk_duration * sr)
        tasks = []
        for start in range(0, len(audio), samples_per_chunk):
            end = start + samples_per_chunk
            audio_chunk = audio[start:end]
            task = self._transcribe_chunk.remote(audio_chunk, sr, self.model_size)
            tasks.append(task)

        partial_results = ray.get(tasks)
        return " ".join(partial_results)
