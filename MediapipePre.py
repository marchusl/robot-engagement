from operator import truediv


import cv2
import mediapipe as mp
import cv2
import ChangeHeadOrientation_Pixel

mp_drawing = mp.solutions.drawing_utils #The drawing utilities used for drawing the graphics when finding a face etc.
mp_face_mesh=mp.solutions.face_mesh

drawing_spec=mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

video = cv2.VideoCapture(0)

def FindFaceAndCreateImage():
    ret,image = video.read()
    image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    #Convert BGR to RGB colourspace so we can use mediapipe
    image.flags.writeable=False
    results = face_mesh.process(image)      #Save Mediapipe face mesh data into results variable
    #print(results)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)      #Convert back to BGR colourspace so we can use openCV (imshow, rectangle drawing etc.)
    faceBoundingBox_Image = []
    imageHeight = int
    imageWidth = int
    centerCoordinate_BoundingBox = []
    centerOfBoundingBoxes = []
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(  image=image,
                                        landmark_list=face_landmarks,
                                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                                        landmark_drawing_spec=drawing_spec,
                                        connection_drawing_spec=drawing_spec)
            h, w, c = image.shape
            imageHeight = h
            imageWidth = w
            cx_min=  w
            cy_min = h
            cx_max= cy_max= 0

            face_id = results.multi_face_landmarks.index(face_landmarks)

            for id, lm in enumerate(face_landmarks.landmark):       #Loop over face landmarks and make a bounding box around the face landmarks.
                cx, cy = int(lm.x * w), int(lm.y * h)
                if cx<cx_min:
                    cx_min=cx
                if cy<cy_min:
                    cy_min=cy
                if cx>cx_max:
                    cx_max=cx
                if cy>cy_max:
                    cy_max=cy

            #Making sure that the min_xy and max_xy bounding box coordinates do not exceed the image shape...
            if cx_min < 0:
                cx_min=0
            if cx_max > w:
                cx_max = w
            if cy_min < 0:
                cy_min = 0
            if cy_max > h:
                cy_max = h

            #Draw the bounding box in cyan blue
            cv2.rectangle(image, (cx_min, cy_min), (cx_max, cy_max), (255, 255, 0), 2)
            cv2.putText(image, "Original ID: " + str(face_id), (cx_min, cy_min), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            #Save pixels within the bounding box as an image array
            faceBoundingBox_Image = image[cy_min:cy_max, cx_min:cx_max]
            
            centerCoordinate_BoundingBox = GetCenterOfFaceBoundingBox(cx_min, cx_max, cy_min, cy_max)
            centerOfBoundingBoxes.append(centerCoordinate_BoundingBox)

            #print(centerCoordinate_BoundingBox) 
            
            cv2.circle(image, center=centerCoordinate_BoundingBox, radius=3, color=(0,255,0), thickness=4)


            # for imgCoordinate in imgOnRectangle:

    # Checking all the found bounding boxes and sorts based on the coordinates
    Sorted_IDs = DistributeIDBasedOnPlacement(results.multi_face_landmarks, centerOfBoundingBoxes)

    # Displays the ID on the center pixel
    DisplayIDs(image, Sorted_IDs)

    if len(faceBoundingBox_Image) > 0:
        cv2.imshow("FaceBoundingBox", faceBoundingBox_Image)
        faceBoundingBox_Image = []

    cv2.imshow("Face mesh", image)
    
    return centerCoordinate_BoundingBox, imageWidth, imageHeight, faceBoundingBox_Image
    
    #-------------------END OF FUNCTION-----------------------#
    

def GetCenterOfFaceBoundingBox(x_min, x_max, y_min, y_max):

    centerCoordinate_x = int((x_min + x_max) / 2)
    centerCoordinate_y = int((y_min + y_max) / 2)
    
    centerCoordinates_xy = [centerCoordinate_x, centerCoordinate_y]
    #print(centerCoordinate_x, centerCoordinate_y)
    return centerCoordinates_xy

def DistributeIDBasedOnPlacement(face_meshes, centerCoordinateBoundingBoxes):

    # Ensuring it does not crash if no face is detected
    if face_meshes != None:

        # Creating a dictionary to keep track of faces coordinates and ID
        FaceSortedIDs = {}
        for face in face_meshes:
            FaceSortedIDs[face_meshes.index(face)] = centerCoordinateBoundingBoxes[face_meshes.index(face)]

        # Sorting the faces based on their coordinates
        sorted_faces = sorted(FaceSortedIDs.items(), key=lambda x: x[1])
        sorted_dict = dict(sorted_faces)

        return sorted_dict

def DisplayIDs(image, sorted_ids):
    if sorted_ids != None:
        for id in sorted_ids:
            cv2.putText(image, "Sorted ID: " + str(list(sorted_ids.keys()).index(id)), (sorted_ids[id][0] - 70, sorted_ids[id][1] + 110), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5,
                           min_tracking_confidence=0.5) as face_mesh:
    while True:
        #FindFaceAndCreateImage() values are stored in current while loop iteration...
        pixelCoordinate, cameraResolution_width, cameraResolution_height, faceBoundingBox_Image = FindFaceAndCreateImage()
        
        if len(pixelCoordinate) > 0:
            ChangeHeadOrientation_Pixel.ChangeHeadOrientation_PixelCoordinate(pixelCoordinate, cameraResolution_width, cameraResolution_height)
            
        k=cv2.waitKey(1)
        if k==ord('q'):
            break
video.release()
cv2.destroyAllWindows()


