import numpy as np
import cv2


#IDEA DI FONDO: CONTO I MATCH CON UNA DISTANZA ENTRO UNA SOGLIA
# USO IMPLEMENTRAZIONE GIA PRONTA DI OPENCV

#confronto i 2 des dei 2 indicatori, normalizzo tra 0 e 1 dove 1 e l uguaglianza (des1 e se stesso)


class confrontaORB:
	def orbControl(self,a,b,sog):

		des1 = a
		des2 = b
		soglia=sog

		# create BFMatcher object
		bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

		# Match descriptors.
		matches = bf.match(des1,des2)
		matchesRif = bf.match(des1,des1)

		# Sort them in the order of their distance.
		matches = sorted(matches, key = lambda x:x.distance)  #se li ordino dopo che 1 e definito scarso posso smettere di cercare e risparmiare un
		matchesRif = sorted(matchesRif, key = lambda x:x.distance)
		#sacco di calcolo

		cont=0
		contRif=0
		
	#uso il numero di corrispondenze non la loro distanza (mi sembra di ottenere risultati migliori), 
	#se ritenete cambiate, (altrimenti al variare della dimensione dell immagine
	#l indicatore dovrebbe essere sfasato [si diverta il gruppo di machine learning a scoprire se questa ipotesi e vera])
	#il numero e normalizzato rispetto al numero calcolato nel caso di somiglianza perfetta (stessa immagine)

		for i in range(0,len(matches)-1):
			if matches[i].distance<soglia:
				cont=cont+1
			else:
				break   #non ce ne sono altri, risparmio calcoli
				
		for i in range(0,len(matchesRif)-1):
			if matchesRif[i].distance<soglia:
				contRif=contRif+1
			else:
				break   #non ce ne sono altri,
				
		#print float(float(cont)/float(contRif))		
		return float(float(cont)/float(contRif))

