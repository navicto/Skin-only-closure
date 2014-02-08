'''
Created on Jul 18, 2013

@author: VMR11

Purpose of this script is to quantify how quick new concepts are found in reports. In other words,
how many reports you need to achieve certain % of concept discovery
'''
import os, collections

def get_concepts_list(concepts_directory):
    '''
    Parses a file set containing concepts found in operative reports, and returns a list of all
    the concepts found, with unique appearance, as well as a list of the same concepts, including
    their repetitions
    '''
    fileList = os.listdir(concepts_directory)
    concepts_raw = []
    concepts = set()
    for fileName in fileList:
        conceptsList = open(concepts_directory + fileName).readlines()
        conceptsList = [concept.strip() for concept in conceptsList if concept != '']
        conceptsList = list(set(conceptsList))
        concepts_raw += conceptsList
        for concept in conceptsList:
            concepts = concepts.union(set([concept]))
    return (concepts, concepts_raw, len(fileList))

def single_report_concepts(concepts_path):
    conceptsList = open(concepts_path).readlines()
    conceptsList = [concept.strip() for concept in conceptsList if concept != '']
    return list(set(conceptsList))

def concepts_frequency(concepts, concepts_raw, n_reports):
    conceptsFreq = dict([(concept,0) for concept in concepts])
    for concept in concepts:
        conceptsFreq[concept] = float(concepts_raw.count(concept))/n_reports
    conceptsFreq = collections.OrderedDict(sorted(conceptsFreq.items(), key = lambda x: x[1], reverse = True))
    return conceptsFreq
    
def concept_discovery_rate(concepts_directory, concepts_freq, minimum_freq, out_path):
    file_list = os.listdir(concepts_directory)
    target_concepts = [concept for concept in concepts_freq.items() if concept[1] > minimum_freq]
    target_concepts = sorted(target_concepts, key = lambda x: x[1], reverse = True)
    target_concepts = [concept[0] for concept in target_concepts]
    n_concepts = len(target_concepts)
    discovery_count = 0
    discovery_progression = []
    for file_name in file_list:
        file_concepts = single_report_concepts(concepts_directory + file_name)
        for concept in file_concepts:
            if concept in target_concepts:
                discovery_count += 1
                target_concepts.remove(concept)
        discovery_progression += [float(discovery_count) / n_concepts]
        if not target_concepts:
            break
    out_file = open(out_path, 'w')
    print >> out_file, discovery_progression 
    return discovery_progression
    
def main():
#    concepts_directory = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Concepts Found - Negatives\\'
    concepts_directory = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Analysis Run\\READ codes\\Whole text\\Concepts Found - Positives\\'
    concepts,concepts_raw,n_reports = get_concepts_list(concepts_directory)
    concepts_freq = concepts_frequency(concepts, concepts_raw, n_reports)
    out_path = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Concepts Analysis\\Discovery Rate\\discoverRate.txt'
    discovery_progression = concept_discovery_rate(concepts_directory, concepts_freq, 0.05, out_path)
    print discovery_progression

if __name__ == '__main__':
    main()