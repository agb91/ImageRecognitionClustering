# -*- coding: cp1252 -*-
import mysql.connector
from mysql.connector import Error

class sqlQuery:

    # ************************* Query per la creazione del database *****************
    """
        Metodo per la creazione del database
        si consiglia di chiamarlo solo se necessario,
        per evitare spreco di tempo
        in quanto se esiste gia non fara nulla!
        Inoltre in questo punto si aprono e si chiudono le connessioni
        a differenza di tutte le altre funzioni della classe!
    """
    def createDB(self, _host, _user, _password, dbName):
        try:
            conn=mysql.connector.connect(host=_host, user=_user, passwd=_password)
            cursor=conn.cursor()
            sql='CREATE DATABASE {}'.format(dbName)
            cursor.execute(sql)
        except Error as err:
            print("Feaild create database:{}".format(err))
        finally:
            cursor.close()
            del cursor
            conn.close()

            
    # ******************** Query per la connessione al database ************ 
    """
        Metodo per aprire la connessione al databese, se fallisce mi ritorna None
        altrimenti mi ritorna la connessione
    """
    def connectMySql(self, _host, _user, _password, dbName):
        try:
            conn=mysql.connector.connect(host=_host, user=_user, passwd=_password, db=dbName)
        except Error as err:
            print("Feaild connection mySql:{}".format(err))
            return None
        return conn



    
    # ****************** Query per la creazione e per la manipolazione della mainTable ****************
    """
        Metodo per la creazione della tabella generale (mainTable)
        è consigliabile chiamarlo una sola volta per non incorrere
        in exception in quanto la tabella esiste
        La mainTable contiene le parole chiavi cercate e relativo path
        per accedere alla cartella in cui sono salvate le immagini
    """
    def createMainTable(self, conn, mainTable):
        try:
            cursor=conn.cursor()
            sql="""CREATE TABLE IF NOT EXISTS %s(
                    ID INT NOT NULL AUTO_INCREMENT,
                    Object varchar(128) NOT NULL,
                    numeroImm INT(3) NOT NULL,
                    googleIndex INT(3) NOT NULL DEFAULT 0,
                    Path varchar(255) NOT NULL,
                    PRIMARY KEY(ID),
                    UNIQUE(Object)
                    );""" %mainTable
            cursor.execute(sql)
        except Error as err:
            print("Feaild create table:{}".format(err))
        finally:
            cursor.close()
            del cursor

    """
        Metodo per inserire un nuovo oggetto e relativo path nella tabella principale,
        successivamente il valore dell'ogetto sara utilizzato anche come nome del database
        contenente informazioni su quell'ogetto
        nel caso si cerchi di inserire valori gia presenti nel database entra in exception
    """
    def insertMainTable(self, conn, mainTable, _object, numeroImm, googleIndex, path):
        try:
            cursor=conn.cursor()
            path=path.replace('\\','\\\\')
            sql="""INSERT INTO {}(Object,numeroImm,googleIndex, Path)
                   VALUES (\"{}\", \"{}\", \"{}\", \"{}\");""".format(mainTable, _object, numeroImm, googleIndex, path)
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild insert value:{}".format(err))
        finally:
            cursor.close()
            del cursor


    """
        Metodo per selezionare il path contenente
        le immagini dato un certo oggetto ricercato
        Return:  risultato di cursor.fetchall, se non ci sono stati errori,
        altrimenti return None
    """
    def selectPathMainTable(self, conn, mainTable, _object):
        data=None
        try:
            cursor=conn.cursor()
            sql="""SELECT Path FROM {} WHERE Object=\"{}\";""".format(mainTable, _object)
            cursor.execute(sql)
            data = cursor.fetchall()
        except Error as err:
            print("Feaild select Path:{}".format(err))
        finally:
            cursor.close()
            del cursor
        return data

    """
        Metodo per eliminare le righe con Object=_object dalla tabella principale (mainTable)
    """
    def deleteRowMainTable(self, conn, mainTable, _object):
        try:
            cursor=conn.cursor()
            sql="""DELETE FROM {} WHERE Object=\"{}\";""".format(mainTable, _object)
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild delete Path:{}".format(err))
        finally:
            cursor.close()
            del cursor

    """
        Metodo per eliminare tutte le ricerche dalla tabella principale (mainTable)
    """
    def deleteAllMainTable(self, conn, mainTable):
        try:
            cursor=conn.cursor()
            sql="""DELETE FROM {};""".format(mainTable)
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild delete Path:{}".format(err))
        finally:
            cursor.close()
            del cursor


    """
        Metodo per aggiornare il path dato una ricerca gia esistente
    """
    def updatePathMainTable(self, conn, mainTable, _object, path):
        try:
            cursor=conn.cursor()
            sql="""UPDATE {} SET Path=\'{}\'
                   WHERE Object=\'{}\';
                  """.format(mainTable, path, _object)
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild update Path:{}".format(err))
        finally:
            cursor.close()
            del cursor

    """
        Metodo per selezionare il path contenente le immagini
        dato un certo oggetto ricercato
        restituisce il risultato di cursor.fetchall() se tutte
        le operazioni hanno avuto succetto, None altrimenti
    """
    def selectObjectMainTable(self, conn, mainTable, _object):
        data=None
        try:
            cursor=conn.cursor()
            sql="""SELECT Object FROM {} WHERE Object=\"{}\";""".format(mainTable, _object)
            cursor.execute(sql)
            data = cursor.fetchall()
            conn.commit()
        except Error as err:
            print("Feaild select Path:{}".format(err))
        finally:
            cursor.close()
            del cursor
        return data

    """
        Metodo per selezionare indice a cui era arrivato google 
        dopo il download restituisce il risultato di cursor.fetchall() 
        se tutte le operazioni hanno avuto succetto, None altrimenti
    """
    def selectGoogleIndexMainTable(self, conn, mainTable, _object):
        data=None
        try:
            cursor=conn.cursor()
            sql="""SELECT googleIndex FROM {} WHERE Object=\"{}\";""".format(mainTable, _object)
            cursor.execute(sql)
            data = cursor.fetchall()
            conn.commit()
        except Error as err:
            print("Feaild select googleIndex:{}".format(err))
        finally:
            cursor.close()
            del cursor
        return data

    """
        Metodo per aggiornare l'indice di google dato una ricerca gia esistente
    """
    def updateGoogleIndexNumImmMainTable(self, conn, mainTable, _object,numeroImm, google):
        try:
            cursor=conn.cursor()
            sql="""UPDATE {} SET googleIndex=\'{}\',numeroImm=\'{}\'
                   WHERE Object=\'{}\';
                  """.format(mainTable, google,numeroImm, _object)
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild update googleIndex:{}".format(err))
        finally:
            cursor.close()
            del cursor



    # ****************** Query per la creazione e manipolazione della tabella contenente i risultati
    # della clusterizzazione (clustTable) **********************************************************

    """
        Metodo per la creazione della tabella contenente le informazioni
        della clusterizzazione (clustTable) è consigliabile chiamarlo una sola volta per non incorrere
        in exception in quanto la tabella esiste
    """
    def createClustTable(self, conn, clustTable):
        try:
            cursor=conn.cursor()
            sql="""CREATE TABLE IF NOT EXISTS %s(
                    ID INT NOT NULL AUTO_INCREMENT,
                    Search varchar(128) NOT NULL,
                    ImageName varchar(128) NOT NULL,
                    Rank Double(3,2) NOT NULL DEFAULT 0.00,
                    Class INT NOT NULL DEFAULT 0,
                    PRIMARY KEY(ID),
                    UNIQUE(ImageName)
                    );""" %clustTable
            
            cursor.execute(sql)
        except Error as err:
            print("Feaild create table:{}".format(err))
        finally:
            cursor.close()
            del cursor

    """
        Metodo per l'iserimento di nuovi valori nella tabella contenente infromazioni
        sulla clusterizzazione (clustTable)
        Se ImageName e' gia' presente nella tabella, non vera' inserito nuovamente
        Solitamente nel main chiamo questo metodo con i valori della clusterizzazione
        nulli, solo in seguito saranno aggiornati!
    """
    def insertInClustTable(self, conn, clustTable, toSearch, _name, _rank, _class):
        try:
            cursor=conn.cursor()
            sql="""INSERT INTO {}(Search, ImageName,  Rank, Class)
                   VALUES (\"{}\",\"{}\",\"{}\", \"{}\")
                  ;""".format(clustTable, toSearch, _name, _rank, _class)
            
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild insert value:{}".format(err))
        finally:
            cursor.close()
            del cursor

    """
        Metodo per l'aggiornamento dei record nella tabella contenente infromazioni
        sulla clusterizzazione (clustTable)
    """
    def updateClustTable(self, conn, clustTable, toSearch, _name, _rank, _class):
        try:
            cursor=conn.cursor()
            sql="""UPDATE {} SET Rank=\'{}\', Class=\'{}\'
                   WHERE ImageName=\'{}\' AND Search=\'{}\';
                  """.format(clustTable, _rank, _class, _name, toSearch)
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild update value:{}".format(err))
        finally:
            cursor.close()
            del cursor

    """
        Metodo per la cancellazione dei record corrispondenti alla parola toSearch
        nella tabella contenente infromazioni sulla clusterizzazione (clustTable)
    """
    def deleteSearchClustTable(self, conn, clustTable, toSearch):
        try:
            cursor=conn.cursor()
            sql="""DELETE FROM {} WHERE Search=\"{}\";""".format(clustTable, toSearch)
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild delete value:{}".format(err))
        finally:
            cursor.close()
            del cursor
    """
        Metodo per la cancellazione dei record corrispondenti alla parola toSearch
        nella tabella contenente infromazioni sulla clusterizzazione (clustTable)
    """
    def deleteElementClustTable(self, conn, clustTable, immName):
        try:
            cursor=conn.cursor()
            sql="""DELETE FROM {} WHERE ImageName=\"{}\";""".format(clustTable, immName)
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild delete value:{}".format(err))
        finally:
            cursor.close()
            del cursor

    """
        Metodo per la selezione dei record corrispondenti alla parola toSearch
        nella tabella contenente infromazioni sulla clusterizzazione (clustTable)
    """
    def selectRecordsClustTable(self, conn, clustTable, toSearch):
        data=None
        try:
            cursor=conn.cursor()
            sql="""SELECT Search FROM {} WHERE Search=\"{}\";""".format(clustTable, toSearch)
            cursor.execute(sql)
            data = cursor.fetchall()
            conn.commit()
        except Error as err:
            print("Feaild select Path:{}".format(err))
        finally:
            cursor.close()
            del cursor
        return data
    """
        Metodo per eliminare tutte le informazioni nella tabella
        contenente infromazioni sulla clusterizzazione (clustTable)
    """
    def deleteAllClustTable(self, conn, clustTable):
        try:
            cursor=conn.cursor()
            sql="""DELETE FROM {};""".format(clustTable)
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild delete value:{}".format(err))
        finally:
            cursor.close()
            del cursor
            

    #******************************* QUERY SU TABELLA DI INPUT *****************************
    """
        Metodo per la lettura dei parametri contenuti nella tabella inputTable
        restituisce il risultato di cursor.fetchall() se tutte
        le operazioni hanno avuto succetto, None altrimenti
    """
    def readInputParams(self, conn, inputTable):
        data=None
        try:
            cursor=conn.cursor()
            sql="""SELECT algoritmo1,algoritmo2, algoritmo3, numClassi FROM {} WHERE ID ='0'""".format(inputTable)
            cursor.execute(sql)
            data = cursor.fetchall()   
        except Error as err:
            print("Feaild select :{}".format(err))
        finally:
            cursor.close()
            del cursor
        return data

    """
        Metodo per la lettura dei dati necessari per il download nella tabella inputTable
        restituisce il risultato di cursor.fetchall() se tutte
        le operazioni hanno avuto succetto, None altrimenti
    """
    def readInputDownload(self, conn, inputTable):
        data=None
        try:
            cursor=conn.cursor()
            sql="SELECT toSearch, numImages, deleteSearch, deleteAll, selectCluster FROM {} WHERE ID ='0'".format(inputTable)
            cursor.execute(sql)
            data = cursor.fetchall()
        except Error as err:
            print("Feaild select :{}".format(err))
        finally:
            cursor.close()
            del cursor
        return data

    # ATTENZIONE: le query: createInputTable(...), insertInputTable(...) e updateInputTable(...) devono essere implementate
    # dall'interfaccia web, importante ID=0!
    """
        Metodo per la creazione della tabella dei dati in input (inputTable)
        La tabella inputTable tecnicamente è aggiornata e creata dall'interfaccia web,
        allo stato attuale il metodo serve solo per comodità di utilizzo del
        senza interfaccia web.
        E' importante modificare sempre la stessa riga, corrispondente ad ID=0!
    """
    def createInputTable(self,conn, inputTable):
        try:
            cursor=conn.cursor()
            # ATTENZIONE Modificare sempre la stessa riga con ID=0!
            # deleteAll Svuota completamente tutto
            # deleteSearch cancella le ricerche precedenti relative a quella ricerca
            sql="""CREATE TABLE IF NOT EXISTS %s(
                    ID INT(1) NOT NULL DEFAULT 0,
                    toSearch varchar(128) NOT NULL,
                    numImages INT(3) NOT NULL DEFAULT 10,
                    deleteSearch INT(1) NOT NULL DEFAULT 0,
                    deleteAll INT(1) NOT NULL DEFAULT 0,
                    selectCluster INT(1) NOT NULL DEFAULT 0,
                    algoritmo1 INT(1) NOT NULL DEFAULT 1,
                    algoritmo2 INT(1) NOT NULL DEFAULT 1,
                    algoritmo3 INT(1) NOT NULL DEFAULT 1,
                    numClassi INT(1) NOT NULL DEFAULT 8,
                    PRIMARY KEY(ID)
                    );""" %inputTable
                
            cursor.execute(sql)
        except Error as err:
            print("Feaild create table:{}".format(err))
        finally:
            cursor.close()
            del cursor

    """
        Metodo per l'inserimento di una riga nella tabella di input (inputTable)
        La tabella inputTable tecnicamente è aggiornata e creata dall'interfaccia web,
        allo stato attuale il metodo serve solo per comodità di utilizzo del
        senza interfaccia web.
        E' importante modificare sempre la stessa riga, corrispondente ad ID=0!
        Come si puo' notare la riga è inserita con ID=0.
    """
    def insertInputTable(self,conn, inputTable, toSearch, numImm, deleteSearch, deleteAll, selectCluster, algoritmo1, algoritmo2, algoritmo3, numClassi):
        try:
            cursor=conn.cursor()
            sql="""INSERT INTO {} (ID, toSearch, numImages, deleteSearch, deleteAll, selectCluster, algoritmo1, algoritmo2, algoritmo3, numClassi)
                    VALUES (0, \'{}\',\'{}\', \'{}\',\'{}\',\'{}\', \'{}\',\'{}\',\'{}\', \'{}\');
                  """.format(inputTable, toSearch, numImm, deleteSearch, deleteAll, selectCluster, algoritmo1, algoritmo2, algoritmo3, numClassi)
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild insert value:{}".format(err))
        finally:
            cursor.close()
            del cursor
            
    """
        Metodo per l'aggiornamento di una riga nella tabella di input (inputTable)
        La tabella inputTable tecnicamente e' aggiornata e creata dall'interfaccia web,
        allo stato attuale il metodo serve solo per comodità di utilizzo del
        senza interfaccia web.
        E' importante modificare sempre la stessa riga, corrispondente ad ID=0!
        Come si puo' notare la riga modificata  con ID=0.
    """
    def updateInputTable(self, conn, inputTable, toSearch, numImm, deleteSearch, deleteAll, selectCluster, algoritmo1, algoritmo2, algoritmo3, numClassi):
        try:
            cursor=conn.cursor()
            sql="""UPDATE {} SET toSearch=\'{}\', numImages=\'{}\', deleteSearch=\'{}\', deleteAll=\'{}\', selectCluster=\'{}\', algoritmo1=\'{}\', algoritmo2=\'{}\',
                    algoritmo3=\'{}\', numClassi=\'{}\'
                   WHERE ID='0';
                  """.format(inputTable, toSearch, numImm,deleteSearch, deleteAll, selectCluster, algoritmo1, algoritmo2, algoritmo3, numClassi)
            cursor.execute(sql)
            conn.commit()
        except Error as err:
            print("Feaild update value:{}".format(err))
        finally:
            cursor.close()
            del cursor
