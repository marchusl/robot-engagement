from Mic_Test import record_audio
from STT_Transcription import transcribe_audio
import TTS_Robot
import ChatGPT_Prompting

# startingPrompt_ChatGPT = ("You are embodying a robot that is supposed to help a group of 3-4 students evaluate and build upon their current ideas for a project regarding the main topic 'The Modern Youth'." + 
#                           "You will first listen to each student's pitch of their idea. When every student/participant has done their pitch, you will give feedback in the form of a maximum of 4 key points that can help them improve or build upon their ideas in regards to the main topic. Do this within a maximum of 200 words" +
#                           "Remember to be jolly and motivating when giving this feedback to the students, highlighting interesting points about their individual ideas." +
#                           "Your responses should be in Danish." +
#                           "Do not correlate the student's idea pitch to outside sources too much, but instead refer to overarching sources useful for their general research in coherence with what they said.")

introductionDialogue_qtRobot = "Hej alle sammen! Vi skal spille et idé-genereringsspil! Alle får et minut til at fortælle om deres idé. Personen længst til venstre for mig starter."

#introductionDialogue_qtRobot_TESTING = "Hej vi begynder nu okay."

messagesList_participant_1 = []
messagesList_participant_2 = []
messagesList_participant_3 = []

def main():
    # ChatGPT_Prompting.Add_System_Prompt_ChatGPT(startingPrompt_ChatGPT)
    # ChatGPT_Prompting.messages.append(startingPrompt_ChatGPT)
    # Introduction dialogue by QT
    #TTS_Robot.text_to_speech(introductionDialogue_qtRobot_TESTING, 200)
    
    # Participant 1 starting their pitch is announced by QT
    #TTS_Robot.text_to_speech(introductionDialogue_qtRobot, 200)
    
    # ROUND 1: FIRST PARTICIPANT
    # ------------------------------------------------------------------
    # Record audio using the record_audio function
    ChatGPT_Prompting.Add_System_Prompt_ChatGPT("The first participant is now starting their pitch presentation.")
    print("Starting the audio recording...")
    saved_audio_file = record_audio(5)  # Records for specified amount of time in seconds in record_audio parameter and returns the saved file path
    # Transcribe the saved audio file
    print(f"Transcribing the audio file: {saved_audio_file}")
    transcription = transcribe_audio(saved_audio_file, participant_number=1)  # Pass participant number as needed
    print("Participant 1 said: " + transcription)
    ChatGPT_Prompting.Add_System_Prompt_ChatGPT("The first participant has now finished their pitch presentation.")
    messagesList_participant_1.append({"role": "user", "content": ("Participant nr. 1 said: " + transcription)}) # Appends what the user just said in their transcription to their chatmessage list of everything they said and what ChatGPT responded to them
    chatGPTresponse = ChatGPT_Prompting.Simple_PromptChatGPT_ReturnResponse(_promptMessage="Participant nr. 1 said: " + transcription, _messageRole="user")    #Pass participant 1 transcription to chatgpt.
    TTS_Robot.text_to_speech(chatGPTresponse, 200)
    # ------------------------------------------------------------------ #
    
    
    
    

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
