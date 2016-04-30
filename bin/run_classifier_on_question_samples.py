import os
from ir_query_engine.qclassifier.question_classifier import QuestionTypeClassifier

classifier = QuestionTypeClassifier(debug=True)
metrics = {}
classifier.classify('My phone is not working', metrics)

# classifier.classify('can I get my order expedited?', metrics)
# classifier.classify("I don't have the middle support of my bed", metrics)

print
print '**********************:'
print '*     PERFORMANCE    *'
print '**********************'
print metrics

# classifier = QuestionTypeClassifier(debug=False)
#
# with open(os.path.join(os.path.dirname(__file__), 'data/all_questions.txt'), 'r') as question_file:
#     for line in question_file.readlines():
#         if line.isspace() or line.startswith('#'):
#             continue
#
#         question_text = line.strip()
#
#         print
#         print '========================'
#         result = classifier.classify(question_text)
#         print 'Input: ' + question_text
#         print 'Best match: %s  <-->  %s, score: %.1f' % (result[0][0].interpreted_query, result[0][1], result[0][2])
