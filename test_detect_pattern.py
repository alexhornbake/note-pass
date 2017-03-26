import unittest
import detect_pattern
import cv2

class TestDetectPatternMethods(unittest.TestCase):

	def test_decodeBitsFromDetectedImage(self):
		img = cv2.imread('test_pattern_5.jpg')
		detected, wasFound = detect_pattern.getPatternFromImage(img, 11, 11)

		self.assertTrue(wasFound)
		
		decodedImage, decodedBits = detect_pattern.decodeBitsFromDetectedImage(detected, 11, 11)

		self.assertEquals(decodedBits, [False, False, False, True, False, False, True, True, True, False, False, False, True, False, False, False, False, False, False, False, True, True, True, False, True, False, False, True, False, True, False, False, False, False, False, False, False, True, True, False, True, False, True, True, True, False, True, True, False, True, False, True, True, True, False, False, False, False, True, False, True, False, False, False, False, True, True, True, False, True, True, False, True, True, False, False, False, False, True, True, False, False, False, False, True, True, False, False, True, False, False, True, True, True, False, False, True, True, False, False, False, False, False, False, True, False, True, False, False, False, False, False, False, True, False, True, True, False, False, False, False, False, False, False, False, False, False, False, True, False, True, False, False, False, True, False, False, True, True, False, False, True, False, False, False, False, False, False, False, False, False, False, True, False, False, True, False, False, False, True, False, True, False, True, False, False, True, False, True, True, False, True, False, True, False, False, False, False, False, False, True, True, False, False, True, False, False, False, True, False, True, False, False, True, True, False, True, False, False, False, False, False, False, True, False, False, True, False, False, False, False, True, False, True, False, False, True, True, False, False])

if __name__ == '__main__':
    unittest.main()
