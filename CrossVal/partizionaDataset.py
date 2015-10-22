import sys
sys.path.insert(0, "./Scripts")
import random
import json
import os
import errno
import funzioniDB as fdb

MSG_INPUT = "Inserisci k (numero di round di cross-validazione): "
MSG_ERRORE_k_ALTO = "E' stato inserito un valore di k troppo alto. Inserire un valore minore della meta' della dimensione del dataset, ossia di "
MSG_ERRORE_k_BASSO = "E' stato inserito un valore di k minore di 2"
MSG_ERRORE_NO_INT = "Non e' stato inserito un numero intero, riprovare."
STR_DIRECTORY = "."+os.sep+"Temp"+os.sep
STR_TEST_FILE = "TestSet"
STR_TRAINING_FILE = "TrainingSet"
STR_CONF_FILE = "ConfFile"
STR_ESTENSIONE = ".dip"

def genTempList(k):
    toRet = []
    for i in range(0, k):
        toRet.append(i)
    return toRet

def partitionDataset(datasetList, k):
    testSets = [[] for x in range(0,k)]
    trainingSets = [[] for x in range(0,k)]
    temp = genTempList(k)

    for i in range(0, len(datasetList)):
        for elem in datasetList[i][1]:
            rand = random.choice(temp)
            temp.remove(rand)
            testSets[rand].append(elem)
            for j in range(0, k):
                if j!=rand:
                    trainingSets[j].append([elem, datasetList[i][0]])
            if len(temp)==0:
                temp = genTempList(k)
    saveDatasetFiles(trainingSets, testSets, k)


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def acquireK(kMax):
    inputOk = False
    k = 0
    while inputOk!=True:
        inp = raw_input(MSG_INPUT)
        if isInt(inp):
            k = int(inp)
            if k>1:
                if k<=kMax:
                    inputOk=True
                else:
                    print MSG_ERRORE_k_ALTO + str(kMax)
            else:
                print MSG_ERRORE_k_BASSO
        else:
            print MSG_ERRORE_NO_INT
    return k

def createTempDir():
    try:
        os.makedirs(STR_DIRECTORY)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def saveConfFile(k, dataset):
    classes = []
    for elem in dataset:
        classes.append(elem[0])
    confFile = open(STR_DIRECTORY+STR_CONF_FILE+STR_ESTENSIONE, "w")
    json.dump([k, classes], confFile)
    confFile.close()

def saveDatasetFiles(training, test, k):
    for i in range(0, k):
        testFile = open(STR_DIRECTORY+STR_TEST_FILE+str(i)+STR_ESTENSIONE, "w")
        trainFile = open(STR_DIRECTORY+STR_TRAINING_FILE+str(i)+STR_ESTENSIONE, "w")
        json.dump(test[i], testFile)
        json.dump(training[i], trainFile)

dataset = fdb.getDataset()
createTempDir()
if len(dataset)>0:
    k = acquireK(fdb.getDatasetLen()//2)
    partitionDataset(dataset, k)
    saveConfFile(k, dataset)
else:
    saveConfFile(0, [])
            
    
