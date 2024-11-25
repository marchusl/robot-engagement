import time

import cv2

import ChangeHeadOrientation
import ServerScript
from ServerScript import start_socket_streaming
from Mic_Test import record_audio
from STT_Transcription import transcribe_audio
import TTS_Robot
import ChatGPT_Prompting
import MediapipePre

video = cv2.VideoCapture(0)

# startingPrompt_ChatGPT = ("You are embodying a robot that is communicating verbally and is supposed to help a group of 3-4 students evaluate and build upon their current ideas for a project regarding the main topic 'The Modern Youth'." + 
#                           "You will first listen to each student's pitch of their idea. When every student/participant has done their pitch, you will give feedback in the form of a maximum of 4 key points that can help them improve or build upon their ideas in regards to the main topic. Do this within a maximum of 200 words" +
#                           "Remember to be jolly and motivating when giving this feedback to the students, highlighting interesting points about their individual ideas." +
#                           "Your responses should be in Danish." +
#                           "Do not correlate the student's idea pitch to outside sources too much, but instead refer to overarching sources useful for their general research in coherence with what they said.")

introductionDialogue_qtRobot = "Hej alle sammen! Vi skal spille et idé-genereringsspil! Alle får et minut til at fortælle om deres idé. Personen længst til venstre for mig starter."

#introductionDialogue_qtRobot_TESTING = "Hej vi begynder nu okay."

messagesList_participant_1 = []
messagesList_participant_2 = []
messagesList_participant_3 = []

sorted_participant_IDs = []
faceCenterPixels = []

participant_Amount = 2

# Used for orienting the head
globalCurrentHeadPosition = "neutral"

def main():

    start_socket_streaming()
    print("Beyond start")
    
    # def LookForFaces_ReturnIDs(_duration):
    #     start_time = time.time()  # Get the current time when recording starts
    #     returned_Sorted_IDs = []
    #     while time.time() - start_time < _duration:
    #         temp_Sorted_IDs = MediapipePre.FindFaceAndAssignIDs(video=video)
    #         for id in temp_Sorted_IDs:
    #             returned_Sorted_IDs.append(id)
    #         if time.time() - start_time < _duration:
    #             break
    #         cv2.waitKey(1)
    #     
    #     return returned_Sorted_IDs
    
    # ChatGPT_Prompting.Add_System_Prompt_ChatGPT(startingPrompt_ChatGPT)
    # ChatGPT_Prompting.messages.append(startingPrompt_ChatGPT)
    # Introduction dialogue by QT
    #TTS_Robot.text_to_speech(introductionDialogue_qtRobot_TESTING, 200)
    
    # Participant 1 starting their pitch is announced by QT
    #TTS_Robot.text_to_speech(introductionDialogue_qtRobot, 200)
    
    #sorted_participant_IDs, imageWidth, imageHeight = MediapipePre.FindFaceAndAssignIDs()
    #print(sorted_participant_IDs)
    
    # sorted_participant_IDs = LookForFaces_ReturnIDs(3)
    # final_participant_list = MediapipePre.FindMostOccuringElementValue(sorted_participant_IDs)
    # print(final_participant_list)
    
    
    #video.release()
    #cv2.destroyAllWindows()
    
    
    
    # ROUND 1: PITCH ROUND
    # ------------------------------------------------------------------
    # FIRST PARTICIPANT
    # Record audio using the record_audio function
    ChatGPT_Prompting.Add_System_Prompt_ChatGPT("The first participant is now starting their pitch presentation.")
    print("Starting the audio recording...")
    #saved_audio_file = record_audio(60)  # Records for specified amount of time in seconds in record_audio parameter and returns the saved file path
    # Transcribe the saved audio file
    #print(f"Transcribing the audio file: {saved_audio_file}")
    #transcription = transcribe_audio(saved_audio_file, participant_number=1)  # Pass participant number as needed
    #print("Participant 1 said: " + transcription)
    ChatGPT_Prompting.Add_System_Prompt_ChatGPT("The first participant has now finished their pitch presentation.")
    messagesList_participant_1.append({"role": "user", "content": ("Participant nr. 1 said: " + transcription)}) # Appends what the user just said in their transcription to their chatmessage list of everything they said and what ChatGPT responded to them
    #chatGPTresponse = ChatGPT_Prompting.Simple_PromptChatGPT_ReturnResponse(_promptMessage="Participant nr. 1 said: " + transcription, _messageRole="user")    #Pass participant 1 transcription to chatgpt.
    #TTS_Robot.text_to_speech(chatGPTresponse)
    # ------------------------------------------------------------------ #


    # ROUND 2: DISCUSSION ROUND
    
    #id'er går fra venstre til højre

    input_ask_order = input("RANK ENGAGEMENT NOW (comma separation): ")
    final_ask_order = input_ask_order.split(",")

    #Loop over id in the written order input above, and create and save string commands into variables for use later, so we can easily apply the rotations when each student has been discussed with.
    # The four variables below are strings that should be able to be used as an argument in the set_send_message method in ServerScript.py, so the robot will orient its head correctly.
    first_headOrientation = ""
    second_headOrientation = ""
    third_headOrientation = ""
    fourth_headOrientation = ""

    iterator = 1
    currentlyIteratedOrientation = ""   # Used for storing the head orientation "calculated" in the current for loop iteration, so the next head orientations know which orientation to rotate from.
    for id in final_ask_order:
        nextIdLocation = ChangeHeadOrientation.define_orientation_by_id(id=id, participation_amount=participant_Amount)
        currentlyIteratedOrientation = nextIdLocation
        
        if iterator == 1:
            if nextIdLocation == "neutral":
                first_headOrientation = "QT/neutral"
            else:
                first_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("look", currentPosition=globalCurrentHeadPosition, newPosition=nextIdLocation)

        if iterator == 2:
            if nextIdLocation == "neutral":
                second_headOrientation = "QT/neutral"
            else:
                second_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("look", currentPosition=currentlyIteratedOrientation, newPosition=nextIdLocation)

        if iterator == 3:
            if nextIdLocation == "neutral":
                third_headOrientation = "QT/neutral"
            else:
                third_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("look", currentPosition=currentlyIteratedOrientation, newPosition=nextIdLocation)

        if iterator == 4:
            if nextIdLocation == "neutral":
                fourth_headOrientation = "QT/neutral"
            else:
                fourth_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("look", currentPosition=currentlyIteratedOrientation, newPosition=nextIdLocation)

        iterator += 1

    ServerScript.set_send_message(first_headOrientation)
    ServerScript.set_send_message(second_headOrientation)
    ServerScript.set_send_message(third_headOrientation)
    ServerScript.set_send_message(fourth_headOrientation)
            

def setGlobalHeadOrientation(newOrientation):
    global globalCurrentHeadPosition
    globalCurrentHeadPosition = newOrientation

    
if __name__ == "__main__":
    main()
    
    # ----- PLAN FOR MAIN ----- #
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
    

# def LookForFaces_ReturnIDs(_duration):
#     start_time = time.time()  # Get the current time when recording starts
#     returned_Sorted_IDs = []
#     while time.time() - start_time < _duration:
#         temp_Sorted_IDs = MediapipePre.FindFaceAndAssignIDs(video=video)
#         for id in temp_Sorted_IDs:
#             returned_Sorted_IDs.append(id)
#         cv2.waitKey(1)
#         
#     return returned_Sorted_IDs


# def choosePersonToDiscuss(participantNumber):
#    