from Mic_Test import record_audio
from STT_Transcription import transcribe_audio

def main():
    # Step 1: Record audio using the record_audio function
    print("Starting the audio recording...")
    saved_audio_file = record_audio()  # This now returns the saved file path

    # Step 2: Transcribe the saved audio file
    print(f"Transcribing the audio file: {saved_audio_file}")
    transcribe_audio(saved_audio_file, participant_number=1)  # Pass participant number as needed

if __name__ == "__main__":
    main()

    #Give ID to each participant from left to right by using Mediapipe
    #QTrobot greets participants and introduces itself

    #QTrobot introduces the tasks

    #Idea presentation round starts

    #Participant ID 1 starts
    #Record audio for 60 seconds...
    #Give 5 second countdown when nearing 60 seconds
    #Participant ID 2 starts

    #Participant ID 3 starts

    #Participant ID 4 starts
