import sys
sys.path.insert(0, "./Scripts")
import funzioniDB as fdb
import cv2
import numpy as np

MSG_INPUT = "Inserisci un ID (per questo esempio, inserire un ID compreso tra 146 e 168): "
MSG_ERRORE_k_BASSO = "Errore: inserire un ID maggiore o uguale a 0"
MSG_ERRORE_NO_INT = "Non e' stato inserito un numero intero, riprovare."

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def acquireID():
    inputOk = False
    k = 0
    while inputOk!=True:
        inp = raw_input(MSG_INPUT)
        if isInt(inp):
            k = int(inp)
            if k>=0:
                inputOk=True
            else:
                print MSG_ERRORE_ID_BASSO
        else:
            print MSG_ERRORE_NO_INT
    return k

esci = False
while not esci:
    path = fdb.getPath(acquireID())
    if path!="":
        esci = True
img = cv2.imread(path, cv2.IMREAD_COLOR)
cv2.imshow("pippo", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
