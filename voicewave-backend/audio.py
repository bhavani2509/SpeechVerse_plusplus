import sounddevice as sd
import soundfile as sf

# Settings
duration = 5  # seconds
samplerate = 16000  # 16 kHz

print("🎤 Speak now... Recording for 5 seconds...")
audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
sd.wait()

# Save to file
sf.write('test_audio.wav', audio, samplerate)
print("✅ Saved as test_audio.wav")
