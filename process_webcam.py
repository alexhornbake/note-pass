import cv2
import numpy as np
import detect_pattern
import collections

cap = cv2.VideoCapture(0)

while True:
    cameraImg = cap.read()[1]
    detected, numCols, numRows, wasFound = detect_pattern.detectImage(cameraImg)
    cv2.imshow('image', cameraImg)
    key = cv2.waitKey(1)
    if key == 27:
        break

    if not wasFound:
        continue

    im_gray = cv2.cvtColor(detected,cv2.COLOR_BGR2GRAY)
    im_gray = cv2.GaussianBlur(im_gray, (9, 9), 0)
    im_th = cv2.adaptiveThreshold(im_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,7)

    # #mask edges
    width = detected.shape[1]
    height = detected.shape[0]
    mask_width=7
    cv2.rectangle(im_th, (0, 0), (width, mask_width), (255, 255, 255), -1)
    cv2.rectangle(im_th, (0, 0), (mask_width, height), (255, 255, 255), -1)
    cv2.rectangle(im_th, (width-mask_width, 0), (width, height), (255, 255, 255), -1)
    cv2.rectangle(im_th, (0, height-mask_width), (width, height), (255, 255, 255), -1)
    
    #mask markers
    rect_width = np.float32(width)/np.float32(numCols)
    rect_height = np.float32(height)/np.float32(numRows)
    w=np.int(rect_width+mask_width)
    h=np.int(rect_height+mask_width)
    cv2.rectangle(im_th, (0, 0), (w,h), (255, 255, 255), -1)
    cv2.rectangle(im_th, (width-w, 0), (width,h), (255, 255, 255), -1)
    cv2.rectangle(im_th, (width-w, height-h), (width,height), (255, 255, 255), -1)
    cv2.rectangle(im_th, (0, height-h), (w,height), (255, 255, 255), -1)


    im_th = cv2.cvtColor(im_th,cv2.COLOR_GRAY2RGB)
    
    #average color in bin for detection
    thresh = 210

    # draw col bins
    bwp = .5 # bin width as percent
    bhp = .5 # bin height as percent
    bw = np.float32(rect_width)*np.float32(bwp) # bin width
    bh = np.float32(rect_height)*np.float32(bhp) # bin height
    ox = np.float32(rect_width) * np.float32(1.0-0.5*bwp)
    oy = np.float32(0.5*bhp)*np.float32(rect_height)

    for i in range(0,numRows):
        for j in range(0, numCols-1):
            pt1 = (np.int((j*rect_width)+ox) , np.int(oy))
            pt2 = (np.int((j*rect_width)+ox+bw), np.int(oy + bh))
            roi = im_th[pt1[1]:pt2[1],pt1[0]:pt2[0]]
            avg = np.average(roi)
            if avg < thresh :
                cv2.rectangle(im_th, pt1, pt2, (0, 255, 0), -1)

        oy = oy + np.float32(rect_height)

    # # draw row bins
    bwp = .5 # bin width as percent
    bhp = .5 # bin height as percent
    bw = np.float32(rect_width)*np.float32(bwp) # bin width
    bh = np.float32(rect_height)*np.float32(bhp) # bin height
    ox = np.float32(0.5*bwp)*np.float32(rect_width)
    oy = np.float32(1.0-0.5*bhp)*np.float32(rect_height)

    for i in range(0,numRows-1):
        for j in range(0, numCols):
            pt1 = (np.int((j*rect_width)+ox), np.int(oy))
            pt2 = (np.int((j*rect_width)+ox+bw), np.int(oy + bh))
            roi = im_th[pt1[1]:pt2[1],pt1[0]:pt2[0]]
            avg = np.average(roi)
            if avg < thresh :
                cv2.rectangle(im_th, pt1, pt2, (0, 255, 0), -11)

        oy = oy + np.float32(rect_height)

    cv2.imshow('detected', im_th)
    
