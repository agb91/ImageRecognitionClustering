import numpy as np
import json
import os
import funzioniDB as fdb

STR_DIRECTORY = "."+os.sep+"Temp"+os.sep
STR_TEST_FILE = "TestSet"
STR_TRAINING_FILE = "TrainingSet"
STR_CONF_FILE = "ConfFile"
STR_ESTENSIONE = ".dip"
MSG_NO_FILE = "Un file necessario non e' stato trovato, ripetere il processo di cross-validazione"

def getNumIter():
    try:
        aFile = open(STR_DIRECTORY+STR_CONF_FILE+STR_ESTENSIONE, "r")
    except (OSError, IOError):
        print MSG_NO_FILE
        return -1
    numIter = json.load(aFile)[0]
    aFile.close()
    return numIter

def getClasses():
    try:
        aFile = open(STR_DIRECTORY+STR_CONF_FILE+STR_ESTENSIONE, "r")
    except (OSError, IOError):
        print MSG_NO_FILE
        return -1
    numIter = json.load(aFile)[1]
    aFile.close()
    return numIter

def getTrainingSet(numIter):
    try:
        aFile = open(STR_DIRECTORY+STR_TRAINING_FILE+str(iter)+STR_ESTENSIONE, "r")
    except (OSError, IOError):
        print MSG_NO_FILE
        return []
    toRet = json.load(aFile)
    aFile.close()
    return toRet

def getTestSet(numIter):
    try:
        aFile = open(STR_DIRECTORY+STR_TEST_FILE+str(numIter)+STR_ESTENSIONE, "r")
    except (OSError, IOError):
        print MSG_NO_NO_FILE
        return []
    toRet = json.load(aFile)
    aFile.close()
    return toRet
