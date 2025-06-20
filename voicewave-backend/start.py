import time

import ray
from ray import serve

from server import VoiceWaveAPI

# Start Ray
ray.init()

# Start Ray Serve HTTP server
serve.start(
    http_options={"host": "0.0.0.0", "port": 8000}
)

# Bind deployment
deployment = VoiceWaveAPI.bind()

# Serve with route_prefix="/"
serve.run(
    deployment,
    route_prefix="/"
)

print("VoiceWave API is live at http://localhost:8000/")


while True:
    time.sleep(3600)