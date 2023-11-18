import streamlit as st
import cvzone
import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
import random
from PIL import Image

# def app_page()
st.title("SnakeGameUsing CV")
# st.image("snake.jpg",width=200,height = 200)
img = Image.open("snake.jpg")
img = img.resize((500, 400))
st.image(img)


if st.button("Play Game",type="primary"):
    cap = cv.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = HandDetector(detectionCon = .8, maxHands = 1)
    @st.cache_resource
    class SnakeGameClass:
        def __init__(self, path : str) -> None:
            self.points = [] # All points in the snake
            self.lengths = [] # The length of all points in the snake
            self.currentLength = 0 # Total length of the snake
            self.allowedLength = 130
            self.previousHead = 0, 0
            self.score = 0
            self.imgFood = cv.imread(path, cv.IMREAD_UNCHANGED)
            self.hFood, self.wFood, _ = self.imgFood.shape
            self.GameOver = False
            self.foodPoint = 0, 0
            self.randomFoodLocation()
        def randomFoodLocation(self) -> int:
            self.foodPoint = random.randint(100, 1100), random.randint(100,620)

        def gameOver(self) -> None:
            self.points = [] # All points in the snake
            self.lengths = [] # The length of all points in the snake
            self.currentLength = 0 # Total length of the snake
            self.allowedLength = 130
            self.previousHead = 0, 0
            self.hFood, self.wFood, _ = self.imgFood.shape
            self.foodPoint = 0, 0
            self.randomFoodLocation()

        def update(self, imgMain, currentHead) -> None:
            px, py = self.previousHead
            cx, cy = currentHead
            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = currentHead

                # Length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.points.pop(i)
                    self.lengths.pop(i)
                    if self.currentLength < self.allowedLength:
                        break
                    
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx <rx + self.wFood and \
                ry - self.hFood // 2 < cy < ry + self.hFood:
                    
                self.randomFoodLocation()
                self.allowedLength += 40
                self.score += 1

                # Drawing Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                cv.circle(imgMain, self.points[-1], 20, (200, 0, 200), cv.FILLED)

                # Check for collision
            pts = np.array(self.points[ : -2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv.polylines(imgMain, [pts], False, (0, 200, 0), 3)
            minDist = cv.pointPolygonTest(pts, (cx, cy), True)
            cvzone.putTextRect(imgMain, f"Score {self.score}", [50, 80],
                                    scale= 7, thickness= 5, offset= 20)
            if minDist >= -1 and minDist <= 1:
                self.GameOver = True

                # Draw the food
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - (self.wFood // 2), ry - (self.hFood // 2)))
            return imgMain        
           
    game = SnakeGameClass("berry.png")

    while True:
        ret, img = cap.read()
        img = cv.flip(img, 1)
        hands, img = detector.findHands(img, flipType = False)
        if game.GameOver:
            game.gameOver()
            cvzone.putTextRect(img, "Game Over!!!", [300, 400],
                                scale= 7, thickness= 5, offset= 20)
            cvzone.putTextRect(img, F"Your Score {game.score}", [300, 400],
                                scale= 7, thickness= 5, offset= 20)
        else:
            if hands:
                lmList = hands[0]["lmList"]  # lmlist -> landmarkList
                pointIndex = lmList[8][: 2]
                img = game.update(img, pointIndex)

        cv.imshow("Game",img)
        if cv.waitKey(1) == ord("e") or cv.waitKey(1) == ord("E"):
            cv.destroyWindow("Game")
            break
        elif cv.waitKey(1) == ord("r"):
            game.GameOver = False
            game.score = 0

    

