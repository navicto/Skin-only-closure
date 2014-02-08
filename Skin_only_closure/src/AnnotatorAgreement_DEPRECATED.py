#line including for testing
#response to test
#gotcha
#ok, we are ready
#:-)
'''
Created on 30/03/2013

@author: Victor
'''
import re


inPath='/Users/Victor/Dropbox/DBMI/2. Spring 2013/Project course/AnnotatorAgreement/'
inPath = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\AnnotatorAgreement\\'
fileNames=['GabesAnswers.txt','MohamadsAnswers.txt']

annotators_answers={}
ignoredReports={}
annotatedReports={}
for fileName in fileNames:
    reportsList=set()
    ignoredReportsList=[]
    filePath=inPath+fileName
    answers=open(filePath,'r').read()
    answersList=re.split(r'EOA', answers)
    answersList=[answer.strip() for answer in answersList]
    
    for answer in answersList[0:-1]:
        fields=re.split(r' *\| *', answer)
        if fields[0] not in annotators_answers.keys(): #fields[0] is the annotator
            annotators_answers[fields[0]]={}
        (reportID,patientID)=re.split(r',',fields[2])
        if fields[-2]=='Ignore report' and fields[-1]=='True':
            ignoredReportsList+=[reportID]
        reportsList=reportsList.union([reportID])
        if reportID not in ignoredReportsList:
            if patientID not in annotators_answers[fields[0]].keys():
                annotators_answers[fields[0]][patientID]=[(reportID,fields[-2],fields[-1])]
            else:
                annotators_answers[fields[0]][patientID]+=[(reportID,fields[-2],fields[-1])]
    annotatedReports[fields[0]]=sorted(list(reportsList),key=lambda x: map(int,x)[0])
    ignoredReports[fields[0]]=sorted(ignoredReportsList,key=lambda x: map(int,x)[0])
    
    for annotator in annotators_answers.keys():
        for patient in annotators_answers[annotator].keys():
            annotators_answers[annotator][patient].sort(key=lambda x: map(int,x[0])[0])

ignoredQuestions=['Copy and paste the text that supports conclusion of VAC','Copy and paste the text that supports conclusion of Closure','Comments']
annotators=annotators_answers.keys()
annotatedPatients=sorted(list(set(annotators_answers[annotators[0]].keys()).union(set(annotators_answers[annotators[1]].keys()))))
disagreements=[]
for patient in annotatedPatients:
    if patient in annotators_answers[annotators[0]].keys() and patient in annotators_answers[annotators[1]].keys():
        for triplet0 in annotators_answers[annotators[0]][patient]:
            for triplet1 in annotators_answers[annotators[1]][patient]:
                if triplet0[0]==triplet1[0] and triplet0[1]==triplet1[1] and triplet0[2]!=triplet1[2] and triplet0[1] not in ignoredQuestions:
                    disagreements+=[(triplet0[0],triplet0[1])]
#            if triplet[0] in annotatedReports[annotators[0]] and triplet[0] in annotatedReports[annotators[1]]:

print disagreements     
        
            
 








    
