'''
Created on Jun 25, 2013

@author: VMR11
'''

from django.core.management import setup_environ 
import settings
setup_environ(settings)
from annoCentral2.models import *

positiveReports = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\True Positives\\'
negativeReports = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\True Negatives\\'

def fetch_reports(directory, fileName):
    rawList = open(directory+fileName,'r').readlines()
    reportList = map(int,rawList)
    for reportID in reportList:
        reportCopy = Report.objects.filter(id=reportID).get()
        outFile = open(directory+str(reportID)+'.txt','w')
        print>>outFile, reportCopy.text


fetch_reports(positiveReports,'positiveReports.txt')
fetch_reports(negativeReports,'negativeReports.txt')
 
        
    
    
