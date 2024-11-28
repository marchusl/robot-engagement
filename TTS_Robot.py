import pyaudio
from openai import OpenAI

from ServerScript import set_send_message

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


def text_to_speech_openai(_transcriptionText):
    """Converts the provided text to speech and plays it."""
    p = pyaudio.PyAudio()
    stream = p.open(format=8,
                    channels=1,
                    rate=22750,
                    output=True)
    
    try:
        print(f"Starting TTS playback for: {_transcriptionText[:]}...")
        with client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice="nova",      # Nova er nok den bedste. Next best er Alloy og 
            
                input=_transcriptionText,
                response_format="pcm"
        ) as response:
            for chunk in response.iter_bytes(2048):
                stream.write(chunk)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("TTS playback completed.")
        

def text_to_speech_robotlocal(_transcriptionText):
    set_send_message("[TALK] " + _transcriptionText)
    
#text_to_speech_openai("Visdom ligger i at forstå, at de enkleste sandheder ofte er de mest dybsindige. Menneskets søgen efter mening er en rejse, ikke en destination, og svarene findes sjældent uden for os selv, men dybt i vores indre.")
#text_to_speech_openai("Hej alle sammen! Mit navn er Aria, og jeg er her i dag for at hjælpe jer med idéer til jeres projektarbejde. Jeg vil rigtig godt høre jeres idéer og hjælpe jer på vej med at realisere dem. Som den første del af opgaven får I et minut til at skrive så mange idéer ned som muligt, hvor I så skal udvælge jeres bedste idé. Til sidst skal I præsentere for resten af gruppen. "
                      #"Tiden begynder om Tre... To... En... Nu.")