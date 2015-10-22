import numpy as np
import cv2
from croppaSfondo import croppaSfondo

#LEGGO FEATURES SIFT E LE METTO IN UN VETTORE CHE RENDO
class leggiSIFT:
	def leggi(self,a):

		img1 = cv2.imread(a,0)          # base
                #cropper = croppaSfondo()
                #img1 = cropper.croppa(img1)
		# Initiate SIFT detector
		sift = cv2.SIFT(100)
		
		kp1 = []
		des1 = []

		# find the keypoints and descriptors with SIFT
		kp1, des1 = sift.detectAndCompute(img1,None)

		#ogni des e un vettore, ad esempio des1[2] e un vettore quindi des1 e una matrice
		#print des1[0]
		#print "--------------------------------------------------------------------------"

		#print des1[0,3]#quindi questo e un numero

		cont = 0
		righe = len(des1)
		colonne = len(des1[0])
		
		s = [0]*(righe*colonne)
		for i in range(0,righe):
			for c in range(0,colonne):
				s[cont] = des1[i,c]
				cont = cont + 1

		h = [0]*len(s)
		for i in range(0,len(s)):
			h[i]=int(s[i])
			
		return h

