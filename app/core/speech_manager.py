import os
import queue
import time
import pvporcupine
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json

class SpeechManager:
    WAKEWORD="computer"
    LISTEN_DURATION=5
    VOSK_MODEL_PATH="models/vosk-model-en-us-0.22"

    def __init__(self, trancscription_call_back):

        self.audio_q = queue.Queue()
        self.porcupine = None
        self.vosk_model = None
        self.recognizer = None
        self.stream = None

        self.trancscription_call_back = trancscription_call_back

    def __enter__(self):
        # Initialize Porcupine
        self.porcupine = pvporcupine.create(
            keywords=[self.WAKEWORD],
            access_key=os.environ["PICOVOICE_API_KEY"]
        )

        # Initialize Vosk
        self.vosk_model = Model(self.VOSK_MODEL_PATH)
        self.recognizer = KaldiRecognizer(self.vosk_model, 16000)

        # Start audio stream
        self.stream = sd.RawInputStream(
            samplerate=16000,
            blocksize=self.porcupine.frame_length,
            dtype='int16',
            channels=1,
            callback=self.audio_callback
        )
        self.stream.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.stream:
            self.stream.stop()
            self.stream.close()
        if self.porcupine:
            self.porcupine.delete()

    def audio_callback(self, indata, frames, time_info, status):
        self.audio_q.put(bytes(indata))

    def listen(self):
        print(f"Listening for wake word: '{self.WAKEWORD}'...")
        while True:
            pcm = self.audio_q.get()
            pcm_int16 = np.frombuffer(pcm, dtype=np.int16)
            result = self.porcupine.process(pcm_int16)

            if result >= 0:
                print(f"✅ Wake word '{self.WAKEWORD}' detected!")
                transcribed_text = self.transcribe()
                self.trancscription_call_back(transcribed_text)
                print(f"\nListening again for wake word: '{self.WAKEWORD}'...")

    def transcribe(self) -> str:
        print("🎤 Listening for speech...")
        recorded = []
        start_time = time.time()

        while time.time() - start_time < self.LISTEN_DURATION:
            try:
                pcm = self.audio_q.get(timeout=1)
                recorded.append(pcm)
            except queue.Empty:
                break

        audio_bytes = b''.join(recorded)

        if self.recognizer.AcceptWaveform(audio_bytes):
            result = json.loads(self.recognizer.Result())
            transcribed_text = result.get("text", "")

        else:
            transcribed_text = self.recognizer.PartialResult()
            self.recognizer.Result()
        print("Transcribed Text:", transcribed_text)
        return transcribed_text

if __name__ == "__main__":

    import pyttsx3

    

    def say_text(txt):
        print("Transcribed Text:", txt)
        engine = pyttsx3.init()
        engine.say(txt)
        engine.runAndWait()

    try:
        with SpeechManager(say_text) as listener:
            listener.listen()
    except KeyboardInterrupt:
        print("Exiting...")
