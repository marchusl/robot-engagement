import pyaudio
from openai import OpenAI

client = OpenAI()

p = pyaudio.PyAudio()
stream = p.open(format=8,
                channels=1,
                rate=23_000,
                output=True)

with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="onyx",
        input="Hej min ven. Jeg savner at fiske med dig.",
        response_format="pcm"
) as response:
    for chunk in response.iter_bytes(1024):
        stream.write(chunk)