import sys
sys.path.insert(0, "./Scripts")
import json
import os
import shutil
import funzioniDB as fdb

STR_DIRECTORY = "."+os.sep+"Temp"+os.sep
STR_CLASSIFICATION_FILE = "ClassFile"
STR_CONF_FILE = "ConfFile"
STR_RES_FILE = "Results.txt"
STR_ESTENSIONE = ".dip"
MSG_NO_DIR = "Una directory necessaria non e' stata trovata, ripetere il processo di cross-validazione"

def loadResults(ind):
    resFile = open(STR_DIRECTORY+STR_CLASSIFICATION_FILE+str(ind)+STR_ESTENSIONE, "r")
    results = json.load(resFile)
    resFile.close()
    return results
    #results: del tipo [id, [ranking]]. Es.: [[1, [["scarpa", 0.67], ["cane", 0.12], ...]], [2, [...]]]

def loadConf():
    confFile = open(STR_DIRECTORY+STR_CONF_FILE+STR_ESTENSIONE, "r")
    conf = json.load(confFile)
    confFile.close()
    return conf

def analyzeResults(results, classList, confMatrices):
    confMatrix = [[0 for x in range(0,len(classList))] for x in range(0,len(classList))]
    for inst in results:
        trueClass = fdb.getClass(inst[0])
        resultClass = inst[1][0][0]
        confMatrix[classList.index(trueClass)][classList.index(resultClass)]+=1

    correctClassif = 0
    for i in range(0, len(classList)):
        correctClassif+=confMatrix[i][i]
    accuracy = correctClassif*(1.0/len(results))
    confMatrices.append(confMatrix)

    return accuracy

def mean(accuracyList):
    tot = 0
    for i in range(0,len(accuracyList)):
        tot += accuracyList[i]
    return tot/len(accuracyList)

def stringLegend(classes):
    STR_TITOLO_LEGENDA = "Legenda degli indici:"
    toRet = ""
    toRet+= "\n"+STR_TITOLO_LEGENDA+"\n\n"
    for i in range(0,len(classes)):
        toRet += str(i) + " -> " + classes[i] + "\n\n"
    toRet += "\n\n"
    return toRet

def stringMatrix(matrix):
    toRet = ""
    toRet += ("{:4}".format("")+''.join(['{:4}'.format(elem) for elem in range(0,len(matrix))]))
    toRet += "\n"
    for rowInd in range(0,len(matrix[0])):
        toRet+="\n"
        toRet+="{:4}".format(rowInd)
        for colInd in range(0,len(matrix[0])):
            toRet+="{:4}".format(matrix[rowInd][colInd])
        rowInd+=1
    toRet += "\n\n\n"
    return toRet
    

acc = []
confMatrices = []
conf = loadConf()
k = conf[0]
classes = conf[1]
if k>0:
    for i in range(0,k):
        acc.append(analyzeResults(loadResults(i), classes, confMatrices))

    toSave = ""
    toSave += "\nAccuratezza complessiva = " + str(mean(acc)*100) + "%\n\n"
    toSave+= "--------------------------\n"
    toSave += "RISULTATI INTERMEDI\n"
    toSave += "--------------------------\n\n\n"
    toSave += stringLegend(classes)
    print "\n"
    for i in range(0,k):
        toSave += "RISULTATI ITERAZIONE " + str(i) + "\n"
        toSave += "\nMatrice di confusione:\n\n"
        toSave += stringMatrix(confMatrices[i])
        toSave += "Accuratezza = " + str(acc[i]*100) + "%\n\n\n\n"

    resFile = open(STR_RES_FILE, "w")
    resFile.write(toSave)
    resFile.close()
shutil.rmtree(STR_DIRECTORY)

