'''
Created on Jul 11, 2013

@author: VMR11
'''
from django.core.management import setup_environ 
import settings
setup_environ(settings)
from annoCentral2.models import Answer
import itertools

annotators = [52,53]
valid_questions = [251,252,253,254,257,258,259,282,283]
target_questions = [253,257,259]

def get_annotated_reportIDs(answers, valid_questions = []):
    '''
    Gets the reportIDs for a set of answers, discarding any report in answers to questions different from valid_questions 
    '''
    annotated_reports = []
    if valid_questions: discarded_reports = []
    for ans in answers:
        annotated_reports += [ans.report]
        if valid_questions and ans.question_id not in valid_questions:
            discarded_reports += [ans.report]
    discarded_reports = set(discarded_reports)
    if valid_questions:
        return list(set(annotated_reports) - discarded_reports)
    else:
        return list(set(annotated_reports))

def determine_patient_status(answers):
    '''
    Classifies a patient into: ignored, truePositive, trueNegative
    '''
    try:
        ignored = answers.filter(question = 259)[0].stringAnswer
        definitive_closure = answers.filter(question = 259)[0].stringAnswer
        fascial_closure = answers.filter(question = 259)[0].stringAnswer
    except: pass
    if ignored == 'True': 
        return 'Ignored'
    elif definitive_closure == 'Yes' and fascial_closure == ' No - skin only closure':
        return 'Positive'
    else:
        return 'Negative'

'''
Now, I'll find which reports have been annotated by both annotators in annotators
'''
answers_firstAnnotator = Answer.objects.filter(annotator = annotators[0])
annotated_reports_firstAnnotator = get_annotated_reportIDs(answers_firstAnnotator, valid_questions)
answers_sharedReports = Answer.objects.filter(report__in = annotated_reports_firstAnnotator, annotator = annotators[1])
annotated_reports = get_annotated_reportIDs(answers_sharedReports, valid_questions)
answers = Answer.objects.filter(report__in = annotated_reports, annotator__in = annotators, question__in = target_questions)

'''
Find frequency for combinations of patient classification
'''
outcomeCombinations = itertools.product(['Ignored','Positive','Negative'], repeat = 2)
contingencyTable = dict([(combo,0) for combo in outcomeCombinations])
for rep in annotated_reports:
    classification_1st_annotator = determine_patient_status(answers.filter(report = rep, annotator = annotators[0]))
    classification_2nd_annotator = determine_patient_status(answers.filter(report = rep, annotator = annotators[1]))
    contingencyTable[(classification_1st_annotator,classification_2nd_annotator)] += 1


print '\tI\tP\tN'
print 'I\t%s\t%s\t%s' %(contingencyTable[('Ignored','Ignored')], contingencyTable[('Ignored','Positive')], contingencyTable[('Ignored','Negative')])
print 'P\t%s\t%s\t%s' %(contingencyTable[('Positive','Ignored')], contingencyTable[('Positive','Positive')], contingencyTable[('Positive','Negative')])
print 'N\t%s\t%s\t%s' %(contingencyTable[('Negative','Ignored')], contingencyTable[('Negative','Positive')], contingencyTable[('Negative','Negative')])

print len(annotated_reports)

