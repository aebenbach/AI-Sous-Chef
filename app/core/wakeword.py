
import os
import queue
import time
import pvporcupine
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json

# === CONFIG ===
WAKEWORD = "jarvis"
LISTEN_DURATION = 5  # seconds to listen after wake word
VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"

# === Wake Word Detector ===
porcupine = pvporcupine.create(keywords=[WAKEWORD], access_key=os.environ['PICOVOICE_API_KEY'])

# === Vosk Model ===
vosk_model = Model(VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(vosk_model, 16000)

# === Queues ===
audio_q = queue.Queue()

# === Audio Callback ===
def audio_callback(indata, frames, time_info, status):
    audio_q.put(bytes(indata))

# === Wake Word Listening Loop ===
def listen_for_wake_word():
    with sd.RawInputStream(samplerate=16000, blocksize=porcupine.frame_length,
                           dtype='int16', channels=1, callback=audio_callback):
        print(f"Listening for wake word: '{WAKEWORD}'...")

        while True:
            pcm = audio_q.get()
            pcm_int16 = np.frombuffer(pcm, dtype=np.int16)
            result = porcupine.process(pcm_int16)

            if result >= 0:
                print(f"✅ Wake word '{WAKEWORD}' detected!")
                transcribe_with_vosk()
                print(f"\nListening again for wake word: '{WAKEWORD}'...")

# === Transcription ===
def transcribe_with_vosk():
    print("🎤 Listening for speech...")
    recorded = []

    start_time = time.time()
    while time.time() - start_time < LISTEN_DURATION:
        try:
            pcm = audio_q.get(timeout=1)
            recorded.append(pcm)
        except queue.Empty:
            break

    audio_bytes = b''.join(recorded)

    # Feed to Vosk recognizer
    if recognizer.AcceptWaveform(audio_bytes):
        result = json.loads(recognizer.Result())
        print("📝 Transcription:", result.get("text", ""))
    else:
        print("📝 Partial:", recognizer.PartialResult())

# === Main ===
if __name__ == "__main__":
    try:
        listen_for_wake_word()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        porcupine.delete()

