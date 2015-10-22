import numpy as np
import cv2
from random import randint
from downloadImage import Download
from accessoCartella import accessoCartella
from leggiSIFT import leggiSIFT
from leggiORB import leggiORB
from leggiShape import leggiShape
from sklearn.cluster import DBSCAN
from sklearn import metrics

#commenti senza apostrofi ne accenti

#idea di fondo legge le immagini dalla cartella path, le classifica con i 3 filtri legati alle features qualora l utente gradisca usarli
#salva le caratteristiche dentro 3 vettori appositi (cosi ad ogni ciclo NON deve ri-estrarle). la clusterizzazione viene svolta da kmeans

class clusterizzaDBScan:
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




		#lengths = [len(line) for line in nuovo]
		#print lengths


		#print nuovo
		#print "----------------------------------------------------------------------"
		#KMeans gestisce la clusterizzazione
		n_clusters_ = 0
		vetClass = [0]
		neps = 3000
		while n_clusters_ < 1 or n_clusters_ >= (len(vet)/2):
                        neps = neps + 100
                        db = DBSCAN(eps=neps, min_samples=1).fit(nuovo)
                        vetClass = db.labels_

                        n_clusters_ = len(set(vetClass)) - (1 if -1 in vetClass else 0)

		print "numero di cluster ottenuti:  " + str(n_clusters_)

		
		vettoreDistanze = [-1.0]*len(vet)

		for i in range (0,len(vet)):
			print str(vet[i])
			print "classe:" + str(vetClass[i]) + "   somiglianza:" + str(vettoreDistanze[i])
			print ""

		return [vet,vettoreDistanze,vetClass]
