import os
import time
from ir_query_engine.qclassifier.question_classifier import QuestionClassifier

# classifier = QuestionClassifier(debug=True)
# metrics = {}
# classifier.classify("Do you offer 1-hour delivery to my address?", metrics)
#
# # classifier.classify('can I get my order expedited?', metrics)
# # classifier.classify("I don't have the middle support of my bed", metrics)
#
# print
# print '**********************:'
# print '*     PERFORMANCE    *'
# print '**********************'
# print metrics

classifier = QuestionClassifier(debug=False)

with open(os.path.join(os.path.dirname(__file__), 'data/all_questions.txt'), 'r') as question_file:
    for line in question_file.readlines():
        if line.isspace() or line.startswith('#'):
            continue

        question_text = line.strip()

        print
        print '========================'
        metrics = {}
        start_time = time.time()
        result = classifier.classify(question_text, metrics)
        print 'Input: ' + question_text
        print 'Best match: %s' % result[0].template_match_result
        print 'KB query: %s' % result[0].kb_query
        print 'Time spent: %f' % (time.time() - start_time)
        print 'Performance: %s' % metrics
