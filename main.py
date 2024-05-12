import cv2
import mediapipe
import pyautogui
import numpy as np
from sklearn.model_selection import train_test_split


import time

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
face_mesh = mediapipe.solutions.face_mesh.FaceMesh(refine_landmarks = True)
# camera.set(cv2.CAP_PROP_EXPOSURE, 100) 
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


leftEye = [468, 469, 470, 471, 472, 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
leftInnerRing = [130, 25, 110, 24, 23, 22, 26, 112, 243, 190, 56, 28, 27, 29, 30, 247]
leftOuterRing = [226, 31, 228, 229, 230, 231, 232, 233, 244, 189, 221, 222, 223, 224, 225, 113]
rightEye = [473, 474, 475, 476, 477, 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
yPerpendicular = [4, 5, 195, 197, 6, 168, 8, 9, 151, 10]
# print(len(leftEye), len(rightEye), len(yPerpendicular))

features_to_be_checked = leftEye + leftInnerRing + leftOuterRing + rightEye + yPerpendicular

def getLandmarks(frame):
    RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    outputMesh = face_mesh.process(RGBframe)
    landmark_points = outputMesh.multi_face_landmarks

    if(landmark_points):
        landmarks = landmark_points[0].landmark
        index = 0
        
        singleCap = []
        for landmark in landmarks:
            # if(index in features_to_be_checked): #(or True to get full mesh)
                x = landmark.x
                y = landmark.y
                z = landmark.z
                singleCap.append(x)
                singleCap.append(y)
                singleCap.append(z)
            # index+=1
        return(singleCap)


def collection(seconds, visible = False):
    x_data = []
    y_data = []
    startTime = time.time()
    while time.time() < startTime + seconds:
        x, y = pyautogui.position()
        success, frame = camera.read()
        frame_height, frame_width, frame_depth = frame.shape
    
        landmarks = getLandmarks(frame)

        if(visible and landmarks):
            for i in range (0, len(landmarks), 3):
                x, y, z = landmarks[i:i+3]
                cv2.circle(frame, (int(x * frame_width), int(y * frame_height)), 1, (255, 255, 255))
            cv2.imshow("frame", frame)
            cv2.waitKey(1)

        x_data.append(landmarks)
        y_data.append([x, y])

    # x_data = np.array([sublist + [0] * (476 - len(sublist)) for sublist in x_data])
    # y_data = np.array([sublist + [0] * (2 - len(sublist)) for sublist in y_data])
    return(x_data, y_data)





def main():

    x_training, y_training = collection(200, True)
    # np.savez("trainingData.npz", arr1=x_training, arr2=y_training)

    # loadedData = np.load("trainingData.npz")
    # trainingX = loadedData["arr1"]
    # trainingY = loadedData['arr2']

    # x_testing, y_testing = collection(5)


# def main():
#     choice = input("What are we planing to generate? (training/testing): ")
#     if choice == "training":
        

if __name__ == "__main__":
    main()