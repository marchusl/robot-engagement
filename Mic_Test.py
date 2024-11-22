import pyaudio
import wave
import time
import threading
import keyboard

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

# Flag for stopping the recording
stop_recording = False

def check_for_enter():
    global stop_recording
    print("Press Enter to stop recording early...")
    keyboard.wait("enter")  # Wait for Enter key
    stop_recording = True
    print("Enter pressed, stopping recording.")

def record_audio(duration):
    global stop_recording
    frames = []
    start_time = time.time()  # Get the current time when recording starts

    # Start a thread to check for Enter key press
    input_thread = threading.Thread(target=check_for_enter)
    input_thread.daemon = True
    input_thread.start()

    while time.time() - start_time < duration:
        if stop_recording:
            break  # Exit the loop if Enter is pressed

        frame = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(frame)
        ##print(f"Captured frames: {len(frames)}")  # Debugging: show frame count growing

    print("Recording stopped.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded frames to a file
    filename = "output.wav"
    save_audio(frames, filename)

    # Return the path of the saved file
    return filename

def save_audio(frames, filename="output.wav"):
    """ Save the recorded frames to an audio file """
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# Example usage
if __name__ == "__main__":
    saved_audio_file = record_audio(duration=60)  # Set a longer duration if desired
    print(f"Audio saved as {saved_audio_file}")
