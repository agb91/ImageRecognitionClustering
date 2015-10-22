import numpy as np
import cv2
from random import randint
from downloadImage import Download
from accessoCartella import accessoCartella
from leggiSIFT import leggiSIFT
from leggiORB import leggiORB
from leggiShape import leggiShape
from sklearn.cluster import KMeans

#commenti senza apostrofi ne accenti

#idea di fondo legge le immagini dalla cartella path, le classifica con i 3 filtri legati alle features qualora l utente gradisca usarli
#salva le caratteristiche dentro 3 vettori appositi (cosi ad ogni ciclo NON deve ri-estrarle). la clusterizzazione viene svolta da kmeans

class clusterizzaKMeans:
	def clusterizza(self, v, path ):
		siq = v[0]			#uso sift?
		shq = v[1]			#uso shape?
		orq = v[2]			#uso orb?
		classi = v[3]
		
		car = accessoCartella()		#leggo tutto quelloche c e nella cartella, per farlo uso classe accessoCartella
		vet = []					#vettore tutte le immagini senza path, solo nome
		vet=car.leggi(path)
		k=len(vet)	#quante sono le immagini
		vettore = [0]*k#con path
		for i in range(0,k):
			vettore[i]=path+'/'+vet[i]
		vetSiftFeatures = []
		vetOrbFeatures = []
		vetShapeFeatures = []
		vettoreGenerale = []

		# dove i e l indice dell immagine
		for i in range(0,k):#per ogni immagine
			features1immagine = []#vettore con features di 1 singola immagine, contiene matrici filate in vettori
			
			if (siq==1):#se usi sift
				lettoreSi = leggiSIFT()
				vetSiftFeatures.append(lettoreSi.leggi(vettore[i]))
				features1immagine = features1immagine + vetSiftFeatures[i]
			
			if (orq==1):#se usi orb
				lettoreOr = leggiORB()
				vetOrbFeatures.append(lettoreOr.leggi(vettore[i]))
				features1immagine = features1immagine + vetOrbFeatures[i]
									
			if (shq==1):#se usi shape
				lettoreShape = leggiShape()		# shape ha bisogno di 1 solo parametro
				vetShapeFeatures.append(lettoreShape.leggi(vettore[i],0))
				features1immagine = features1immagine + vetShapeFeatures[i]
				
			vettoreGenerale.append(features1immagine)#matrice generale con tutte le features  di tutte le immagini, ogni riga e un immagine

		#non e detto che tutte le righe abbiano la stessa lunghezza, alcune immagini potrebbero avere meno punti chiave, quindi si normalizza
		#la lunghezza dei vari vettori per renderla uguale
		vettoreGenerale = np.array(vettoreGenerale)
		lengths = [len(line) for line in vettoreGenerale]
		#print lengths
		minimo = min(lengths)

		indice = len(vettoreGenerale)
		
		nuovo = []
		for riga in range(0,indice):
			#print "indice:" + str(riga)
			nuovo.append(vettoreGenerale[riga][0:minimo])
			
		lengths = [len(line) for line in nuovo]	
		#print lengths
		
		
		
		#KMeans gestisce la clusterizzazione
		km = KMeans(n_clusters=classi, init='k-means++', n_init=10, max_iter=600, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)
		vetClass = km.fit_predict(nuovo)
		vetCentri = km.cluster_centers_
		
		#print len(vetCentri)
		vettoreDistanze = []#vettore con 1 distanza(rispetto al relativo centroide) per ogni immagine
		for i in range(0,k):#per ogni immagine
			vettoreImm = nuovo[i]#vettode features di ogni immagine
			vettoreCentroide = []#vettore del centroide di quella classe
			#print len(vettoreImm)
			for cl in range(0,classi):#trovo vettore centroide di quella classe
				if vetClass[i]==cl:
					vettoreCentroide = vetCentri[cl]
					#print "classe:" + str(cl)
			#print vettoreCentroide
			#print "----------------------------------------------"
			diff = []#differenza tra vettore dell immagine e della classe:
			for indice in range(0,minimo):#la calcolo
				diff.append(abs(vettoreImm[indice]-vettoreCentroide[indice]))
			diffTot = 0#differenza totale
			for indice in range(0,minimo):
				diffTot = diffTot + diff[indice]
			vettoreDistanze.append(diffTot)	
		
		for i in range(0,len(vettoreDistanze)): #normalizzo a 100 e lo rendo una percentuale di somiglianza
			vettoreDistanze[i]=1-float(float(vettoreDistanze[i])/float(max(vettoreDistanze)))
			
		print vettoreDistanze
							
		

		for classe in range (0,classi):
			print "CLASSE " + str(classe) + ":"
			for i in range(0,k):
				if(vetClass[i]==classe):
					print "    " + str(vet[i])
					

		return [vet,vettoreDistanze,vetClass]

		
