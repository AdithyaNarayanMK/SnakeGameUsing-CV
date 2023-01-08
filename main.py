import cvzone
import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Making a camera object

cap = cv.VideoCapture(0)
cap.set(3, 1200)
cap.set(4, 720)

detector = HandDetector(detectionCon = .8, maxHands = 1)


while True:
    ret, img = cap.read()
    img = cv.flip(img, 1)
    hands, img = detector.findHands(img, flipType = False)
    if hands:
        lmList = hands[0]["lmList"]  # lmlist -> landmarkList
        pointIndex = lmList[8][: 2]
        cv.circle(img, pointIndex, 20, (200, 0, 200), cv.FILLED)


    cv.imshow("Game",img)
    if cv.waitKey(10) == ord("e") or cv.waitKey(10) == ord("E"):
        cv.destroyWindow("Game")
        break