N.B.: la versione attuale non è ancora completamente funzionante poiché le funzionalità relative alla lettura del dataset dal database non sono ancora state provate con il database definitivo. Il materiale è distribuito in anticipo per permettere di capire in anticipo il funzionamento degli script ed iniziare a completare classifica.py con il proprio modello.

N.B.2: è possibile ripulire il database delle immagini dai doppioni della stessa classe con lo script eliminaDoppioni.py, incluso a parte a causa del lungo tempo di esecuzione.

La cross-validazione k-fold è un metodo di validazione per modelli; essa consiste nella creazione di k training set e test set disgiunti e calcola l'accuratezza del modello mediando i risultati ottenuti nei k casi.
L'algoritmo è implementato dallo script crossVal.py, che esegue in sequenza partizionaDataset.py, classifica.py ed analizzaRisultati.py; mentre il primo ed il terzo sono completi e non vanno modificati, il secondo va completato inserendo il modello da validare, in modo da addestrarlo e testarlo con ciascuna combinazione di training set e test set. Per raggiungere questo scopo, bisogna avvalersi in tale script delle funzioni incluse in funzioniCaricamento.py e funzioniSalvataggio.py; uno stub da completare è già incluso in classifica.py . Al termine del processo di cross-validazione i risultati sono presentati nel file Results.txt . In seguito viene presentato in maggior dettaglio il funzionamento degli script partizionaDataset.py, classifica.py ed analizzaRisultati.py, con particolare attenzione ai requisiti da rispettare sul formato dei dati.

 ----------------------------------------------
|             partizionaDataset.py             |
 ----------------------------------------------

Dopo aver eliminato eventuali immagini duplicate dal database, lo script richiede all'utente il numero k di fold (numero di iterazioni, e quindi di training set e test set) con cui avviare la cross-validazione e colloca nella directory ./Temp/ i k file contenenti ciascun training set ed i k file contenenti ciascun test set, oltre ad un file di configurazione.

***Nota importante***: la scelta di k è cruciale per un buon riuscimento del processo di validazione. Poiché ciascun test set conterrà |D|/k istanze, dove |D| è il numero di istanze contenute nel dataset, tale rapporto deve essere sufficientemente grande. Si consiglia quindi prima di effettuare la validazione di inserire nel database un numero sufficientemente elevato di immagini, e quindi scegliere k di conseguenza.

 ----------------------------------------------
|                 classifica.py                |
 ----------------------------------------------

Questo script è principalmente scritto dall'utente sfruttando gli script funzioniCaricamento.py e funzioniSalvataggio.py; il primo contiene funzioni per leggere da file il numero k di iterazioni inserito in precedenza, una lista con tutte le classi contenute nel dataset (probabilmente non necessaria, ma forse utile) ed il training set ed il test set da utilizzare all'iterazione passata come parametro, mentre il secondo include solo una funzione per salvare la lista dei ranking calcolati per ogni immagine del test set ad una data iterazione in appositi file contenuti nella directory ./Temp/. Esempi di utilizzo di queste funzioni sono inclusi nello stub dello script classifica.py .

***Nota importante***: ciascun training set, test set e ranking utilizza una struttura definita a priori e specificata nello stub dello script classifica.py .

 ----------------------------------------------
|             analizzaRisultati.py             |
 ----------------------------------------------

Lo script legge da file le liste di ranking salvate, calcola la matrice di confusione e l'accuratezza ad ogni iterazione (reperendo dal database delle immagini le classificazioni corrette) e l'accuratezza complessiva e scrive questi risultati nel file Results.txt, contenuto nella stessa directory degli script. Viene inoltre eliminata la directory ./Temp/ contenente tutti i file temporanei usati in precedenza.


--------------------------------------------------------------------------------------------------------------------------


APPENDICE: COME LEGGERE UNA MATRICE DI CONFUSIONE E CALCOLARE L'ACCURATEZZA

La matrice di confusione, prodotta nel nostro caso ad ogni iterazione della cross-validazione, contiene informazioni sul numero di elementi attribuiti alle diverse classi (da leggere lungo le colonne) e sulla loro corretta classificazione (da leggere lungo le righe); l'accuratezza è quindi calcolata come somma del numero di istanze classificate correttamente per cento diviso per il numero di istanze totali. Di seguito sono riportati due esempi per chiarire ulteriormente la lettura di una matrice di confusione ed il calcolo dell'accuratezza:

 ------------------------------------------
|                 Esempio 1                |
 ------------------------------------------

       0   1

   0   7   5
   1   6   9

Questa matrice indica che:
- 7 elementi appartenenti alla classe 0 sono stati attribuiti alla classe 0 (classificazione corretta)
- 5 elementi appartenenti alla classe 0 sono stati attribuiti alla classe 1 (classificazione errata)
- 6 elementi appartenenti alla classe 1 sono stati attribuiti alla classe 0 (classificazione errata)
- 9 elementi appartenenti alla classe 1 sono stati attribuiti alla classe 1 (classificazione corretta)

L'accuratezza in questo caso sarà quindi pari a (7+9)*100/(7+5+6+9), ossia al 59.26%

 ------------------------------------------
|                 Esempio 2                |
 ------------------------------------------

       0   1   2

   0   3   1   0
   1   5   2   3
   2   2   2   4

Questa matrice indica che:
- 3 elementi appartenenti alla classe 0 sono stati attribuiti alla classe 0 (classificazione corretta)
- 1 elemento appartenente alla classe 0 è stato attribuito alla classe 1 (classificazione errata)
- nessun elemento appartenente alla classe 0 è stato attribuito alla classe 2 (classificazione errata)
- 5 elementi appartenenti alla classe 1 sono stati attribuiti alla classe 0 (classificazione errata)
- 2 elementi appartenenti alla classe 1 sono stati attribuiti alla classe 1 (classificazione corretta)
- 3 elementi appartenenti alla classe 1 sono stati attribuiti alla classe 2 (classificazione errata)
- 2 elementi appartenenti alla classe 2 sono stati attribuiti alla classe 0 (classificazione errata)
- 2 elementi appartenenti alla classe 2 sono stati attribuiti alla classe 1 (classificazione errata)
- 4 elementi appartenenti alla classe 2 sono stati attribuiti alla classe 2 (classificazione corretta)

L'accuratezza in questo caso sarà quindi pari a (3+2+4)*100/(3+1+0+5+2+3+2+2+4), ossia al 40.9%