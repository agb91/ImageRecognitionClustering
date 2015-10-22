# -*- coding: cp1252 -*-
import json
import os
import time
import requests
from PIL import Image
from StringIO import StringIO
from requests.exceptions import ConnectionError
from accessoCartella import accessoCartella



class Download:
  def go(self,query, path, numImm, googleIndex):
    """Download full size images from Google image search.

    Don't print or republish images without permission.
    I used this to train a learning algorithm.
    """
    BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?'\
               'v=1.0&q=' + query + '&start=%d'
   

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
      #while start < numImm: # Google will only return a max of 56 results.
      r = requests.get(BASE_URL % start)
      
      for image_info in json.loads(r.text)['responseData']['results']:
        print "start ciclo: " + str(start)
        url = image_info['unescapedUrl']
        if(url in urlVec):
          start+=1
        else:
          urlVec.append(url)

        try:
          image_r = requests.get(url)
          
        except ConnectionError, e:
          print 'could not download %s' % url
          j-=1
          continue
        
        if(j<10):
          title=query+"00"+str(j)
        elif(j<100):
          title=query+"0"+str(j)
        else:
          title=query+str(j)
        j+=1
        
        FILE_PATH=os.path.join(path, '%s.jpg') % title
        
        file = open(FILE_PATH, 'wb')
      
        try:
          image=Image.open(StringIO(image_r.content))
          wpercent=(baseWidth/float(image.size[0]))
          hsize = int(float(image.size[1])*float(wpercent))
          image=image.resize((baseWidth, hsize), Image.ANTIALIAS)
          image.save(file, 'JPEG')
        except IOError, e:
          # Throw away some gifs...blegh.
          print 'could not save %s' % url
          start+=1
          j-=1
          continue
        finally:
          file.close()

        start+=1
        # Una volta raggiunto il numero di immagini interrompe il ciclo!
        print "j: " +str(j)
        if(j>=numImm):
          return start
      time.sleep(1.5)
      k=len(imageFolder.leggi(path))



    
  # Example use

