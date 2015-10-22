import numpy as np
import cv2
from math import ceil
import math

#NIENTE ACCENTI NE APOSTROFI

## rapporto altezza/larghezza oggetto

# Prima crea l immagine sure_bg usando l algoritmo opencv per selezionare lo sfondo: in questa implementazione ci occupiamo solo di cio che
# l algoritmo definisce sicuramente sfondo. Poi scorrendo con un for dall angolo alto sinistro e dall angolo basso destro cerchiamo i primi
# punti  di cambiamento dell immagine ottenendo le prime e ultime colonne e righe dell immagine

#FUNZIONA SOLO CON IMMAGINI FORTEMENTE SEPARATE DALLO SFONDO! CON LENA NO PERCHE LA FOTO E PIENA DI OMBRE!!

#IDEA 2 PER VERSIONE SHAPE:
# 4 vettori: distanze (normalizzate rispetto alle dimensioni dell'immagine) da ogni lato sottratta la minore (migliora le prestazioni in caso
#di immagini spostate) il programma restituisce una somiglianza tra 0 e 1 dove 1 e uguaglianza, e 0 la distanza dell immagine piu distante 
# possibile STIMATA (QUINDI A LIVELLO TEORICO POTREBBE ANDARE SOTTO 0, NON CREDO CHE SUCCEDA MA POTREBBE SUCCEDERE)

class Shape:
	def shapeControl(self,a,b,sez):
		k = len(a)
		totdif=0

		for i in range (0,k):
			totdif=totdif+abs(a[i]-b[i])
		   
		totdif=float(sez)-float(totdif)
		totdif = totdif/float(sez)
		
		#print totdif
		
		return totdif
