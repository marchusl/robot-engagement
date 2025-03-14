import time

#import cv2
#import MediapipePre

import ChangeHeadOrientation
import STT_Transcription
from ServerScript import set_send_message, send_message, start_socket_streaming
import ServerScript
from Mic_Test import record_audio
from STT_Transcription import transcribe_audio
import TTS_Robot
import ChatGPT_Prompting



#video = cv2.VideoCapture(0)
                            #-------------------------------------The starting prompt used for instructing the ChatGPT API instance at the start of the experience-------------------------------#
startingPrompt_ChatGPT = ("You are embodying a robot that is communicating verbally and is supposed to help a group of 3-4 students evaluate and build upon their current ideas for a project regarding the main topic 'Den Moderne Ungdom'." + 
                          "You will first listen to each student's pitch of their idea. When every student/participant has done their pitch, you will give feedback that can help them improve or build upon their ideas in regards to the main topic. Do this within a maximum of 100 words." +
                          "Remember to be jolly and motivating when giving this feedback to the students, highlighting interesting points about their individual ideas." +
                          "Your responses should be in Danish. Your feedback cannot ask further questions, since it is final statement to their statement, therefore only rhetorical or reflective questions are allowed that can help the participant in deeper reflection of their idea(s)." +
                          "Do not correlate the student's idea pitch to outside sources too much, but instead refer to overarching sources useful for their general research in coherence with what they said.")

introductionDialogue_qtRobot = ("Hej alle sammen! Mit navn er Aria, og jeg er her i dag for at hjælpe jer med idéer til jeres projektarbejde. Jeg vil rigtig godt høre jeres idéer og hjælpe jer på vej med at realisere dem. Som den første del af vores tid sammen, får I et minut til at skrive så mange idéer ned som muligt, hvor I så skal udvælge jeres yndlings-idé. Til sidst skal I præsentere for resten af gruppen. "
                                "Tiden begynder om tre... To... En... Nu.")

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

allMessages_TranscriptionList = []

participant_Amount = 4

# Used for orienting the head
globalCurrentHeadPosition = "neutral"   # The middle input in the action string sent through socketstreaming.

