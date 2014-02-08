'''
Created on Jul 11, 2013

@author: VMR11
'''
from django.core.management import setup_environ 
import settings
setup_environ(settings)
from annoCentral2.models import *
import re
    
def getAnnotatorAnswers(key,outPath):
    outFile=open(outPath,'w')
    answers=Answer.objects.filter(annotator=key)
    print key
    for answer in answers:
        print>>outFile, 'reportID:',str(answer.report_id),' | ',answer,'\n','EOA'   

def getAnnotatorsKeys(outPath):
    outFile=open(outPath,'w')
    users=User.objects.all()
    userIDs=[]
    ID=1
    for user in users:
        annotator=str(users.filter(id=ID))
        if annotator!='[]':
            userName=re.search(r'<User:\s*(\w+@*\w*\.*\w*)>',annotator)
            userName=userName.group(1)
            userIDs+=[str(ID)+' '+userName]
        ID+=1
    for user in userIDs:
        print>>outFile, user
        

def main():
    #get annotator IDs
    outPath='C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\AnnotatorAgreement\\AnnotatorIDs.txt'
    getAnnotatorsKeys(outPath)
    
    #List of annotators for this project:
    projectAnnotators=[52,53,57,58,59,60,61,62]
    
    
    for ID in projectAnnotators:
        user=str(User.objects.filter(id=ID))
        userName=re.search(r'<User:\s*(\w+@*\w*\.*\w*)>',user).group(1)
        outPath='C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Answers\\'+str(ID)+userName+'.txt'
        getAnnotatorAnswers(ID,outPath)
        
    

if __name__=='__main__':
    main()

print 5