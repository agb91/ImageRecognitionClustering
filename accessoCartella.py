from os import listdir
import shutil
from os.path import isfile, join
import os


class accessoCartella:
        def leggi(self, path):
                try: 
                        onlyfiles = [ str(f) for f in listdir(path) if isfile(join(path,f)) ]
                except OSError as  err:
                        print("Nothin in the Path:{}".format(err))
                        return []
		return onlyfiles
		
	def cancella(self, path):
                try: 
                        shutil.rmtree(path)
                except OSError as  err:
                        print("Nothin in the Path:{}".format(err))

	def cancellaFile(self, path, _file):
                filename=join(path, _file)
                try:
                    os.remove(filename)
                except OSError:
                    pass
			  
	  
	  
	  


