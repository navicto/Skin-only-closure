'''
Created on Jul 31, 2013

@author: VMR11
'''
import re, collections
def concept_frequency(input_path):
    frequency_file = open(input_path,'r')
    frequencies = {}
    for line in frequency_file:
        concept_match = re.search(r"'([\w\s-]+)'\s*,\s+(\d+\.*\d+)",line)
        try:
            frequencies[concept_match.group(1)] = map(float,[concept_match.group(2)])[0]
        except:
            print "couldn't process ",line
    return frequencies

def likelihood_ratios(positives_frequencies, negatives_frequencies):
    lr = {}
    smoothing_num = 0
    smoothing_den = 0.1
    for concept in positives_frequencies.keys():
        numerator = positives_frequencies[concept]
        try:
            denominator = negatives_frequencies[concept]
        except KeyError:
            denominator = 0
        lr[concept] = (smoothing_num+numerator)/(smoothing_den+denominator)
    return collections.OrderedDict(sorted(lr.items(), key = lambda x: x[1], reverse = True))        
        

def main():
    positives_path = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Analysis Run\\READ codes\\Whole text\\Concepts Analysis\\Positives\\conceptFrequency.txt'
    negatives_path = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\2. Spring 2013\\Project course\\Analysis Run\\READ codes\\Whole text\\Concepts Analysis\\Negatives\\conceptFrequency.txt'
    output_path = 'C:\\Users\\vmr11\\Desktop\\'
    positives_frequencies = concept_frequency(positives_path)
    negatives_frequencies = concept_frequency(negatives_path)
    lr = likelihood_ratios(positives_frequencies, negatives_frequencies)
    output_file = open(output_path+'LR.txt','w')
    for pair in lr.items():
        print>>output_file, str(pair[0])+'\t'+str(pair[1])

if __name__ == '__main__':
    main()