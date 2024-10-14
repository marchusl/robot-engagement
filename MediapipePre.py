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
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(  image=image,
                                            landmark_list=face_landmarks,
                                            connections=mp_face_mesh.FACEMESH_CONTOURS,
                                            landmark_drawing_spec=drawing_spec,
                                            connection_drawing_spec=drawing_spec)
        cv.imshow("Face mesh", image)
        k=cv.waitKey(1)
        if k==ord('q'):
            break
video.release()
cv2.destroyAllWindows()


