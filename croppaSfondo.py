import numpy as np
import cv2
from math import ceil
import math

def selezionaSfondo(daSelezionare):
	gray = daSelezionare#cv2.cvtColor(daSelezionare, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	kernel = np.ones((3,3),np.uint8)
	opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
	
	# sure background area, la nostra immagine per capire dove croppare
	sfondo = cv2.dilate(opening,kernel,iterations=3)
	return sfondo
	
def erodi(i):
	h, w = i.shape
	ritorna = i.copy()
	for	x in range(0,h-2):
		for y in range(0,w-2):
			if (i[x-1,y]>240 or i[x+1,y]>240 or i[x,y+1]>240 or i[x,y-1]>240 ):
				ritorna[x,y]=255
	return ritorna		
	
def allarga(i):
	h, w = i.shape
	ritorna = i.copy()
	for	x in range(0,h-2):
		for y in range(0,w-2):
			if (i[x-1,y]<40 or i[x+1,y]<40 or i[x,y+1]<40 or i[x,y-1]<40 ):
				ritorna[x,y]=0
	return ritorna			
		
def erodiAllarga(i):
	i=erodi(i)
	i=erodi(i)
	i=erodi(i)
	i=allarga(i)
	i=allarga(i)
	i=allarga(i)
	return i	

class croppaSfondo:
	def croppa(self,img):

		sure_bg=selezionaSfondo(img)
		sure_bg=erodiAllarga(sure_bg)
		cv2.imwrite("imm/sfondo.jpg",sure_bg)
		#DA QUI COMINCIO CON LA PRIMA IMMAGINE

		#PRIMA TROVO ALTEZZA E LARGHEZZA
		h, w = img.shape #depth non serve..

		print "height: %s" % h
		print "width: %s" % w

		marginTop=0
		marginBottom=0
		marginLeft=0
		marginRight=0
					
		fatto=0			
		for colonne in range(0,w-1):
			for righe in range(0,h-1):
				if(sure_bg[righe,colonne]>230 and fatto==0):
					fatto=1
					marginLeft=colonne
					
		fatto=0			
		for colonne in range(0,w-1):
			for righe in range(0,h-1):
				if(sure_bg[righe,w-1-colonne]>230 and fatto==0):
					fatto=1
					marginRight=w-1-colonne	
					
		fatto=0			
		for righe in range(0,h-1):
			for colonne in range(0,w-1):
				if(sure_bg[righe,colonne]>230 and fatto==0):
					fatto=1
					marginTop=righe		
					
		fatto=0			
		for righe in range(0,h-1):
			for colonne in range(0,w-1):
				if(sure_bg[h-1-righe,colonne]>230 and fatto==0):
					fatto=1
					marginBottom=h-1-righe							

		print "top: %s" % marginTop
		print "bottom: %s" % marginBottom
		print "left: %s" % marginLeft
		print "right: %s" % marginRight			

		croppata = img[marginTop:marginBottom, marginLeft:marginRight]#croppo sui limiti ottenuti

		#cv2.imwrite("risultato.jpg",croppata)
		return croppata




