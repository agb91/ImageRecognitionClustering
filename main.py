# -*- coding: cp1252 -*-
import os
from downloadImage import Download
from sqlQuery import sqlQuery
from accessoCartella import accessoCartella
from clusterizzaKMeans import clusterizzaKMeans
from clusterizzaBinario import clusterizzaBinario
from clusterizzaDBScan import clusterizzaDBScan

class Main:
  def main(self):

    # Dati per accesso e uso DB e tabelle
    host="127.0.0.1"
    user='root'
    password=''
    dbName="imageRecognize" # Nome del database
    mainTable="mainTable"   
    inputTable="inputTable"
    clustTable="clustTable"
    imm="imm"
  
    mn=Main()
    mySql = sqlQuery()
    imageFolder=accessoCartella()

    mySql.createDB(host, user, password, dbName) # Crea il database se non esiste
    
    
    conn = mySql.connectMySql(host, user, password, dbName) #Apertura connessione al database

    if(conn!=None):
      
      #*********************** CREAZIONE TABELLE ****************************
     
      mySql.createMainTable(conn, mainTable)
      mySql.createClustTable(conn, clustTable)
      mySql.createInputTable(conn, inputTable) # Questa non dovrà essere creata da qui ma da interfaccia

      "insertInputTable e updateInputTable Servono solo fintanto che manca interfaccia Web"
     
      #toSearch="fish"      # Parola da cercare
      #numImm=30              # Quante immagini scaricare
      #deleteSearch=0        # 0- non cancellare nulla (default); 1- cancella tutte le informazioni precedenti per una data ricerca!
      #deleteAll=0           # 0- non cancellare nulla (default); 1- cancella, Database con il nome, cancella tutte le immagini nella cartella con path
      #algoritmo1=1          # Uso Sift 0-NO, 1-SI
      #algoritmo2=1          # Uso Shape 0-NO, 1-SI
      #algoritmo3=1          # Uso Orb 0-NO, 1-SI
      #selezionaClust=0      # 0: Default dv Scan, 1: KMeans, 2: Binario!
      #numClassi=5           # numero di classi
      
      #mySql.insertInputTable(conn, inputTable, toSearch, numImm, deleteSearch, deleteAll, selezionaClust, algoritmo1, algoritmo2, algoritmo3, numClassi) # Inserisce se la tabella e' appena stata creata

      #mySql.updateInputTable(conn, inputTable, toSearch, numImm, deleteSearch, deleteAll, selezionaClust, algoritmo1, algoritmo2, algoritmo3, numClassi) # Aggiorna 


      # ********************************** LETTURA DATI DALLA TABELLA DI INPUT ********************************************************************** 
      dataClust=mySql.readInputParams(conn, inputTable) # dataClust contiene i dati da mandare in input a clusterizza come restituiti da cursor.fetchAll
      arrayDataClust=mn.fetchAllToArray(dataClust) 
       
      dataSearch=mySql.readInputDownload(conn, inputTable)# dataSearch contiene i dati da mandare in input a Download e alle varie query (dove necessario) come restituiti da cursor.fetchAll
      arrayDataSearch=mn.fetchAllToArray(dataSearch)

      #Assegnamento Dati Input
      toSearchDownload=arrayDataSearch[0] #La parola che useremo per il download delle immagini cosi come arriva da interfaccia web
      toSearch=toSearchDownload.replace(' ','_') #La parola che useremo per tutte le operazioni sul database, e la creazione delle cartelle!
      numImm=arrayDataSearch[1] #Numero delle immagini da scaricare
      deleteSearch=arrayDataSearch[2]       # 0- non cancellare nulla (default); 1- cancella tutte le informazioni precedenti per una data ricerca!
      deleteAll = arrayDataSearch[3] # 0- non cancellare nulla (default); 1- cancella, cancella righe corrispondente a toSearch da mainTable e clustTable, cancella tutte le immagini nella cartella con path (Metodo AP)
      selezionaClust=arrayDataSearch[4]
      
      PATH = os.path.abspath(os.path.join(imm, toSearch)) #PATH della cartella contenente le immagini scaricate per la parola toSearchDownload
      pathImm = os.path.abspath(imm) # Path della cartella imm
      

      print("\n\n ********************* LETTURA DATI INPUT ************************* \n")


      mySql.deleteAllClustTable(conn, clustTable) # Ad ogni esecuzione svuota la clustTable
      
      if(deleteAll>0):
        mySql.deleteAllMainTable(conn, mainTable)
        mySql.deleteAllClustTable(conn, clustTable)
        imageFolder.cancella(pathImm)
        print ("\n ************** CANCELLATO TUTTO ***************** \n")

      elif(deleteSearch>0 and ((len(imageFolder.leggi(PATH))>0) or len(mySql.selectObjectMainTable(conn, mainTable, toSearch)))):
        imageFolder.cancella(PATH)
        mySql.deleteRowMainTable(conn, mainTable, toSearch)
        print ("\n ************** CANCELLA RICERCA PRECEDENTE ***************** \n")
        

      # Crea la cartella imm/toSearch
      if not os.path.exists(PATH):
        os.makedirs(PATH)

      # Se la ricerca non è nella main table la inserisce con googleIndex = 0
      mySql.insertMainTable(conn, mainTable, toSearch, numImm, 0, PATH)

      # Se la cartella contiene meno immagini di quelle da scaricare, scarica le restanti
      if(len(imageFolder.leggi(PATH))<numImm):
        googleIndexArray=mn.fetchAllToArray(mySql.selectGoogleIndexMainTable(conn, mainTable, toSearch))
        googleIndex=googleIndexArray[0]
        scarica=Download()
        googleIndex=scarica.go(toSearch, PATH, numImm, googleIndex)

        mySql.updateGoogleIndexNumImmMainTable(conn, mainTable, toSearch, len(imageFolder.leggi(PATH)), googleIndex)
        print ("\n\n *************************** FINE DOWNLOAD ********************************* \n\n")

      """
        Se il numero di immagini nella cartella è maggiore del numero di immagini
        da scaricare quando il numero di immagini da scaricare è diverso da 0
        allora cancella gli elementi in eccesso!
      """
      vet=imageFolder.leggi(PATH)    
      if(len(vet)>numImm and numImm!=0):
        googleIndexArray=mn.fetchAllToArray(mySql.selectGoogleIndexMainTable(conn, mainTable, toSearch))
        googleIndex=googleIndexArray[0]
        googleIndex=googleIndexArray[0] - (len(vet)-numImm)
        
        for i in range(numImm, len(vet)):
          imageFolder.cancellaFile(PATH, vet[i]);
        print ("\n\n ****************** IMMAGINI IN PIU' CANCELLATE *************************** \n\n")
        mySql.updateGoogleIndexNumImmMainTable(conn, mainTable, toSearch, len(imageFolder.leggi(PATH)), googleIndex)


      #Inserimento nella clustTable
      vet=imageFolder.leggi(PATH)
      if((len(vet)>0)):
        for i in range (0, len(vet)):
          mySql.insertInClustTable(conn, clustTable, toSearch, vet[i], '0.00','0')
 
      #vet=imageFolder.leggi(PATH)
      if (len(vet)!=0):
        
        if(selezionaClust==0):
          print("\n\n ***************** CLUSTERIZZAZIONE : DBScan *********************** \n")
          cl=clusterizzaDBScan()
        elif (selezionaClust==1):
          print("\n\n ***************** CLUSTERIZZAZIONE : KMeans *********************** \n")
          cl=clusterizzaKMeans()
        else:
          print("\n\n ****************  CLUSTERIZZAZIONE : Binario *********************** \n")
          cl=clusterizzaBinario()

          
        allVectors=cl.clusterizza(arrayDataClust, PATH)
        
        #allVectors contiene alla posizione: 0 - vettore nomi immagini; 1-vettore valori Rank; 2-vettore classificazione

        print("\n\n **************************** FINE CLUSTERIZZAZIONE *********************** \n")
        
        if allVectors!=None:
          for i in range(0, len(allVectors[0])):
            mySql.updateClustTable(conn, clustTable, toSearch, allVectors[0][i], allVectors[1][i], allVectors[2][i])
      else:
        print("Non ci sono immagini nella cartella!")

    conn.close()


  "Metodo per scrivere i riulstati dati da cursor.fetchall in un array"
  def fetchAllToArray(self, fetchall):    
    array=[]
    for row in fetchall:
      for i in range(0,len(row)):
        array.append(row[i])
        print str(i)+"-   " +str(row[i])
    return array


mn=Main()
mn.main()
