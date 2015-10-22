import numpy as np
import cv2
from croppaSfondo import croppaSfondo


#LEGGO CARATTERISTICHE ORB E LE RENDO IN UN VETTORE


class leggiORB:
	def leggi(self,a):
		img = cv2.imread(a,0)           # base
		#cropper = croppaSfondo()
                #img = cropper.croppa(img)
	
		# Initiate SIFT detector
		orb = cv2.ORB(100)

		# find the keypoints and descriptors with SIFT
		kp, des = orb.detectAndCompute(img,None)

		#ogni des e un vettore, ad esempio des[2] e un vettore quindi des e una matrice
		#print des[0]
		#print "--------------------------------------------------------------------------"

		#print des[0,31]#quindi questo e un numero
		#print "------------------------------------------------------"
		
		cont = 0
		righe = len(des)
		colonne = len(des[0])
			
		s = [0]*(righe*colonne)
		for i in range(0,righe):
			for c in range(0,colonne):
				s[cont] = des[i,c]
				cont = cont + 1

		h = [0]*len(s)
		for i in range(0,len(s)):
			h[i]=int(s[i])
			
			
		return h

