import numpy as np
import cv2

#LEGGO FEATURES SIFT E LE METTO IN UN VETTORE CHE RENDO
class leggiSIFT:
	def leggi(self,a):

		img1 = cv2.imread(a,0)          # base

		# Initiate SIFT detector
		sift = cv2.SIFT(400)
		
		kp1 = []
		des1 = []

		# find the keypoints and descriptors with SIFT
		kp1, des1 = sift.detectAndCompute(img1,None)

		return des1

