import main

# Used for orienting the head
#globalCurrentHeadPosition = "neutral"

def PixelCoordinate_HeadOrientation(pixelCoordinate, cameraResolution_width, cameraResolution_height):
    
    #print(int(pixelCoordinate[0]))     #Pixel X coordinate
    #print(int(pixelCoordinate[1]))     #Pixel Y coordinate
    
    #Check if pixel's x coordinate is to the right or the left of the camera image width's middle + offset (y)
    if int(pixelCoordinate[0]) < int(cameraResolution_width / 2) - 200:   #The 200 is a 200 pixel offset from the image width's middle 
        print("FAR_LEFT")
    if int(pixelCoordinate[0]) > int(cameraResolution_width / 2) + 200:
        print("FAR_RIGHT")
    
    #Check if pixel's y coordinate is above or below the middle of the camera image height's middle + offset (y)
    if int(pixelCoordinate[1]) < int(cameraResolution_height / 2) - 150:    #The 150 is a 150 pixel offset from the image width's middle 
        print("FAR_UP")
    if int(pixelCoordinate[1]) > int(cameraResolution_height / 2) + 150:
        print("FAR_DOWN")
    

def CreateStringCommand_HeadOrientation(action, currentPosition, newPosition):
    
    # if currentPosition != newPosition:
    actionString = "[GESTURE] " + action + "-" + currentPosition + "-" + newPosition
    return actionString
    
    # elif currentPosition == newPosition:
    #     print("Current position equals new position...")
    
def CreateStringCommand_Nod(currentPosition):
    actionstring = "[GESTURE] nod-" + currentPosition
    return actionstring


def define_orientation_by_id(id, participation_amount):     # Method used for translating the participation id to rotations, given that IDs are given to participants starting from the LEFT going right, icrementing participation ID the further right you are relative to other participants.
    #participantAmmount = len(ask_order_list)
    headOrientation = ""
    if participation_amount == 2:
        match id:
            case "1":
                headOrientation = "left"
            case "2":
                headOrientation = "right"
                
    
    if participation_amount == 3:
        match id:
            case "1":
                headOrientation = "left"
            case "2":
                headOrientation = "neutral"
            case "3":
                headOrientation = "right"

    if participation_amount == 4:
        match id:
            case "1":
                headOrientation = "left"
            case "2":
                headOrientation = "neutral"
            case "3":
                headOrientation = "neutral"
            case "4":
                headOrientation = "right"
            
    return headOrientation

def NeutralPointing(id, participant_amount):
    neutralAction = ""
    if participant_amount == 3:
        match id:
            case "2":
                neutralAction = "[GESTURE] lookpoint-leftarm"

    if participant_amount == 4:
        match id:
            case "2":
                neutralAction = "[GESTURE] lookpoint-leftarm"
            case "3":
                neutralAction = "[GESTURE] lookpoint-rightarm"
            
    
    return neutralAction