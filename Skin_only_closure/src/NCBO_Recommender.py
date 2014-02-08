'''
Created on Jul 26, 2013

@author: VMR11
'''
import urllib #@UnresolvedImport
import urllib2 #@UnresolvedImport

#API key, login to BioPortal (http://www.bioontology.org) and go to Account to see your API key 
API_KEY= '24e050ca-54e0-11e0-9d7b-005056aa3316'

# Base URL for service
recommender_URL = 'http://rest.bioontology.org/recommender' 

# Text to Annotate 
textToAnnotate = "skin only"

# Structure containing parameters
params = {
          'format':'simpleText',
          'ontologyId':'',  #Output formats (one of): xml, tabDelimited, text  
          'apikey':API_KEY,
          'text':textToAnnotate,
}
 
# Submit job
submitUrl = recommender_URL + '/submit/example@your_email.com'
postData = urllib.urlencode(params)
fh = urllib2.urlopen(submitUrl, postData)
annotatorResults = fh.read()
fh.close()
# Print job identifier
print annotatorResults,6