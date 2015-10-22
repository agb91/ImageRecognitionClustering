import numpy as np
import cv2
import os
import MySQLdb as mdb
import sys

STR_ERROR = "Error %d: %s"
STR_ERR_ID = "L'ID inserito non e' contenuto nel database"
STR_EMPTY_DB = "Il database delle immagini e' vuoto. Premi invio per uscire."

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "imagerecognize"
DB_TABLE = "dbtable"
ID_NAME = "ID"
CLASS_NAME = "classe"
NAME_NAME = "nome"
PATH_NAME = "path"
ID_INDEX = 0
CLASS_INDEX = 1
NAME_INDEX = 2
PATH_INDEX = 3

#DB (dbTable) fatto cosi': ID classe nome path
#credenziali su FB

def deleteDuplicates():
    toDel = []
    
    try:
        conn = mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        cur = conn.cursor()
        cur.execute("LOCK TABLES %s WRITE" % DB_TABLE)
        cur.execute("SELECT * FROM %s" % (DB_TABLE))

        res = cur.fetchall()

        for i in range(0, len(res)):
            if not [res[i][ID_INDEX], res[i][NAME_INDEX], res[i][PATH_INDEX]] in toDel:
                img1 = cv2.imread(res[i][PATH_INDEX]+res[i][NAME_INDEX], cv2.IMREAD_COLOR)
                class1 = res[i][CLASS_INDEX]
                cur.execute("SELECT * FROM %s WHERE %s = %s" %
                            (DB_TABLE, CLASS_NAME, "'"+class1+"'"))
                res2 = cur.fetchall()

                for j in range(0, len(res2)):
                    if not res2[j][ID_INDEX]==res[i][ID_INDEX]:
                        img2 = cv2.imread(res2[j][PATH_INDEX]+res2[j][NAME_INDEX], cv2.IMREAD_COLOR)
                        if img1.shape == img2.shape and not(np.bitwise_xor(img1,img2).any()):
                            if not [res2[j][ID_INDEX], res2[j][NAME_INDEX], res2[j][PATH_INDEX]] in toDel:
                                toDel.append([res2[j][ID_INDEX], res2[j][NAME_INDEX], res2[j][PATH_INDEX]])

        cur.execute("UNLOCK TABLES")
            
        for elem in toDel:
            os.remove(elem[2]+elem[1])
            cur.execute("DELETE FROM %s WHERE %s = %s" %
                        (DB_TABLE, ID_NAME, int(elem[0])))
            conn.commit()


    except mdb.Error, e:
        print STR_ERROR % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.close()

#crea una cosa tipo [["scarpe", [1,5]], ["auto", [3, 2, 4]]]

def getDataset():
    toRet = []
    try:
        conn = mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        cur = conn.cursor()
        cur.execute("LOCK TABLES %s WRITE" % (DB_TABLE))
        cur.execute("SELECT DISTINCT %s FROM %s" % (CLASS_NAME, DB_TABLE))
        
        cont = True

        while cont:
            res = cur.fetchone()
            if not res==None:
                for elem in res:
                    toRet.append([elem, []])
            else:
                cont = False

        if len(toRet)==0:
            raw_input(STR_EMPTY_DB)
            return []
        else:
            cur.execute("SELECT %s, %s FROM %s" % (ID_NAME, CLASS_NAME, DB_TABLE))

            res = cur.fetchall()
            
            for row in res:
                for i in range(0, len(toRet)):
                    if toRet[i][0]==row[CLASS_INDEX]:
                        toRet[i][1].append(int(row[ID_INDEX]))

            cur.execute("UNLOCK TABLES")

    except mdb.Error, e:
        print STR_ERROR % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.close()

    return toRet

def getDatasetLen():
    toRet = -1
    try:
        conn = mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM %s" % (DB_TABLE))

        res = cur.fetchall()
        toRet = len(res)

    except mdb.Error, e:
        print STR_ERROR % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.close()

    return toRet

def getPath(ID):
    toRet = ""
    try:
        conn = mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM %s WHERE %s = %s" %
                    (DB_TABLE, ID_NAME, int(ID)))

        res = cur.fetchall()

        if len(res)>0:
            toRet = res[0][PATH_INDEX].replace("./", "../")+res[0][NAME_INDEX]
        else:
            print STR_ERR_ID

    except mdb.Error, e:
        print STR_ERROR % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.close()

    return toRet

def getClass(ID):
    toRet = ""
    try:
        conn = mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM %s WHERE %s = %s" %
                    (DB_TABLE, ID_NAME, int(ID)))

        res = cur.fetchall()

        if len(res)>0:
            toRet = res[0][CLASS_INDEX]
        else:
            print STR_ERR_ID

    except mdb.Error, e:
        print STR_ERROR % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.close()

    return toRet
    
    