def main():
    
    global globalCurrentHeadPosition
    
    start_socket_streaming()
    #print("Beyond start")
    input("Start Experience by pressing enter")
    set_send_message("[GESTURE] QT/neutral")
    print("service_in_progress: " + str(ServerScript.service_in_progress))
    while ServerScript.service_in_progress:
        pass
    
    #brainstormingIntroductionDialogue = "Hej allesammen! "
    #TTS_Robot.text_to_speech_openai(brainstormingIntroductionDialogue)
    #TTS_Robot.text_to_speech_robotlocal(brainstormingIntroductionDialogue)
    
    
    ChatGPT_Prompting.Add_System_Prompt_ChatGPT(startingPrompt_ChatGPT)
    #TTS_Robot.text_to_speech_robotlocal(introductionDialogue_qtRobot)
    allMessages_TranscriptionList.append("Robot response: " + introductionDialogue_qtRobot)
    
    # Introduce the robot and the concept of this learning/ideation session.
    set_send_message("[TALK] " + introductionDialogue_qtRobot)
    TTS_Robot.text_to_speech_openai(introductionDialogue_qtRobot)
    while ServerScript.service_in_progress:
        pass
    
    set_send_message("[GESTURE] QT/happy")
    
    time.sleep(62)  # Time set for brainstorming in seconds
        

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
    
    
    
    
    # --------------------- FIRST HALF OF EXPERIENCE: PITCH ROUND ---------------------------------------------

    ask_order = ""  # Variable used for storing the string containing the order in which the robot should talk to participants in the discussion.
    
    #-------Used for asserting in which order the robot should ask and point, starting from its left going right - depending on the amount of participants--------#
    if participant_Amount == 2:
        ask_order = "1,2"
    if participant_Amount == 3:
        ask_order = "1,2,3"
    if participant_Amount == 4:
        ask_order = "1,2,3,4"

    ask_order = ask_order.split(",")
    first_headOrientation, second_headOrientation, third_headOrientation, fourth_headOrientation = Generate_Head_Orientations(ask_order, participant_Amount)

    PitchIntroductionDialogue_qtRobot = ("Så er tiden desvære gået. Nu glæder jeg mig super meget til at høre jeres idéer. "
                                         "Vi starter fra min venstre side og kører mod højre. Når jeg peger på jer, så har I ét minut til at forklare jeres valgte idé til gruppen, "
                                         "hvorefter vi går videre til den næste indtil alle har fortalt om deres idé.")
    allMessages_TranscriptionList.append("Robot response: " + PitchIntroductionDialogue_qtRobot)
    
    set_send_message("[TALK] " + PitchIntroductionDialogue_qtRobot)
    TTS_Robot.text_to_speech_openai(PitchIntroductionDialogue_qtRobot)
    while ServerScript.service_in_progress:
        pass
    
    if participant_Amount <= 1:
        print("ERROR: The amount of participants have to be 2 or more.")
        
    if participant_Amount >= 2:
        
        #----------------------- FIRST PARTICIPANT ----------------------#
        set_send_message(first_headOrientation)
        while ServerScript.service_in_progress:
            pass
            
        #setGlobalHeadOrientation(first_headOrientation)
        # Introduce the participant
        _introduceParticipantDialogue = "Først vil jeg gerne høre hvad du har tænkt over. Du må gerne begynde nu."
        allMessages_TranscriptionList.append("Robot response: " + _introduceParticipantDialogue)
        set_send_message("[TALK] " + _introduceParticipantDialogue)
        TTS_Robot.text_to_speech_openai(_introduceParticipantDialogue)
        while ServerScript.service_in_progress:
            pass
        
        set_send_message("[NOD] nod-" + ServerScript.current_head_position)
        
        Pitch_StartParticipationRound(firstPrompt="The first participant is now starting their pitch presentation.",    # Prompt used to tell ChatGPT API instance, the chronological time 
                                                                                                                        # that the participant starts talking, which is sent as the context window.
                                      secondPrompt="The first participant has now finished their pitch presentation.",  # Tells the ChatGPT API instance that the participant has finished talking.
                                      duration=60,                                                                      # Duration of the time the ChatGPT instance listens to the participant (Can be manually triggered by pressing SPACE)
                                      currentParticipantNumber=1,                                                       # Participant number is used for labelling input from participants, so as to know who said what.
                                      messageList=messagesList_participant_1,                                           # The message structure list instance which is used to store each participant's conversations with the robot.
                                      roundDoneBool=pitch_firstPitchDone)                                               # Flips a bool in order to confirm the end of a pitch round.
        while ServerScript.service_in_progress:
            pass
        
        #---------------------- SECOND PARTICIPANT ----------------------#
        set_send_message(second_headOrientation)
        while ServerScript.service_in_progress:
            pass
        
        #setGlobalHeadOrientation(second_headOrientation)
        # Introduce the participant
        _introduceParticipantDialogue = "Og nu skal vi videre og høre hvad du har tænkt på. Du må gerne begynde nu."
        allMessages_TranscriptionList.append("Robot response: " + _introduceParticipantDialogue)
        set_send_message("[TALK] " + _introduceParticipantDialogue)
        TTS_Robot.text_to_speech_openai(_introduceParticipantDialogue)
        while ServerScript.service_in_progress:
            pass
        
        set_send_message("[NOD] nod-" + ServerScript.current_head_position)
        
        #------------Refer to code explanation starting line 161------------#
        Pitch_StartParticipationRound(firstPrompt="The second participant is now starting their pitch presentation.",   
                                      secondPrompt="The second participant has now finished their pitch presentation.",
                                      duration=60,
                                      currentParticipantNumber=2,
                                      messageList=messagesList_participant_2,
                                      roundDoneBool=pitch_secondPitchDone)
        while ServerScript.service_in_progress:
            pass
        
        
    if participant_Amount >= 3:

        #---------------------- THIRD PARTICIPANT ----------------------#
        set_send_message(third_headOrientation)
        while ServerScript.service_in_progress:
            pass
        #setGlobalHeadOrientation(third_headOrientation)
        # Introduce the participant
        _introduceParticipantDialogue = "Så blev det DIN tur til at fortælle om din sikkert spændende idé. Du kan bare begynde."
        allMessages_TranscriptionList.append("Robot response: " + _introduceParticipantDialogue)
        set_send_message("[TALK] " + _introduceParticipantDialogue)
        TTS_Robot.text_to_speech_openai(_introduceParticipantDialogue)
        while ServerScript.service_in_progress:
            pass
        set_send_message("[NOD] nod-" + ServerScript.current_head_position)
        Pitch_StartParticipationRound(firstPrompt="The third participant is now starting their pitch presentation.",
                                      secondPrompt="The third participant has now finished their pitch presentation.",
                                      duration=60,
                                      currentParticipantNumber=3,
                                      messageList=messagesList_participant_3,
                                      roundDoneBool=pitch_thirdPitchDone)
        while ServerScript.service_in_progress:
            pass
        
        
    if participant_Amount >= 4:
        
        #---------------------- FOURTH PARTICIPANT ----------------------#
        set_send_message(fourth_headOrientation)
        while ServerScript.service_in_progress:
            pass
        #setGlobalHeadOrientation(fourth_headOrientation)
        # Introduce the participant
        _introduceParticipantDialogue = "Sidst men ikke mindst skal vi høre hvad DU har tænkt på. Du må gerne begynde nu."
        allMessages_TranscriptionList.append("Robot response: " + _introduceParticipantDialogue)
        set_send_message("[TALK] " + _introduceParticipantDialogue)
        TTS_Robot.text_to_speech_openai(_introduceParticipantDialogue)
        while ServerScript.service_in_progress:
            pass
        set_send_message("[NOD] nod-" + ServerScript.current_head_position)
        Pitch_StartParticipationRound(firstPrompt="The fourth participant is now starting their pitch presentation.",
                                      secondPrompt="The fourth participant has now finished their pitch presentation.",
                                      duration=60,
                                      currentParticipantNumber=4,
                                      messageList=messagesList_participant_4,
                                      roundDoneBool=pitch_fourthPitchDone)
        while ServerScript.service_in_progress:
            pass
        
        
    
    
    
    # ------------------------------------------------- End of PITCH ROUND -------------------------------------------------------------------------------------------- #
    
    set_send_message("[GESTURE] QT/neutral")
    while ServerScript.service_in_progress:
        pass

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
    
    first_headOrientation, second_headOrientation, third_headOrientation, fourth_headOrientation = Generate_Head_Orientations(final_ask_order, participant_Amount)
    
    print(first_headOrientation)
    print(second_headOrientation)
    print(third_headOrientation)
    print(fourth_headOrientation)
    
    _introduceDiscussionRoundDialogue = "Tak for alle jeres spændende idéer! Nu kunne jeg godt tænke mig at vi gik lidt mere i dybden med jeres forslag og potentielt få jer til at overveje hvordan I kunne arbejde videre med dem i jeres projekter."
    allMessages_TranscriptionList.append(_introduceDiscussionRoundDialogue)
    #Introducing the Discussion Round
    set_send_message("[TALK] " + _introduceDiscussionRoundDialogue)
    TTS_Robot.text_to_speech_openai(_introduceDiscussionRoundDialogue)
    while ServerScript.service_in_progress:
        pass
    
    ChatGPT_Prompting.Add_System_Prompt_ChatGPT("Now all participants have given their idea pitch from their brainstorming session. "
                                                "It is now time to discuss the participants' individual ideas together. You are the facilitator of the discussion who will be firstly summarizing their idea pitch followed by asking one question to each participant. "
                                                "The question will have to relate to the general topic 'Den moderne ungdom', and the other participants' ideas. It should also be contained within 100 words. "
                                                "Only refer to the participants by what they have said, and do NOT use words like 'participant' or their participant numbers. Formulate yourself in Danish."
                                                "You will be able to ask the question in four different ways, which are as follows: "
                                                "'Linking' - Link two ideas together. "
                                                "'Hypothetical' - Reflect on the idea in another context. "
                                                "'Cause and effect' - Reflect on the specific causes and effects of the idea. "
                                                "'Extension' - Further explain how the idea would work in practice. ")
    
    #participantIntroductionText = ""
    
    # # First participant in Discussion Round
    # set_send_message(first_headOrientation)
    # while ServerScript.service_in_progress:
    #     pass
    # 
    # TTS_Robot.text_to_speech_openai("PLACEHOLDER TEXT FOR TELLING THIS PARTICIPANT THAT THEY ARE THE FIRST ONE TO START")
    # TTS_Robot.text_to_speech_robotlocal("PLACEHOLDER TEXT FOR TELLING THIS PARTICIPANT THAT THEY ARE THE FIRST ONE TO START")
    # while ServerScript.service_in_progress:
    #     pass
    # 
    # chatgptResponse = ChatGPT_Prompting.User_PromptChatGPT_ReturnResponse(messagesList_participant_1, "Participant nr. 1 said: ", "system")
    # TTS_Robot.text_to_speech_openai(chatgptResponse)      # IF OPENAI TTS REQUEST IS MADE BEFORE THE SOCKET STREAM CALL TO THE LOCAL TTS ON THE ROBOT (LIKE HERE), THEN THE VOICE ON THE OPENAI TTS WILL STUTTER A LOT.
    # TTS_Robot.text_to_speech_robotlocal(chatgptResponse)
    # while ServerScript.service_in_progress:
    #     pass
    
    if participant_Amount >= 2:
        # First participant in Discussion Round
        Discussion_StartParticipantRound(_storedHeadOrientation=first_headOrientation,
                                         _participantMessageList=messagesList_participant_1, 
                                         _participantNumber=final_ask_order[0], 
                                         #_participantIntroductionText="Du bliver den første til at starte her i diskussions-runden. Du kan bare begynde.", 
                                         _recordDuration=60,
                                         _questionType="'Linking'")
        time.sleep(1)
        
        # Second participant in Discussion Round
        Discussion_StartParticipantRound(_storedHeadOrientation=second_headOrientation,
                                         _participantMessageList=messagesList_participant_2,
                                         _participantNumber=final_ask_order[1],
                                         #_participantIntroductionText="Så er det din tur til at starte. Du kan bare begynde.",
                                         _recordDuration=60,
                                         _questionType="'Hypothetical'")
        time.sleep(1)
    
    if participant_Amount >= 3:
        # Third participant in Discussion Round
        Discussion_StartParticipantRound(_storedHeadOrientation=third_headOrientation,
                                         _participantMessageList=messagesList_participant_3,
                                         _participantNumber=final_ask_order[2],
                                         #_participantIntroductionText="Og så er det din tur, vi glæder os til at høre hvad du har at sige. Du begynder bare.",
                                         _recordDuration=60,
                                         _questionType="'Cause and effect'")
        time.sleep(1)
    if participant_Amount >= 4:
        # Fourth participant in Discussion Round
        Discussion_StartParticipantRound(_storedHeadOrientation=fourth_headOrientation,
                                         _participantMessageList=messagesList_participant_4,
                                         _participantNumber=final_ask_order[3],
                                         #_participantIntroductionText="Sidste men ikke mindst, så er det dig! Du kan bare begynde.",
                                         _recordDuration=60,
                                         _questionType="'Extension'")
        time.sleep(1)
    
    
    
    
    # while send_message == False:
    #     set_send_message(second_headOrientation)
    # while send_message == False:
    #     set_send_message(third_headOrientation)
    # while send_message == False:
    #     set_send_message(fourth_headOrientation)
    
    # Conclude the whole session with the robot giving a small conclusion and summary for actions to go with henceforth from feedback given.
    Conclude_Session()
    
    # Save the transcript of the whole session
    STT_Transcription.saveFullDiscussion(allMessages_TranscriptionList)
    
    
    
    
    
    
