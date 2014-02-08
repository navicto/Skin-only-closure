'''
Created on Jul 9, 2013

@author: VMR11
'''

import os, collections
inPath = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Analysis Run\\READ codes\\Focused text\\Concepts Found - Positives\\'
outPath = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Concepts Analysis\\Positives\\'
#inPath = 'C:\\Users\\vmr11\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Concepts Found - Negatives\\'
#outPath = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Concepts Analysis\\Negatives\\'

fileList = os.listdir(inPath) #directory where the annotations from the ncbo annotator are saved

'''
Here, a set is created with all the concepts found across annotated reports. Also, a list is generated,
which keep multiple appearances of each concept.
'''
concepts_raw = []
concepts = set()
for fileName in fileList:
    conceptsList = open(inPath + fileName).readlines()
    conceptsList = [concept.strip() for concept in conceptsList if concept != '']
    conceptsList = list(set(conceptsList))
    concepts_raw += conceptsList
    for concept in conceptsList:
        concepts = concepts.union(set([concept]))

'''
Here, the frequency of each concept is determined
'''
conceptsFreq = dict([(concept,0) for concept in concepts])
for concept in concepts:
    conceptsFreq[concept] = float(concepts_raw.count(concept))/len(fileList)
conceptsFreq = collections.OrderedDict(sorted(conceptsFreq.items(), key = lambda x: x[1], reverse = True))    
    

outFile = open(outPath + 'conceptFrequency.txt' , 'w')

for concept in conceptsFreq.items():
    print>>outFile, concept
    