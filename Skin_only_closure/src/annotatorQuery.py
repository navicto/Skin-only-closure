'''
Created on 18/06/2013

@author: Victor
'''

import os, re, urllib2, urllib

API_KEY= '24e050ca-54e0-11e0-9d7b-005056aa3316'
annotatorUrl = 'http://rest.bioontology.org/obs/annotator' 

outputDirectory = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Concepts Found - Positives\\'
inPath = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\True Positives\\'

outputDirectory = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Concepts Found - Negatives\\'
inPath = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\True Negatives\\'

TPFiles=os.listdir(inPath)
for fileName in TPFiles:
    
    if fileName[0] == '.': continue
    try:
        textToAnnotate = open(inPath + fileName,'r').read()
    except:
        print 'file ',fileName,' could not be read'
    
    params = {
              'longestOnly':'false',
              'wholeWordOnly':'true',
              'withContext':'true',
              'filterNumber':'false', 
              'stopWords':"",
              'withDefaultStopWords':'true', 
              'isStopWordsCaseSenstive':'false', 
              'minTermSize':'3', 
              'scored':'true',  
              'withSynonyms':'true', 
              'ontologiesToExpand':'',   
              'ontologiesToKeepInResult':'1427',   
              'isVirtualOntologyId':'true', 
              'semanticTypes':'',  #T017,T047,T191&" #T999&"
              'levelMax':'0',
              'mappingTypes':'null', 
              'textToAnnotate':textToAnnotate, 
              'format':'tabDelimited',  #Output formats (one of): xml, tabDelimited, text  
              'apikey':API_KEY,
              }
    
    try:
        submitUrl = annotatorUrl + '/submit/example@your_email.com'
        postData = urllib.urlencode(params)
        fh = urllib2.urlopen(submitUrl, postData)
        annotations = fh.readlines()
    except:
        print fileName
        continue
    
    if fileName == '126.txt':
        xxxxx = 5
    
    outputFile = open(outputDirectory + fileName,'w')
    for concept in annotations:
        conceptID = concept
        try:
            conceptID = re.split(r'\t', concept)[2]
        except:
            pass
        print >> outputFile, conceptID
    