#------------------------------------------------------------------------------------------------------ END OF MAIN DEF ----------------------------------------------------------------------------------------------------------------------------------------








def setGlobalHeadOrientation(newOrientation):
    #newOrientation.find()
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
    allMessages_TranscriptionList.append("Participant nr. " + str(currentParticipantNumber) + " said: " + transcription)
    
    chatGPTresponse = ChatGPT_Prompting.Simple_PromptChatGPT_ReturnResponse(_promptMessage="Participant nr. " + str(currentParticipantNumber) + " said: " + transcription, _messageRole="user")    #Pass participant 1 transcription to chatgpt.
    messageList.append({"role": "user", "content": ("Robot response: " + chatGPTresponse)})
    allMessages_TranscriptionList.append("Robot response: " + chatGPTresponse)

    # Make TTS Openai request
    set_send_message("[TALK] " + chatGPTresponse)
    TTS_Robot.text_to_speech_openai(chatGPTresponse)
    while ServerScript.service_in_progress:
        pass
    roundDoneBool = True
    
    
def Discussion_StartParticipantRound(_storedHeadOrientation, _participantMessageList, _participantNumber, _questionType, _recordDuration):

    set_send_message(_storedHeadOrientation)    # Setting the head orientation for the robot
    while ServerScript.service_in_progress:
        pass
    
    _participantFeedback = ChatGPT_Prompting.Simple_PromptChatGPT_ReturnResponse(_promptMessage="You are now talking to Participant " + _participantNumber + ". Quickly summarize their pitch (less than 30 words) and then ask one " + _questionType + " question based on their pitch in relation to the pitches from the other participants.", 
                                                                                        _messageRole="system")
    allMessages_TranscriptionList.append("Robot response: " + _participantFeedback)
    
    set_send_message("[TALK] " + _participantFeedback)
    TTS_Robot.text_to_speech_openai(_participantFeedback)
    while ServerScript.service_in_progress:
        pass

    set_send_message("[NOD] nod-" + ServerScript.current_head_position)     # Make the robot nod in affirmation to what is said.
    #AUDIO RECORDING
    print("Starting the audio recording...")
    saved_audio_file = record_audio(_recordDuration)  # Records for specified amount of time in seconds in record_audio parameter and returns the saved file path

    # Transcribe the saved audio file
    #print(f"Transcribing the audio file: {saved_audio_file}")
    transcription = transcribe_audio(saved_audio_file, participant_number=_participantNumber)  # Pass participant number as needed
    print("Participant " + str(_participantNumber) + " said: " + transcription)
    #END OF AUDIO RECORDING
    
    ChatGPT_Prompting.Add_System_Prompt_ChatGPT("The participant has now answered your question. Make a simple affirming answer to their statement, recognizing what they said, but without asking further questions until prompted to do so.")
    
    _participantMessageList.append({"role": "user", "content": ("Participant nr. " + str(_participantNumber) + " said: " + transcription)}) # Appends what the user just said in their transcription to their chatmessage list of everything they said and what ChatGPT responded to them
    allMessages_TranscriptionList.append("Participant nr. " + str(_participantNumber) + " said: " + transcription)
    
    chatgptResponse_1 = ChatGPT_Prompting.Simple_PromptChatGPT_ReturnResponse(_promptMessage="Participant nr. " + str(_participantNumber) + " said: " + transcription, _messageRole="user")
    _participantMessageList.append({"role": "assistant", "content": ("Robot response: " + chatgptResponse_1)})
    allMessages_TranscriptionList.append("Robot response: " + chatgptResponse_1)
    
    set_send_message("[TALK] " + chatgptResponse_1)
    TTS_Robot.text_to_speech_openai(chatgptResponse_1)
    while ServerScript.service_in_progress:
        pass
    
    
