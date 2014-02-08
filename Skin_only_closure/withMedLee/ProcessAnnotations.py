'''
Created on 25/11/2013

@author: Victor
'''
import os
import re
import csv
import collections

def get_file_annotations(csv_path, column_name):
    '''
    returns a set with all UMLS_codes present in a csv-formatted MedLee output
    '''
    with open(csv_path, 'r') as csv_file:
        csv_values = csv.DictReader(csv_file)
#        return set([re.split(r'_', row[column_name])[0] for row in csv_values])
        return set([row[column_name] for row in csv_values])

def get_dataset_annotations(data_path):
    annotations = {}
    for file_name in os.listdir(data_path):
        if os.path.splitext(file_name)[1] == '.csv':
            report_id = re.split(r'\.', file_name)[0]
            annotations[report_id] = get_file_annotations(data_path + file_name, 'UMLS_code')
    return annotations

def get_unique_codes(annotations):
    codes = set([])
    for concepts in annotations.values():
        codes = codes.union(concepts)
    return codes

def code_frequencies(annotations):
    codes = get_unique_codes(annotations)
    code_freq = dict([(code, 0) for code in codes])
    for concepts in annotations.values():
        for c in concepts:
            code_freq[c] += 1
    return code_freq

def likelihood(freq_p, n_p, freq_n, n_n, a, b):
    p_pos = (float(freq_p) + a) / (n_p + b)
    p_neg = (float(freq_n) + a) / (n_n + b)
    return (p_pos / p_neg)

def likelihood_ratios(positives_path, negatives_path, smooth_a, smooth_b, min_freq = 1):
    LR = {}
    annotations_pos = get_dataset_annotations(positives_path)
    annotations_neg = get_dataset_annotations(negatives_path)
    pos_freq = code_frequencies(annotations_pos)
    pos_freq = dict([pair for pair in pos_freq.items() if pair[1] >= min_freq])
    neg_freq = code_frequencies(annotations_neg)
    neg_freq = dict([pair for pair in neg_freq.items() if pair[1] >= min_freq])
    codes = set.union(get_unique_codes(annotations_pos), get_unique_codes(annotations_neg))
    n_p, n_n = (len(pos_freq), len(neg_freq))
    for c in codes:
        LR[c] = likelihood(pos_freq.get(c, 0), n_p, neg_freq.get(c, 0), n_n, smooth_a, smooth_b)
    return LR

def LR_filter(ordered_LR, threshold):
    return collections.OrderedDict(sorted([ c for c in ordered_LR.items() if c[1] > threshold], key=lambda x:x[1], reverse = True))

def code_discovery(annotations, codes):
    codes = set(codes)
    n = len(codes)
    progression = []
    values = annotations.itervalues()
    while codes:
        codes = codes - set(values.next())
        progression += [-1*(len(codes) - n)]
    return progression
        
def main():
    data_path = "/Users/Victor/Dropbox/DBMI/2. Spring 2013/Project course/MedLee Annotations/CSV files/"
    positives_path = data_path + 'Positives/'
    negatives_path = data_path + 'Negatives/'
    annotations_pos = get_dataset_annotations(positives_path)
    code_freq = code_frequencies(annotations_pos)

    smooth_a, smooth_b = (1,2)
    min_frequency = 5
    LR = likelihood_ratios(positives_path, negatives_path, smooth_a, smooth_b, min_freq = min_frequency)
    ordered_LR = collections.OrderedDict(sorted(LR.items(), key=lambda x:x[1], reverse = True))
#    print ordered_LR
#    for code, LR in ordered_LR.items():
#        if LR > 1:
#            print code, LR
#        else:
#            break
#    print len(LR_filter(ordered_LR, 2))
    
#    for c in LR_filter(ordered_LR, 0):
    for c in ordered_LR:
        print c, LR[c]

    progression = code_discovery(annotations_pos, LR_filter(ordered_LR, 3).keys())
    print progression
    
    return

if __name__ == "__main__":
    main()