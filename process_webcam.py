import cv2
import detect_pattern

cap = cv2.VideoCapture(0)

while True:
    cameraImg = cap.read()[1]
    detected, wasFound = detect_pattern.detectImage(cameraImg)
    cv2.imshow('image', cameraImg)
    if wasFound:
        cv2.imshow('detected', detected)
    key = cv2.waitKey(1)
    if key == 27:
        break
