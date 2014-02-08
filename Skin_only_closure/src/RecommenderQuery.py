'''
Created on 18/06/2013

@author: Victor
'''

import os, re, urllib2, urllib

API_KEY= '24e050ca-54e0-11e0-9d7b-005056aa3316'
recommenderUrl = 'http://rest.bioontology.org/recommender' 

outputDirectory = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Recommended Ontologies\\Positives\\'
inPath = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\True Positives\\Text for Annotation\\'

#outputDirectory = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Recommended Ontologies\\Negatives\\'
#inPath = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\True Negatives\\'

TPFiles=os.listdir(inPath)
recommendation_aggregate = []

def get_score(recommendation):
    match = re.search(r'\d+\s+(.+)\s+(\d+)', recommendation, re.DOTALL)
    ontology = match.group(1)
    score = map(float, map(int, [float(match.group(2))]))[0]
    return (ontology, score)

document_count = 0
ontology_scores = {}
for fileName in TPFiles:
    print document_count
    if fileName[0] == '.': continue
    try:
        textToAnnotate = open(inPath + fileName,'r').read()
        document_count += 1
    except:
        print 'file ',fileName,' could not be read'
        continue
    
    params = {
              'format':'simpleText',
              'ontologyId':'',  #Output formats (one of): xml, tabDelimited, text  
              'apikey':API_KEY,
              'text':textToAnnotate,
              'normalized':True,
              'output':'normalized-score',
              }
    
    try:
        submitUrl = recommenderUrl + '/submit/example@your_email.com'
        postData = urllib.urlencode(params)
        fh = urllib2.urlopen(submitUrl, postData)
        recommendations = fh.readlines()
    except:
        print fileName
        document_count -= 1
        continue
    
    for recommendation in recommendations:
        ontology, score = get_score(recommendation)
        if ontology in ontology_scores:
            ontology_scores[ontology] += score
        else:
            ontology_scores[ontology] = score

ontology_scores_avg = [(ontology, score/float(document_count)) for (ontology, score) in ontology_scores.items()]
ontology_scores_avg = sorted(ontology_scores_avg, key=lambda x: x[1], reverse = True)

outputFile = open(outputDirectory + 'scored_ontologies.txt','w')
with open(outputDirectory + 'scored_ontologies.txt','w') as output_file:
    for ontology in ontology_scores_avg:
        print>>output_file, ontology
    
