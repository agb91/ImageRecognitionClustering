import numpy as np
import cv2
from math import ceil
import math

#NIENTE ACCENTI NE APOSTROFI


# Prima crea l immagine sure_bg usando l algoritmo opencv per selezionare lo sfondo: in questa implementazione ci occupiamo solo di cio che
# l algoritmo definisce sicuramente sfondo. Poi scorrendo con un for dall angolo alto sinistro e dall angolo basso destro cerchiamo i primi
# punti  di cambiamento dell immagine ottenendo le prime e ultime colonne e righe dell immagine

#FUNZIONA SOLO CON IMMAGINI FORTEMENTE SEPARATE DALLO SFONDO! CON LENA NO PERCHE LA FOTO E PIENA DI OMBRE!!

#IDEA 2 PER VERSIONE SHAPE:
# 4 vettori: distanze (normalizzate rispetto alle dimensioni dell'immagine) da ogni lato sottratta la minore (migliora le prestazioni in caso
#di immagini spostate) il programma restituisce una somiglianza tra 0 e 1 dove 1 e uguaglianza, e 0 la distanza dell immagine piu distante 
# possibile STIMATA (QUINDI A LIVELLO TEORICO POTREBBE ANDARE SOTTO 0, NON CREDO CHE SUCCEDA MA POTREBBE SUCCEDERE)

class leggiShape:
	def leggi(self,a,sez,it):
		sezioni=sez
		iterazioni = it

		img = cv2.imread(a) 

		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

		ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

		kernel = np.ones((3,3),np.uint8)
		opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = iterazioni)

		# sure background area
		sure_bg = cv2.dilate(opening,kernel,iterations=3)

		#DA QUI COMINCIO CON LA PRIMA IMMAGINE

		#PRIMA TROVO ALTEZZA E LARGHEZZA
		h, w, depth = img.shape #depth non serve..
		#creo il  range (credo che il for in python si faccia cosi)
		hh=range(0,h-1)
		ww=range(0,w-1)


		disth= ceil(h/sezioni)
		distw= ceil(w/sezioni)


		#PRIMA LE ALTEZZE
		sezioniColonne=range(0,sezioni-1)

		primerighe=[0] * (sezioni-1)
		ultimerighe=[h-1] * (sezioni-1)
		altezze = [0]*(sezioni-1)

		#scorro in larghezza quindi trovo le altezze!
		for i in sezioniColonne:
			fatto=0
			fatto2=0
			pos = (i+1)*distw #colonna in cui testo
			#print pos
			for r in hh:
				#print r
				val = sure_bg[r,pos]
				val2 = sure_bg[h-r-1,pos]
				if(val>155 and fatto == 0):
					#print r
					fatto=1
					primerighe[i]=r
				if(val2>155 and fatto2 == 0):
					#print (h-r-1)
					fatto2=1
					ultimerighe[i]=h-r-1  
			altezze[i]=ultimerighe[i]-primerighe[i]

		#print altezze

		#ORA LE LARGHEZZE
		sezioniRighe=range(0,sezioni-1)

		primecols=[0] * (sezioni-1)
		ultimecols=[w-1] * (sezioni-1)
		larghezze = [0]*(sezioni-1)

		#scorro in altezza quindi trovo le larghezze!
		for i in sezioniRighe:
			fatto=0
			fatto2=0
			pos = (i+1)*disth #riga in cui testo
			#print pos
			for c in ww:
				#print c
				val = sure_bg[pos,c]
				val2 = sure_bg[pos,w-c-1]
				if(val>155 and fatto == 0):
					#print c
					fatto=1
					primecols[i]=c
				if(val2>155 and fatto2 == 0):
					#print (w-c-1)
					fatto2=1
					ultimecols[i]=w-c-1  
			larghezze[i]=ultimecols[i]-primecols[i]

		##print larghezze
		#ORA CREO TABELLA DI RICONOSCIMENTO CHE CONTIENE LE PRIME E ULTIME RIGHE E COLONNE NORMALIZZATE DOPO CHE PER OGNI GRUPPO E STATA SOTTRATTA LA PIU
		#PICCOLA!
		minpr=min(primerighe)
		minpc=min(primecols)
		minur=min(ultimerighe)
		minuc=min(ultimecols)

		for i in range(0,4):
			primerighe[i] = (primerighe[i]-minpr)/float(h)
			ultimerighe[i] = (ultimerighe[i]-minur)/float(h)
			primecols[i] = (primecols[i]-minpc)/float(w)
			ultimecols[i] = (ultimecols[i]-minuc)/float(w)

		risultati = primerighe + ultimerighe + primecols + ultimecols

		return risultati

