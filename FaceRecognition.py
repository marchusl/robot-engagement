import cv2 as cv
import os, sys
import numpy as np
import math
import face_recognition


# Method for calculating the confidence value for a given face
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

# Class that keeps track of all the known faces and relevant attributes
class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

def encode_faces(self):
    print('starts encoding...')
    for image in os.listdir('Faces'):
        face_image = face_recognition.load_image_file(f'Faces/{image}')

        if (face_recognition.face_encodings(face_image) != []):
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        else:
            print(f'{image}: No face found in picture')

def run_recognition(self):
    video_capture = cv.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        if self.process_current_frame:
            small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv.cvtColor(small_frame, cv.COLOR_BGR2RGB)

            # Finding all faces in current frame
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = 'Unknown'
                confidence = 'Unknown'

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name} ({confidence})')

        # Calling only every second frame to limit resources
        self.process_current_frame = not self.process_current_frame

        # Displaying Annotations
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
            cv.putText(frame, name, (left + 6, bottom - 6), cv.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        cv.imshow('Face Recognition', frame)

        if cv.waitKey(1) == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition
    encode_faces(fr)
    print(f'Known Faces: {fr.known_face_names}')
    run_recognition(fr)