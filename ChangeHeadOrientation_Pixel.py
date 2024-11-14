

def ChangeHeadOrientation_PixelCoordinate(pixelCoordinate, cameraResolution_width, cameraResolution_height):
    
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
    