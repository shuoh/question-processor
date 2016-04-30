import os
from ir_query_engine.qclassifier.question_classifier import QuestionTypeClassifier

classifier = QuestionTypeClassifier(debug=True)

metrics = {}
# classifier.classify('how can I get my order expedited?')
classifier.classify('my phone is not working', metrics)

print
print '**********************:'
print '*     PERFORMANCE    *'
print '**********************'
print metrics

# with open(os.path.join(os.path.dirname(__file__), 'data/questions.txt'), 'r') as question_file:
#     for line in question_file.readlines():
#         if line.isspace() or line.startswith('#'):
#             continue
#
#         question_text = line.strip()
#
#         print
#         print '========================'
#         result = classifier.classify(question_text)
