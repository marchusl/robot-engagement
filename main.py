from Mic_Test import record_and_transcribe
import ChatGPT_Prompting

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