def Generate_Head_Orientations(ask_order, _participant_Amount):
    first_headOrientation = ""
    second_headOrientation = ""
    third_headOrientation = ""
    fourth_headOrientation = ""
    
    iterator = 0
    currentlyIteratedOrientation = ""   # Used for storing the head orientation "calculated" in the current for loop iteration, so the next head orientations can still store which orientation to rotate from.
    
    for id in ask_order:
        nextIdLocation = ChangeHeadOrientation.define_orientation_by_id(id=id, participation_amount=_participant_Amount)

        if iterator == 0:
            if nextIdLocation == "neutral":
                first_headOrientation = ChangeHeadOrientation.NeutralPointing(id, _participant_Amount)
            else:
                first_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("lookpoint", currentPosition=ServerScript.current_head_position, newPosition=nextIdLocation)


        if iterator == 1:
            if nextIdLocation == "neutral":
                second_headOrientation = ChangeHeadOrientation.NeutralPointing(id, _participant_Amount)
            else:
                second_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("lookpoint", currentPosition=currentlyIteratedOrientation, newPosition=nextIdLocation)


        if iterator == 2:
            if nextIdLocation == "neutral":
                third_headOrientation = ChangeHeadOrientation.NeutralPointing(id, _participant_Amount)
            else:
                third_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("lookpoint", currentPosition=currentlyIteratedOrientation, newPosition=nextIdLocation)

        if iterator == 3:
            if nextIdLocation == "neutral":
                fourth_headOrientation = ChangeHeadOrientation.NeutralPointing(id, _participant_Amount)
            else:
                fourth_headOrientation = ChangeHeadOrientation.CreateStringCommand_HeadOrientation("lookpoint", currentPosition=currentlyIteratedOrientation, newPosition=nextIdLocation)
        currentlyIteratedOrientation = nextIdLocation
        iterator += 1
    return first_headOrientation, second_headOrientation, third_headOrientation, fourth_headOrientation

def Conclude_Session():
    
    set_send_message("[GESTURE] " + "QT/neutral")
    while ServerScript.service_in_progress:
        pass
    
    conclusionResponse = ChatGPT_Prompting.Simple_PromptChatGPT_ReturnResponse("Summarize and state a course of actions the participants can do when trying to realize their ideas for their project. Maximum a 150 words. Thank the participants for a good conversation and end by greeting them goodbye.", _messageRole="system")
    allMessages_TranscriptionList.append("Robot response: " + conclusionResponse)
    
    set_send_message("[TALK] " + conclusionResponse)
    TTS_Robot.text_to_speech_openai(conclusionResponse)
    while ServerScript.service_in_progress:
        pass
    
    set_send_message("[GESTURE] QT/bye")
    


def HeadNodForDuration():
    set_send_message("[NOD]") # Comment om nodding og hvordan det fungere.
    
    
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