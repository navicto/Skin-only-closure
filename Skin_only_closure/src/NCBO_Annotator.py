import urllib #@UnresolvedImport
import urllib2 #@UnresolvedImport


'''
Created on Aug 3, 2010
Updated on Apr 26, 2011

@author: Trish Whetzel
@contact: support@bioontology.org 
@note: See the Annotator User Guide for the full list of parameters: http://www.bioontology.org/wiki/index.php/Annotator_User_Guide
@note: Please subscribe to the bioportal-announce mailing list (https://mailman.stanford.edu/mailman/listinfo/bioportal-announce) to stay informed of any changes to the Annotator Web service 
'''
#API key, login to BioPortal (http://www.bioontology.org) and go to Account to see your API key 
API_KEY= '24e050ca-54e0-11e0-9d7b-005056aa3316'

# Base URL for service
annotatorUrl = 'http://rest.bioontology.org/obs/annotator' 
#annotatorUrl = 'http://bioportal.bioontology.org/annotator'

# Text to Annotate 
textToAnnotate = "skin only"

# Structure containing parameters
params = {
          'longestOnly':'false',
          'wholeWordOnly':'true',
          'withContext':'true',
          'filterNumber':'true', 
          'stopWords':"breast , cancer",
          'withDefaultStopWords':'true', 
          'isStopWordsCaseSenstive':'false', 
          'minTermSize':'3', 
          'scored':'true',  
          'withSynonyms':'true', 
          'ontologiesToExpand':'',   
          'ontologiesToKeepInResult':'1353',   
          'isVirtualOntologyId':'true', 
          'semanticTypes':'',  #T017,T047,T191&" #T999&"
          'levelMax':'0',
          'mappingTypes':'null', 
          'textToAnnotate':textToAnnotate, 
          'format':'tabDelimited',  #Output formats (one of): xml, tabDelimited, text  
          'apikey':API_KEY,
}
 
# Submit job
submitUrl = annotatorUrl + '/submit/example@your_email.com'
postData = urllib.urlencode(params)
fh = urllib2.urlopen(submitUrl, postData)
annotatorResults = fh.read()
fh.close()
# Print job identifier
print annotatorResults

