import pyaudio
from openai import OpenAI

client = OpenAI()

# p = pyaudio.PyAudio()
# stream = p.open(format=8,
#                 channels=1,
#                 rate=23_000,
#                 output=True)
# 
# with client.audio.speech.with_streaming_response.create(
#         model="tts-1",
#         voice="onyx",
#         input=_transcriptionText,
#         response_format="pcm"
# ) as response:
#     for chunk in response.iter_bytes(1024):
#         stream.write(chunk)


def text_to_speech(_transcriptionText):
    """Converts the provided text to speech and plays it."""
    p = pyaudio.PyAudio()
    stream = p.open(format=8,
                    channels=1,
                    rate=23000,
                    output=True)
    
    try:
        print(f"Starting TTS playback for: {_transcriptionText[:]}...")
        with client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice="nova",      # Nova er nok den bedste. Next best er Alloy og Onyx
                input=_transcriptionText,
                response_format="pcm"
        ) as response:
            for chunk in response.iter_bytes(1024):
                stream.write(chunk)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("TTS playback completed.")