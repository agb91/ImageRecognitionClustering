Questa versione di prova utilizza un database di immagini ad hoc ed effettua una classificazione casuale delle immagini di ciascun test set (come visibile in classifica.py). Si richiede l'uso del software xampp per la gestione di un database MySQL.
***N.B.***: non modificare in alcun modo la directory Immagini ed il suo contenuto

ISTRUZIONI PER IL PRIMO UTILIZZO:

1) Creare su xampp un nuovo database MySQL di nome imagerecognize (tipicamente tramite phpMyAdmin) se non ne esiste già uno (in tal caso, accertarsi che non esista già anche una tabella di nome dbTable)
2) Importare il database di prova contenuto in imagerecognize.sql (contenuto in questa cartella) nel database appena creato
3) Inserire nella cartella ClustImm (contenuta nella directory precedente) le immagini contenute in ClustImmProva (ricordatevi di cancellarle dopo aver finito di provare!)
4) Lanciare lo script provaCrossVal.py

ISTRUZIONI PER GLI UTILIZZI SUCCESSIVI: è sufficiente lanciare lo script crossVal.py (con gli stessi valori di k suggeriti in precedenza) per generare altre classificazioni casuali. E' possibile anche verificare il corretto funzionamento della lettura del path di un'immagine da database tramite lo script provaGetImgPath.py