from sklearn.externals import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np
import cv2
from glob import glob

outputFile = "./classifiers/symbols_v001_cls.pkl"

features = []
labels = []

print("transforming images to hog features...")
for i in range(1, 7):
	print("processing ./ml_images/{0}/*.png".format(i))
	for file in glob('./ml_images/{0}/*.png'.format(i)):
		im=cv2.imread(file)
		grey_im = cv2.cvtColor( im, cv2.COLOR_BGR2GRAY );
		cv2.imshow('image',grey_im)
		cv2.waitKey()
		fd = hog(grey_im.reshape((30, 30)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
	 	features.append(fd)
	 	labels.append(i)

hog_features = np.array(features, 'float64')
hog_labels = np.array(labels, 'int')
clf = LinearSVC()

print("classifying the features...")
clf.fit(hog_features, hog_labels)
joblib.dump(clf, outputFile, compress=0)
print("done!")