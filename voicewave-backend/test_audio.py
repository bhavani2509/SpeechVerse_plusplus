import requests
import threading

def send_audio(file_path):
    url = "http://127.0.0.1:8000/process/"
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    print(f"Response: {response.json()}")

# List of audio files to upload
audio_files = [
    "test_audio -1.wav",
    "test_audio -2.wav",
    "test_audio -3.wav"
]

# Start threads
threads = []
for file_path in audio_files:
    thread = threading.Thread(target=send_audio, args=(file_path,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

