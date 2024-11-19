from Mic_Test import record_audio_to_mp3
from STT_Transcription import transcribe_audio

def main():
    participant_number = 1  # Start with participant 1

    while True:
        print(f"Starting recording for participant {participant_number}")

        # Record the audio and get the file path of the saved MP3
        audio_file_path = record_audio_to_mp3(participant_number)

        if audio_file_path:
            print(f"Recording complete. Transcribing audio for participant {participant_number}...")

            # Transcribe the recorded audio
            transcribe_audio(audio_file_path, participant_number)

        # Increment participant number
        participant_number += 1
        print(f"Ready for next participant. Press Enter to start or type 'exit' to stop.")

        # Check if the user wants to exit
        exit_prompt = input().strip().lower()
        if exit_prompt == "exit":
            print("Exiting program.")
            break


if __name__ == "__main__":
    main()
