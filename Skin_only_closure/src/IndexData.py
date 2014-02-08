'''
Created on Aug 28, 2013

@author: VMR11
'''
import re

patient_ids_path = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\GIANT\\Open Skin\\DS_FollowUP\\FollowUpDSids.txt'
index_data_path = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\GIANT\\Open Skin\\DS_FollowUP\\open_abdomen_index_data.csv'
output_data_path = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\GIANT\\Open Skin\\DS_FollowUP\\output_index_data.csv'

with open(patient_ids_path,'r') as ids_file:
    patient_ids = ids_file.readlines()
    patient_ids = list(set([id.strip() for id in patient_ids if id != '']))
    
with open(index_data_path,'r') as data_file:
    index_data = data_file.readlines()
    column_headers = re.split(r',',index_data.pop(0))
    index_data = [re.split(r',',line) for line in index_data]
    
with open(output_data_path,'w') as output_file:
    for id in patient_ids:
        for patient in index_data:
            if patient[0] == id:
                output = ','.join(patient)
                print>>output_file, output.strip()
        