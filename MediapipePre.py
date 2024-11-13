from operator import truediv

import cv2
import mediapipe as mp
import cv2 as cv

mp_drawing = mp.solutions.drawing_utils #The drawing utilities used for drawing the graphics when finding a face etc.
mp_face_mesh=mp.solutions.face_mesh

drawing_spec=mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

video = cv.VideoCapture(0)

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as face_mesh:


    while True:
        ret,image = video.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    #Convert BGR to RGB colourspace
        image.flags.writeable=False
        results = face_mesh.process(image)
        #print(results)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        imgOnRectangle = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(  image=image,
                                            landmark_list=face_landmarks,
                                            connections=mp_face_mesh.FACEMESH_CONTOURS,
                                            landmark_drawing_spec=drawing_spec,
                                            connection_drawing_spec=drawing_spec)
                h, w, c = image.shape
                cx_min=  w
                cy_min = h
                cx_max= cy_max= 0
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
                
                #Making sure that the bounding box coordinates do not exceed the image shape...
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
                
                #Save pixels within the bounding box as an image array
                imgOnRectangle = image[cy_min:cy_max, cx_min:cx_max]        
                print(cy_min)
        
        # for imgCoordinate in imgOnRectangle:
        #     

        if len(imgOnRectangle) > 0:
            cv.imshow("FaceBoundingBox",imgOnRectangle)
            imgOnRectangle = []
        
        cv.imshow("Face mesh", image)
        k=cv.waitKey(1)
        if k==ord('q'):
            break
video.release()
cv2.destroyAllWindows()


