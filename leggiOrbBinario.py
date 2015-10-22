import numpy as np
import cv2


#LEGGO CARATTERISTICHE ORB E LE RENDO IN UN VETTORE


class leggiORB:
	def leggi(self,a):
		img = cv2.imread(a,0)           # base
	
		# Initiate SIFT detector
		orb = cv2.ORB()

		# find the keypoints and descriptors with SIFT
		kp, des = orb.detectAndCompute(img,None)
			
		return des

