from openai import OpenAI
import os
import datetime

client = OpenAI()

def transcribe_audio(file_path, participant_number):
    """ Transcribe the audio file using OpenAI's Whisper model. """
    # Ensure the transcription directory exists
    transcription_dir = "transcriptionFiles"
    os.makedirs(transcription_dir, exist_ok=True)

    try:
        # Open the audio file for transcription
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="da"
            )

        # Save the transcription to a text file named by participant number
        text_filename = os.path.join(transcription_dir, f"participant{participant_number}_transcription.txt")
        with open(text_filename, "a", encoding="utf-8") as text_file:
            text_file.write(transcription.text + "\n")
        
        print(f"Transcription saved to {text_filename}")
        
        return transcription.text

    except Exception as e:
        print(f"Error during transcription: {e}")

def saveFullDiscussion(fullList):
    my_list = fullList
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.txt"
    with open(filename, "w") as file:
        for line in my_list:
            file.write(line + "\n")

    print(f"File saved as: {filename}")
