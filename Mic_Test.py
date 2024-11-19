import pyaudio
import wave
import datetime
import threading
from pydub import AudioSegment
import os

def record_audio_to_mp3(participant_number):
    # Define the directory to save audio files
    directory = "audios"
    os.makedirs(directory, exist_ok=True)

    # Audio configuration
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

    def record():
        print(f"Recording for participant {participant_number}... Press Enter to save and stop recording.")
        while not stop_event.is_set():
            data = stream.read(chunk_size)
            frames.append(data)

    def save_current_audio():
        nonlocal frames
        if not frames:
            return

        # Generate filenames including participant number
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        wav_filename = os.path.join(directory, f"participant{participant_number}_recording_{timestamp}.wav")
        mp3_filename = wav_filename.replace(".wav", ".mp3")

        # Save the frames as a WAV file
        with wave.open(wav_filename, 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(audio.get_sample_size(audio_format))
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(frames))

        print(f"Saved temporary WAV recording as {wav_filename}")

        # Convert the WAV file to MP3
        audio_segment = AudioSegment.from_wav(wav_filename)
        audio_segment.export(mp3_filename, format="mp3")
        print(f"Converted recording to MP3 as {mp3_filename}")

        # Delete the WAV file
        os.remove(wav_filename)
        print(f"Temporary WAV file {wav_filename} deleted.")

        # Clear frames after saving
        frames = []

        return mp3_filename  # Return the MP3 file path for transcription

    # Start the recording thread
    recording_thread = threading.Thread(target=record)
    recording_thread.start()

    try:
        input("Press Enter to save and stop recording for the current participant...\n")
        stop_event.set()
        recording_thread.join()

        # Save audio and return the file path
        return save_current_audio()

    finally:
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        print("Recording stopped and all audio saved.")
