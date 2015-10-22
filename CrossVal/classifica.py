import sys
sys.path.insert(0, "./Scripts")
import funzioniCaricamento as fc
import funzioniSalvataggio as fs
import funzioniDB as fdb

totIter = fc.getNumIter()

if totIter>0:

    # FOR EVERY FOLD OF THE CROSS-VALIDATION PROCESS

    for i in range(0,totIter):
        
        # TRAINING
        # The training set has the following structure:
        #   [[groupClass, [IDs]], ...]
        # Example:
        #   [["ClassA", [4, 8, 24]], ["ClassB", [15, 29, 1]], ...]
        
        trainingSet = fc.getTrainingSet(i)
        for group in trainingSet:
            groupClass = group[0] # class of the images in this group
            for ID in group[1]:
                imgPath = fdb.getPath(ID)
                # retrieve the image using imgPath and use it to train the model,
                # knowing that its class is groupClass

        #TESTING
        # The test set has the following structure:
        #   [IDs]
        # Example:
        #   [5, 15, 21, ...]
        
        testSet = fc.getTestSet(i)
        rankingList = []
        for ID in testSet:
            imgPath = fdb.getImgPath(ID)
            ranking = # image classification, see the next comment
            rankingList.append(ranking)
            
            # retrieve the image using imgPath and classify it. The classification
            # process must produce a ranking having the following structure:
            #   [ID, [[Class, percentage], [...], ...]]
            # The ranking can contain the classification results over multiple classes
            # with the respective confidence percentages, in decreasing order; only
            # the leftmost class in the ranking (the one whose confidence percentage
            # is the highest) will be considered, though. Each percentage is a decimal
            # number between 0 and 1
            # Example:
            #   [5, [["ClassB", 0.65], ["ClassC", 0.20], ["ClassA", 0.15]]]
            # but the following would work, too:
            #   [5, [["ClassB", 0.65]]]

        fs.saveRanking(i, rankingList)
    
            
