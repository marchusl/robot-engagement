import time

import cv2

import ChangeHeadOrientation
from ServerScript import set_send_message, send_message, start_socket_streaming
from Mic_Test import record_audio
from STT_Transcription import transcribe_audio
import TTS_Robot
import ChatGPT_Prompting
import MediapipePre


video = cv2.VideoCapture(0)

startingPrompt_ChatGPT = ("You are embodying a robot that is communicating verbally and is supposed to help a group of 3-4 students evaluate and build upon their current ideas for a project regarding the main topic 'The Modern Youth'." + 
                          "You will first listen to each student's pitch of their idea. When every student/participant has done their pitch, you will give feedback in the form of a maximum of 4 key points that can help them improve or build upon their ideas in regards to the main topic. Do this within a maximum of 200 words" +
                          "Remember to be jolly and motivating when giving this feedback to the students, highlighting interesting points about their individual ideas." +
                          "Your responses should be in Danish." +
                          "Do not correlate the student's idea pitch to outside sources too much, but instead refer to overarching sources useful for their general research in coherence with what they said.")

introductionDialogue_qtRobot = "Hej alle sammen! Vi skal spille et idé-genereringsspil! Alle får et minut til at fortælle om deres idé. Personen længst til venstre for mig starter."

#introductionDialogue_qtRobot_TESTING = "Hej vi begynder nu okay."

messagesList_participant_1 = []
messagesList_participant_2 = []
messagesList_participant_3 = []
messagesList_participant_4 = []

pitch_firstPitchDone = bool
pitch_secondPitchDone = bool
pitch_thirdPitchDone = bool
pitch_fourthPitchDone = bool

sorted_participant_IDs = []
faceCenterPixels = []

participant_Amount = 4

# Used for orienting the head
globalCurrentHeadPosition = "neutral"   # The middle input in the action string sent through socketstreaming.

