import sys
import cv2
import numpy as np
import detect_pattern
import collections
import hashlib
import base64

cap = cv2.VideoCapture(0)
password = sys.argv[1]
prevDecoded = []
sequentialHitsRequired = 5

def appendAndCheckPrev(prevDecoded, curr):
    prevDecoded.append(curr)
    if len(prevDecoded) > sequentialHitsRequired :
        prevDecoded = prevDecoded[-sequentialHitsRequired:]

    if len(prevDecoded) < sequentialHitsRequired :
        return prevDecoded, False

    for s in prevDecoded:
        if curr != s:
            return prevDecoded, False

    return prevDecoded, True

while True:
    cameraImg = cap.read()[1]
    detected, numCols, numRows, wasFound = detect_pattern.getPatternFromImage(cameraImg)

    cv2.imshow('image', cameraImg)
    key = cv2.waitKey(1)
    if key == 27:
        break

    if not wasFound:
        continue

    decodedImage, decodedBits = detect_pattern.decodeBitsFromDetectedImage(detected)

    decodedBytes = np.packbits(np.uint8(decodedBits))
    decodedString = ""
    for indx, i in enumerate(decodedBytes):
        decodedString += chr(i)

    prevDecoded, isStable = appendAndCheckPrev(prevDecoded, decodedString)
    if isStable:
        print(base64.b64encode(hashlib.sha256(decodedString+password).hexdigest()))
        break

    cv2.imshow('detected', decodedImage)
    
