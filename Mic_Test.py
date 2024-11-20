import pyaudio
import wave
import datetime
import threading
import os
from openai import OpenAI

client = OpenAI()


def transcribe_audio(file_path, participant_number):
    # Ensure the transcription directory exists
    transcription_dir = "transcriptionFiles"
    os.makedirs(transcription_dir, exist_ok=True)

    # Open the audio file for transcription
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    # Save the transcription to a text file (overwrite for each participant)
    text_filename = os.path.join(transcription_dir, f"participant{participant_number}_transcription.txt")
    with open(text_filename, "w", encoding="utf-8") as text_file:  # "w" ensures the file is overwritten
        text_file.write(transcription.text + "\n")

    print(f"Transcription saved to {text_filename}")


def record_and_transcribe(participant_number):
    # Directories
    audio_dir = "audios"
    os.makedirs(audio_dir, exist_ok=True)

    # Audio settings
    sample_rate = 16000
    chunk_size = 1024
    channels = 1
    audio_format = pyaudio.paInt16

    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio_format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    frames = []
    stop_event = threading.Event()
    exit_event = threading.Event()

    def record():
        print(f"Recording for participant {participant_number}... Press '0' to exit.")
        while not stop_event.is_set() and not exit_event.is_set():
            data = stream.read(chunk_size)
            frames.append(data)

    def monitor_exit():
        while not stop_event.is_set():
            user_input = input("Press '0' to exit or Enter to stop recording:\n").strip()
            if user_input == "0":
                print("Exit signal detected.")
                exit_event.set()
                stop_event.set()
                break
            elif user_input == "":
                stop_event.set()

    # Start threads
    recording_thread = threading.Thread(target=record)
    exit_thread = threading.Thread(target=monitor_exit)
    recording_thread.start()
    exit_thread.start()

    # Wait for threads to finish
    recording_thread.join()
    exit_thread.join()

    # Handle exit signal
    if exit_event.is_set():
        return True

    # Save audio if recording was stopped
    if frames:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        wav_filename = os.path.join(audio_dir, f"participant{participant_number}_recording_{timestamp}.wav")

        # Save WAV file
        with wave.open(wav_filename, 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(audio.get_sample_size(audio_format))
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(frames))

        print(f"Saved WAV recording as {wav_filename}")

        # Transcribe audio directly from the WAV file
        transcribe_audio(wav_filename, participant_number)

    # Clean up audio resources
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Recording stopped and transcription completed.")
    return False  # Continue program
