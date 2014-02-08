'''
Created on Aug 5, 2013

@author: VMR11
'''

from django.core.management import setup_environ 
import settings
setup_environ(settings)
from annoCentral2.models import *
from pt_reports.models import *
import re

def get_project_patients(project_id):
    query_set = Patient.objects.filter(anno_project = project_id)
    patient_set = set()
    for patient in query_set:
        patient_set = patient_set.union([str(patient.patientID)])
    return patient_set

def patients_from_file(file_path):
    in_file = open(file_path, 'r')
    patient_set = set()
    for line in in_file:
        patient_match = re.search(r'(S\d+)\s+PUH\s+S\d+', line)
        patient = patient_match.group(1)
        patient_set = patient_set.union([patient])
    return patient_set

def model_fields(model_instance):
    class_fields = model_instance._meta.fields
    for column in class_fields:
        print column.name

def patients_from_question(project_id, question_id, answer_values):
    answers = Answer.objects.filter(project=project_id, question=question_id, stringAnswer__in=answer_values)
    patients = set([])
    reports = set([])
    for answer in answers:
        report_id = answer.report.id
        reports = reports.union([report_id])
        patient = Report.objects.filter(id=report_id).get().ptID
        patients = patients.union([patient])
    return (patients, reports)
        
        

def main():
    patientset_path = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\GIANT\\Open Skin\\Original set\\original set.txt'
#    patientset_path = 'C:\\Users\\vmr11\\Dropbox\\DBMI\\GIANT\\Open Skin\\Original set\\included_only.txt'
    file_patients = patients_from_file(patientset_path)
    db_patients = get_project_patients(23)
    print 'from file: ',len(file_patients)
    print 'from db: ', len(db_patients)
    print 5

if __name__ == '__main__':
    main()