def main():
    
    global globalCurrentHeadPosition
    
    start_socket_streaming()
    print("Beyond start")
    input("Start Experience by pressing enter")
    
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
    # ChatGPT_Prompting.allMessages.append(startingPrompt_ChatGPT)
    
    #Testing Introduction dialogue by QT
    #TTS_Robot.text_to_speech(introductionDialogue_qtRobot_TESTING, 200)
    
    # Participant 1 starting their pitch is announced by QT
    # TTS_Robot.text_to_speech(introductionDialogue_qtRobot)
    
    #sorted_participant_IDs, imageWidth, imageHeight = MediapipePre.FindFaceAndAssignIDs()
    #print(sorted_participant_IDs)
    
    # sorted_participant_IDs = LookForFaces_ReturnIDs(3)
    # final_participant_list = MediapipePre.FindMostOccuringElementValue(sorted_participant_IDs)
    # print(final_participant_list)
    
    
    #video.release()
    #cv2.destroyAllWindows()
    
    
    
    # ROUND 1: PITCH ROUND
    # ------------------------------------------------------------------
    # _______________FIRST PARTICIPANT_________________
    if participant_Amount <= 1:
        print("ERROR: The amount of participants have to be 2 or more.")
    if participant_Amount >= 2:
        Pitch_StartParticipationRound(firstPrompt="The first participant is now starting their pitch presentation.",
                                      secondPrompt="The first participant has now finished their pitch presentation.",
                                      duration=10,
                                      currentParticipantNumber=1,
                                      messageList=messagesList_participant_1,
                                      roundDoneBool=pitch_firstPitchDone)
        print("FIRST ROUND DONE I GUESS")
        
        Pitch_StartParticipationRound(firstPrompt="The second participant is now starting their pitch presentation.",
                                      secondPrompt="The second participant has now finished their pitch presentation.",
                                      duration=10,
                                      currentParticipantNumber=2,
                                      messageList=messagesList_participant_2,
                                      roundDoneBool=pitch_secondPitchDone)
    if participant_Amount >= 3:
        Pitch_StartParticipationRound(firstPrompt="The third participant is now starting their pitch presentation.",
                                      secondPrompt="The third participant has now finished their pitch presentation.",
                                      duration=10,
                                      currentParticipantNumber=3,
                                      messageList=messagesList_participant_3,
                                      roundDoneBool=pitch_thirdPitchDone)
    if participant_Amount >= 4:
        Pitch_StartParticipationRound(firstPrompt="The fourth participant is now starting their pitch presentation.",
                                      secondPrompt="The fourth participant has now finished their pitch presentation.",
                                      duration=10,
                                      currentParticipantNumber=4,
                                      messageList=messagesList_participant_4,
                                      roundDoneBool=pitch_fourthPitchDone)
    
    
    
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

    iterator = 0
    currentlyIteratedOrientation = ""   # Used for storing the head orientation "calculated" in the current for loop iteration, so the next head orientations know which orientation to rotate from.
    for id in final_ask_order:
        nextIdLocation = ChangeHeadOrientation.define_orientation_by_id(id=id, participation_amount=participant_Amount)
        
        if iterator == 0:
            if nextIdLocation == "neutral":
                first_headOrientation = ChangeHeadOrientation.NeutralPointing(id, participant_Amount)
            else:
                first_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("lookpoint", currentPosition=globalCurrentHeadPosition, newPosition=nextIdLocation)
                

        if iterator == 1:
            if nextIdLocation == "neutral":
                second_headOrientation = ChangeHeadOrientation.NeutralPointing(id, participant_Amount)
            else:
                second_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("lookpoint", currentPosition=currentlyIteratedOrientation, newPosition=nextIdLocation)


        if iterator == 2:
            if nextIdLocation == "neutral":
                third_headOrientation = ChangeHeadOrientation.NeutralPointing(id, participant_Amount)
            else:
                third_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("lookpoint", currentPosition=currentlyIteratedOrientation, newPosition=nextIdLocation)

        if iterator == 3:
            if nextIdLocation == "neutral":
                fourth_headOrientation = ChangeHeadOrientation.NeutralPointing(id, participant_Amount)
            else:
                fourth_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("lookpoint", currentPosition=currentlyIteratedOrientation, newPosition=nextIdLocation)
        currentlyIteratedOrientation = nextIdLocation
        iterator += 1
    print(first_headOrientation)
    print(second_headOrientation)
    print(third_headOrientation)
    print(fourth_headOrientation)
    
    
    
    set_send_message(first_headOrientation)
    time.sleep(1.5)
    set_send_message(second_headOrientation)
    time.sleep(1.5)
    set_send_message(third_headOrientation)
    time.sleep(1.5)
    set_send_message(fourth_headOrientation)
    time.sleep(1.5)
    
    # while send_message == False:
    #     set_send_message(second_headOrientation)
    # while send_message == False:
    #     set_send_message(third_headOrientation)
    # while send_message == False:
    #     set_send_message(fourth_headOrientation)
            

def setGlobalHeadOrientation(newOrientation):
    global globalCurrentHeadPosition
    globalCurrentHeadPosition = newOrientation

def Pitch_StartParticipationRound(firstPrompt, secondPrompt, currentParticipantNumber, messageList, duration, roundDoneBool):
    roundDoneBool = False
    ChatGPT_Prompting.Add_System_Prompt_ChatGPT(firstPrompt)
    # Record audio using the record_audio function
    print("Starting the audio recording...")
    saved_audio_file = record_audio(duration)  # Records for specified amount of time in seconds in record_audio parameter and returns the saved file path

    # Transcribe the saved audio file
    #print(f"Transcribing the audio file: {saved_audio_file}")
    transcription = transcribe_audio(saved_audio_file, participant_number=currentParticipantNumber)  # Pass participant number as needed
    print("Participant " + str(currentParticipantNumber) + " said: " + transcription)
    ChatGPT_Prompting.Add_System_Prompt_ChatGPT(secondPrompt)
    messageList.append({"role": "user", "content": ("Participant nr. " + str(currentParticipantNumber) + " said: " + transcription)}) # Appends what the user just said in their transcription to their chatmessage list of everything they said and what ChatGPT responded to them

    chatGPTresponse = ChatGPT_Prompting.Simple_PromptChatGPT_ReturnResponse(_promptMessage="Participant nr. " + str(currentParticipantNumber) + " said: " + transcription, _messageRole="user")    #Pass participant 1 transcription to chatgpt.
    messageList.append({"role": "user", "content": ("Robot response: " + chatGPTresponse)})

    # Make TTS Openai request
    # TTS_Robot.text_to_speech(chatGPTresponse)
    set_send_message("[TALK] " + chatGPTresponse)
    roundDoneBool = True
    
    
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