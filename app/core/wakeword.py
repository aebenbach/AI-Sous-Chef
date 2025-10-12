import os
import pvporcupine
import sounddevice as sd
import numpy as np

# Create Porcupine instance with built-in keyword
porcupine = pvporcupine.create(keywords=["blueberry"], access_key=os.environ['PICOVOICE_API_KEY'])

# Callback function that runs in real time
def audio_callback(indata, frames, time, status):
    if status:
        print(f"Audio status: {status}")

    # Convert byte buffer to 16-bit integers
    pcm = np.frombuffer(indata, dtype=np.int16)

    # Process frame with Porcupine
    keyword_index = porcupine.process(pcm)
    if keyword_index >= 0:
        print("Wake word detected!")
        # Trigger your action here (e.g., call function)

# Start streaming audio from mic
try:
    with sd.RawInputStream(
        samplerate=porcupine.sample_rate,
        blocksize=porcupine.frame_length,
        dtype="int16",
        channels=1,
        callback=audio_callback
    ):
        print("Listening for wake word... Press Ctrl+C to stop.")
        while True:
            pass
except KeyboardInterrupt:
    print("Stopping...")
finally:
    porcupine.delete()

