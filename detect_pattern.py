# Import the modules
import cv2
from sklearn.externals import joblib
import skimage.feature as feature
import numpy as np

#only process contours with bounding rects larger than
firstpass_size_threshold=5
secondpass_size_theshold=5
output_width=200
output_padding=50

# Load the classifier
clf = joblib.load("symbols_v001_cls.pkl")

def getRectsForLabelsInImage(im, label, thresh):
	# Convert to grayscale and apply filtering for better detection
	im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)
	im_canny = cv2.Canny(im_gray, 100, 200)
	im_th = cv2.adaptiveThreshold(im_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

	# Find contours in the image
	ctrs, hier = cv2.findContours(im_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# For each countour region, calculate HOG features and predict
	# the digit using Linear SVM.
	foundLabels = []
	for ctr in ctrs:
		# get the bounding rect of the countour
		rect = cv2.boundingRect(ctr)
		#ignore rectangles below threshold
		if rect[2] < thresh or rect[3] < thresh:
		 	continue

		# Grab the region of interest
		leng = int(rect[3] * 1.6)
		pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
		pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
		roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
		if roi.size == 0 :
			continue
		# Resize the image
		roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
		roi = cv2.dilate(roi, (3, 3))
		# Calculate the HOG features
		roi_hog_fd = feature.hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)

		labels = clf.predict(np.array([roi_hog_fd], 'float64'))

		# 4 is the label for "X" in our model
		# set those aside for later.
		if labels[0] == label :
			foundLabels.append(rect)

	return foundLabels, im_th

def getBoundingCornersOfRects(rects):
	#find the corners
	t = np.transpose(np.array(rects))
	upperLeft = rects[np.argmin(t[0]+t[1])]
	upperRight = rects[np.argmax(t[0]-t[1])]
	lowerRight = rects[np.argmax(t[0]+t[1])]
	lowerLeft = rects[np.argmin(t[0]-t[1])]

	# return the result clockwise from upperLeft
	return np.array([
		[upperLeft[0], upperLeft[1]],
		[upperRight[0] + upperRight[2], upperRight[1]],
		[lowerRight[0] + lowerRight[2], lowerRight[1] + lowerRight[3]],
		[lowerLeft[0], lowerLeft[1] + lowerLeft[3]]],
		np.float32
	)

def getAvgRectSize(rects):
	t = np.transpose(np.array(rects))
	return [np.average(t[2]), np.average(t[3])]

def detectImage(im):
	# find the 4 X's in the corner of the pattern
	foundFours, im_th = getRectsForLabelsInImage(im, 4, firstpass_size_threshold)

	# check if we have the 4 corners
	if len(foundFours) != 4 :
		return im_th, False

	boundingPolygon = getBoundingCornersOfRects(foundFours)

	#figure out the aspect ratio, of the input image
	resize_percent = np.float32(output_width)/np.float32(im.shape[1])
	output_height = np.int32(np.float32(im.shape[0])*resize_percent)

	targetPolygon = np.array([
		[output_padding,output_padding],
		[output_width+output_padding,output_padding],
		[output_width+output_padding,output_height+output_padding],
		[output_padding,output_height+output_padding],
	], np.float32)

	warpMat = cv2.getPerspectiveTransform(boundingPolygon, targetPolygon)
	warped = cv2.warpPerspective(im, warpMat, (output_width+(2*output_padding),output_height+(2*output_padding)))

	#second pass on the warped image
	foundFours, im_th = getRectsForLabelsInImage(warped, 4, secondpass_size_theshold)
	# check if we have the 4 corners
	if len(foundFours) != 4 :
		return warped, True


	avgRectSize = getAvgRectSize(foundFours)

	boundingPolygon = getBoundingCornersOfRects(foundFours)
	targetPolygon = np.array([
		[0,0],
		[output_width,0],
		[output_width,output_height],
		[0,output_height],
	], np.float32)

	warpMat = cv2.getPerspectiveTransform(boundingPolygon, targetPolygon)
	warped = cv2.warpPerspective(im_th, warpMat, (output_width,output_height))

	#cv2.polylines(im, [np.int32(boundingPolygon).reshape((-1,1,2))], True, (0,255,0))
	#cv2.rectangle(im, (upperLeft[0], upperLeft[1]), (lowerRight[0]+lowerRight[2], lowerRight[1]+lowerRight[3]), (0,255,0),3)

	#for rect in foundFours:
		# Draw the rectangles
		#cv2.rectangle(warped, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)

	return warped, True