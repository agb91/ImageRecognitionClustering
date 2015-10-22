# -*- coding: cp1252 -*-
import json
import os
import time
import requests
from PIL import Image
from StringIO import StringIO
from requests.exceptions import ConnectionError
from accessoCartella import accessoCartella
from croppaSfondo import croppaSfondo

def createUrls(q):
	query2 = q[:-2]+" "+q[-2:]
	query3 = q[:-3]+" "+q[-3:]
	BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?'\
			   'v=1.0&q=' + q + '&start=%d' + '&rsz=1'
	BASE_URL2 = 'https://ajax.googleapis.com/ajax/services/search/images?'\
			   'v=1.0&q=' + q + 's&start=%d' + '&rsz=1'
	BASE_URL3 = 'https://ajax.googleapis.com/ajax/services/search/images?'\
			   'v=1.0&q=' + query2 + '&start=%d' + '&rsz=1'
	BASE_URL4 = 'https://ajax.googleapis.com/ajax/services/search/images?'\
			   'v=1.0&q=' + query3 + '&start=%d' + '&rsz=1'
	return [BASE_URL, BASE_URL2, BASE_URL3, BASE_URL4]
	
def createRequests(vurls, start):
	vrisp = []
	for i in range(0,len(vurls)):
		vrisp.append(requests.get(vurls[i] % start))
	return vrisp

def setTitle(q,j):
	if(j<10):
		title=q+"00"+str(j)
	elif(j<100):
		title=q+"0"+str(j)
	else:
		title=q+str(j)
	return title
	
def dimensiona(i):
	baseWidth = 500
	wpercent=(baseWidth/float(i.size[0]))
	hsize = int(float(i.size[1])*float(wpercent))
	i=i.resize((baseWidth, hsize), Image.ANTIALIAS)
	return i
	
		


class Download:
	def go(self,query, path, numImm, googleIndex):
		vBaseUrls = createUrls(query)
		
		if not os.path.exists(path):
		  os.makedirs(path)

		imageFolder=accessoCartella()

		# Google's start query string parameter for pagination.
		urlVec=[]

		k=len(imageFolder.leggi(path))

		baseWidth=500
		ciclo=0
		start=googleIndex
		print "start Iniziale: " + str(start)
		j=k

		while k<numImm:
			vector=[]
			vetr = createRequests(vBaseUrls,start)
				  
			for i in range(0,3):
			  quale = vetr[i];
			  for image_info in json.loads(quale.text)['responseData']['results']:
				print "start ciclo: " + str(start)
				url = image_info['unescapedUrl']
				if(url in urlVec):
				  start+=0
				else:
				  urlVec.append(url)
				  try:
					image_r = requests.get(url)
					
				  except ConnectionError, e:
					print 'could not download %s' % url
					j-=1
					continue
				  
				  title = setTitle(query,j)
				  j+=1
				  
				  FILE_PATH=os.path.join(path, '%s.jpg') % title
				  
				  file = open(FILE_PATH, 'wb')
				
				  try:
					image=Image.open(StringIO(image_r.content))
					image=dimensiona(image)
					image.save(file, 'JPEG')
				  except IOError, e:
					# Throw away some gifs...blegh.
					print 'could not save %s' % url
					#start+=1
					j-=1
					continue
				  finally:
					file.close()

				  #start+=1
				  # Una volta raggiunto il numero di immagini interrompe il ciclo!
				  print "j: " +str(j)
				  if(j>=numImm):
					return start

			time.sleep(1.5)
			start+=1
			k=len(imageFolder.leggi(path))
