from Mic_Test import record_and_transcribe

def main():
    participant_number = 1
    print("Program started. Press '0' during recording to exit.")

    while True:
        should_exit = record_and_transcribe(participant_number)
        if should_exit:
            print("Exiting program. Goodbye!")
            break
        participant_number += 1
        print(f"Moving to participant {participant_number}...")


if __name__ == "__main__":
    main()