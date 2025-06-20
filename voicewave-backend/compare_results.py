import requests
import time
import matplotlib.pyplot as plt
from jiwer import wer


import re

def clean_text(text):
    # Remove punctuation and make lowercase
    return re.sub(r"[^\w\s]", "", text).lower().strip()

# Test files and references
test_files = {
"sheldon2": ("sheldon2.mp3", "sheldon2.txt"),

    "sheldon3": ("sheldon3.mp3", "sheldon3.txt")
}

APIS = {
    "Local API": "http://localhost:8000/process/",
    "EC2 API":   "http://3.143.239.220:8000/process/"
}

headers = { "accept": "application/json" }

# Results will be stored like: results[api][file] = {"time": x, "wer": y}
results = {api: {} for api in APIS}

for file_key, (audio_path, ref_path) in test_files.items():
    reference = ""
    with open(ref_path, "r") as ref_file:
        for i in ref_file.readlines():
            reference = reference + i.strip().lower()+" "
    print(reference)
    for api_name, url in APIS.items():
        with open(audio_path, "rb") as f:
            files = {"file": (audio_path, f, "audio/wav")}
            print(f"\nSending {audio_path} to {api_name}...")

            start_time = time.time()
            try:
                response = requests.post(url, headers=headers, files=files, timeout=120)
                end_time = time.time()
                elapsed = end_time - start_time

                if response.status_code == 200:
                    response_json = response.json()
                    transcription = clean_text(response_json.get("transcription", ""))
                    print(transcription)
                    wer_score = wer(reference, transcription)
                    results[api_name][file_key] = {
                        "time": elapsed,
                        "wer": wer_score
                    }
                    print(f"{api_name} [{file_key}]: {elapsed:.2f}s, WER: {wer_score:.2%}")
                else:
                    print(f"{api_name} [{file_key}] failed: {response.status_code}")
                    results[api_name][file_key] = { "time": None, "wer": None }
            except Exception as e:
                print(f"{api_name} [{file_key}] exception: {e}")
                results[api_name][file_key] = { "time": None, "wer": None }
# Plotting
file_labels = list(test_files.keys())
api_labels = list(APIS.keys())

# Time comparison chart
plt.figure(figsize=(10, 5))
bar_width = 0.35
x = range(len(file_labels))

for idx, api in enumerate(api_labels):
    times = [results[api][f]["time"] if results[api][f]["time"] else 0 for f in file_labels]
    plt.bar([i + idx*bar_width for i in x], times, width=bar_width, label=api)

plt.xticks([i + bar_width / 2 for i in x], file_labels)
plt.ylabel("Processing Time (s)")
plt.title("API Processing Time per File")
plt.legend()
plt.tight_layout()
plt.savefig("processing_time_comparison.png")
plt.show()

# WER comparison chart
# plt.figure(figsize=(10, 5))
# for idx, api in enumerate(api_labels):
#     wers = [results[api][f]["wer"] if results[api][f]["wer"] is not None else 1.0 for f in file_labels]
#     plt.bar([i + idx*bar_width for i in x], wers, width=bar_width, label=api)
#
# plt.xticks([i + bar_width / 2 for i in x], file_labels)
# plt.ylabel("Word Error Rate")
# plt.title("API WER Comparison per File")
# plt.legend()
# plt.tight_layout()
# plt.savefig("wer_comparison.png")
# plt.show()
