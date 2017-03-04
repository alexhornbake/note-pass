import sys
import cv2
import numpy as np

# This script takes an image, and lets user classify image (y/n) on keyboard as an roi to save for
# running against classifier

image_name = sys.argv[1]
output_prefix = sys.argv[2]

img = cv2.imread(image_name)

# make grayscale and apply blur
im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)
ret, im_th = cv2.threshold(im_gray, 150, 255, cv2.THRESH_BINARY_INV)

ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Get rectangles contains each contour
rects = [cv2.boundingRect(ctr) for ctr in ctrs]

# For each rectangular region, calculate HOG features and predict
# the digit using Linear SVM.
for i, rect in enumerate(rects):
	# Draw the rectangles
	cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
	# Make the rectangular region around the digit
	leng = int(rect[3] * 1.6)
	pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
	pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
	roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
	
	# Resize the image
	roi = cv2.resize(roi, (30, 30), interpolation=cv2.INTER_AREA)
	#roi = cv2.dilate(roi, (3, 3))
	
	cv2.imshow('image', roi)
	key = cv2.waitKey(0)
	print(key)
	if key == 121:
		cv2.imwrite('{0}{1}.png'.format(output_prefix, i), roi)
		

cv2.imshow('image', img)
key = cv2.waitKey(0)

