import sys
sys.path.insert(0, "./Scripts")
import funzioniCaricamento as fc
import funzioniSalvataggio as fs
import funzioniDB as fdb
import random

totIter = fc.getNumIter()

if totIter>0:

    # FOR EVERY FOLD OF THE CROSS-VALIDATION PROCESS

    for i in range(0,totIter):
        classes = fc.getClasses()
        testSet = fc.getTestSet(i)
        rankingList = []
        for ID in testSet:
            ranking = [ID, [[classes[random.randint(0,len(classes)-1)], random.random()]]]
            rankingList.append(ranking)

        fs.saveRanking(i, rankingList)
        
            
