'''
Created on 30/03/2013

@author: Victor
'''
import re
import os

inPath = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Answers\\'
fileNames=os.listdir(inPath)

outDir = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\True Positives\\Text for Annotation\\'
positiveDir = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\True Positives\\'
negativeDir = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\True Negatives\\'
positiveReports = open(positiveDir+'positiveReports.txt','w')
negativeReports = open(negativeDir+'negativeReports.txt','w')
fileIndex=1
tpReports = {}

for fileName in fileNames:
    tpReports[fileName] = []
    print fileName
    truePositives=[]
    filePath=inPath+fileName
    answers=open(filePath,'r').read()
    answersList=re.split(r'EOA', answers)
    answersList=[answer.strip() for answer in answersList]

    i=0
    for answer in answersList[0:-1]:
        fields=re.split(r' *\| *', answer)
        if fields[-2] == 'Ignore report' and fields[-1] == 'True':
            i += 1
            continue
        if fields[-2] == 'Was the fascia closed?' and fields[-1] == 'No - skin only closure':
            truePositives+=[i+1]
            match = re.search(r'reportID: *(\d+)',fields[0])
            reportID = match.groups(1)
            tpReports[fileName] +=map(int,reportID)
#            print fields[-1],' ',fields[-2],' ',fields[0]
            print >> positiveReports, str(reportID[0])
        elif fields[-2] == 'Was the fascia closed?' and fields[-1] != 'No data' and fields[-1] != '':
            match = re.search(r'reportID: *(\d+)',fields[0])
            reportID = match.groups(1)
            print >> negativeReports, str(reportID[0])
        i+=1
        
    for tp in truePositives:
        strIndex=str(fileIndex)
        nZeros=3-len(strIndex)
        outPath=outDir+'0'*nZeros+strIndex+'.txt'
        outFile=open(outPath,'w')
        answer=answersList[tp]
        fields=re.split(r' *\| *', answer)
        print>>outFile, fields[-1]
        fileIndex+=1

outFile.close()
positiveReports.close()
negativeReports.close()
        
        
        
        









    
