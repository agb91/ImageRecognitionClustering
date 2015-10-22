import numpy as np
import json
import os

STR_DIRECTORY = "."+os.sep+"Temp"+os.sep
STR_CLASSIFICATION_FILE = "ClassFile"
STR_ESTENSIONE = ".dip"
MSG_NO_DIR = "Una directory necessaria non e' stata trovata, ripetere il processo di cross-validazione"

def saveRanking(numIter, ranking):
    if os.path.exists(STR_DIRECTORY):
        aFile = open(STR_DIRECTORY+STR_CLASSIFICATION_FILE+str(numIter)+STR_ESTENSIONE, "w")
        json.dump(ranking, aFile)
        aFile.close()
    else:
        print MSG_NO_DIR
