import numpy as np
import cv2

class confrontaSIFT:
	def siftControl(self,a,b,sog):
					

		# find the keypoints and descriptors with SIFT
		des1 = a
		des2 = b
					
		#IDEA DI FONDO: CONTO I MATCH CON UNA DISTANZA ENTRO UNA SOGLIA
		# MI BASO SUL SIFT GIA FATTO DI OPENCV
		soglia=sog 
		
		# BFMatcher with default params
		bf = cv2.BFMatcher()
		matches = bf.match(des1,des2)
		matchesRif = bf.match(des1,des1)

		cont=0
		contRif=0
		
	#uso il numero di corrispondenze non la loro distanza, se ritenete cambiate, (altrimenti al variare della dimensione dell immagine
	#l indicatore dovrebbe essere sfasato [si diverta il gruppo di machine learning a scoprire se questa ipotesi e vera])
	#il numero e normalizzato rispetto al numero calcolato nel caso di somiglianza perfetta (stessa immagine)

		for m in matches:
			if m.distance < soglia:
				cont = cont+1
				
		for m in matchesRif:
			if m.distance < soglia:
				contRif = contRif+1		
	
		ris = float(cont)/float(contRif)

		return ris

