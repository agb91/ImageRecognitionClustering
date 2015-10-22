from confrontaShapeBinario import Shape
import numpy as np
import cv2
from confrontaSiftBinario import confrontaSIFT
from confrontaOrbBinario import confrontaORB
from random import randint
from downloadImage import Download
from accessoCartella import accessoCartella
from leggiSiftBinario import leggiSIFT
from leggiOrbBinario import leggiORB
from leggiShapeBinario import leggiShape

#commenti senza apostrofi ne accenti

#idea di fondo legge le immagini dalla cartella path, le classifica con i 3 filtri legati alle features qualora l utente gradisca usarli
#salva le caratteristiche dentro 3 vettori appositi (cosi ad ogni ciclo NON deve ri-estrarle)
#confrontandole individua il gruppo principale segnalato con la classe 3 e definisce le immagini esterne a questo gruppo con le classi
#di somiglianza 1 e 2 (1 diversa, 2 simile)
#il confronto avviene tramire un immagine di riferimento scelta a caso, se il risultato non e concludente (perche il gruppo principale isolato )
#non e abbastanza grande ripete il ciclo a oltranza cambiando immagine (le features sono gia estratte quindi ripetere e computazionalmente
#leggerissimo)

class clusterizzaBinario:
	def clusterizza(self, v, path ):
		siq = v[0]			#uso sift?
		shq = v[1]			#uso shape?
		orq = v[2]			#uso orb?
		soSh = 0.7			#soglia alta shape (oltre la quale e di classe 3)
		sorb = 0.35                     #soglia alta orb
		sosi = 0.35			#soglia alta sift
		bsoSh = 0.35		        #soglia bassa shape (sotto la quale e di classe 1)
		bsorb = 0.20		        #soglia bassa orb
		bsosi=0.20			#soglia bassa sift
		lisi = 300		#parametro di sift
		lior = 60	#paramentro di orb
		itsh = 1		        #paramentro iterazioni di shape
		sesh = 5		        #paramentro sessioni di shape
		minImage = 0.3  	        #quale percentuale normalizzata a 1 e necessaria perche il gruppo principale risulti
						#sufficentemente grande (altrimenti ripeto il ciclo)


		cont3=0
		##leggo da certella shoe e metto in vettore su cui poi si lavora
		car = accessoCartella()		#leggo tutto quelloche c e nella cartella, per farlo uso classe accessoCartella
		vet = []					#vettore tutte le immagini senza path, solo nome
		vet=car.leggi(path)
		k=len(vet)	#quante sono le immagini
                vettore = [0]*k #con path
                for i in range(0,k):
                        vettore[i]=path+'\\'+vet[i]
                vetSiftFeatures = [0]*k
                vetOrbFeatures = [0]*k
                vetShapeFeatures = [0]*k

                #per ogni features leggo le caratteristiche e le metto in un vettore (spesso vettore di matrici)
                #poi il confronto si fara solo tra vettori per non dover rileggere le immagini
                for i in range(0,k):
                        lettoreSi = leggiSIFT()
                        vetSiftFeatures[i] = lettoreSi.leggi(vettore[i])
                        lettoreOr = leggiORB()
                        vetOrbFeatures[i] = lettoreOr.leggi(vettore[i])
                        lettoreShape = leggiShape()
                        # shape ha bisogno di 2 parametri
                        vetShapeFeatures[i] = lettoreShape.leggi(vettore[i],sesh,itsh)

                #print vetSiftFeatures
                #print vetOrbFeatures
                #print vetShapeFeatures
                j=0 # Contatore per fermare la selezione casuale dell'immagine
                while float(cont3)/float(k)<minImage and j<k: #ripeti finche il gruppo principale non e abbastanza grosso rispetto a un parametro settato (minImage)
                        j=j+1
                        images = vettore # immagini scaricate dal db e lette
                        imRif = randint(0,k-1) #immagine casuale di riferimento
                        print images[imRif] #il confronto e in base ad un immagine casuale (ad ogni giro di while e diversa)
                        
                        vettorePeggiori = []
                        vetClSh = []				#vettore classi secondo shape
                        vetClSi = []				#vettore classi secondo sift
                        vetClOr = []				#vettore classi secondo orb
                        #vettore = []				#vettore path completi

                        vettorePeggiori = [0]*k
                        vetClSh = [0]*k				#vettore classi secondo shape
                        vetClSi = [0]*k				#vettore classi secondo sift
                        vetClOr = [0]*k				#vettore classi secondo orb
                        #vettore = [0]*k			#vettore path completi



                        #inizializzo le classi
                        sh = Shape()
                        si = confrontaSIFT()
                        orb = confrontaORB()

                        cont3=0

                        vetSh = [0]*k		#3 vettori dei valori numerici percentuali di somiglianza rispetto alle 3 features
                        vetSi = [0]*k
                        vetOr = [0]*k

                        #imagesSel = []#disuso

                        #FILTRO SHAPE, filtra le immagini con shape, estrae il valore di somiglianza, assegna la classe secondo shape di conseguenza
                        if shq==1:
                                risps=[0]*(len(images))
                                for i in range(0,len(images)):
                                        risps[i]=sh.shapeControl(vetShapeFeatures[imRif],vetShapeFeatures[i],sesh)
                                        vetSh[i] = round(risps[i], 2)
                                        if vetSh[i]<bsoSh:
                                                vetClSh[i]=1
                                        if vetSh[i]>=bsoSh:
                                                if vetSh[i]>soSh:
                                                        vetClSh[i]=3
                                                else:
                                                        vetClSh[i]=2

                        #print vetClSh

                        #FILTRO SIFT
                        if siq==1:
                                risps=[0]*(len(images))
                                for i in range(0,len(images)):
                                        risps[i]=si.siftControl(vetSiftFeatures[imRif],vetSiftFeatures[i],lisi)
                                        vetSi[i] = round(risps[i], 2)
                                        if vetSi[i]<bsosi:
                                                vetClSi[i]=1
                                        if vetSi[i]>=bsosi:
                                                if vetSi[i]>sosi:
                                                        vetClSi[i]=3
                                                else:
                                                        vetClSi[i]=2
                        #print vetClSi


                        #FILTRO ORB
                        if orq==1:
                                risps=[0]*(len(images))
                                for i in range(0,len(images)):
                                        risps[i]=orb.orbControl(vetOrbFeatures[imRif],vetOrbFeatures[i],lior)
                                        vetOr[i] = round(risps[i], 2)
                                        if vetOr[i]<bsorb:
                                                vetClOr[i]=1
                                        if vetOr[i]>=bsorb:
                                                if vetOr[i]>sorb:
                                                        vetClOr[i]=3
                                                else:
                                                        vetClOr[i]=2
                        #print vetClOr

                        vetSum = [0]*k   #vettore somma delle classi assegnate da ogni features

                        for i in range(0,k):
                                vetSum[i] = vetSum[i] + vetClSh[i]
                                vetSum[i] = vetSum[i] + vetClSi[i]
                                vetSum[i] = vetSum[i] + vetClOr[i]
                                vetSum[i] = float(vetSum[i]/float(siq+orq+shq))			#divido per 3 perche sono 3 features

                        vetClass = [0]*k   #vettore della classificazione generale

                        for i in range(0,k):   #assegna la classificazione generale con un po di fantasia
                                if vetSum[i]<2:
                                        vetClass[i]=1
                                else:
                                        if vetSum[i]<2.3:
                                                vetClass[i]=2
                                        else:
                                                vetClass[i]=3

                        for i in range(0,k):
                                if vetClass[i]==3:
                                        cont3=cont3+1
                                        
                if(j>=k):
                        print """\nNon ho trovato nulla che soddisfi i requisiti, saranno restituiti gli ultimi risultati calcolati.\nRivedere i parametri per la parola cercata\n"""


                for i in range(0,k):
                        print vet[i] + " classe:   " + str(vetClass[i])+"\n"

                return [vet,vet,vetClass]
