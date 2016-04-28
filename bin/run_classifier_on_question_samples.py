import os
from qclassifier.question_classifier import QuestionTypeClassifier

classifier = QuestionTypeClassifier()

with open(os.path.join(os.path.dirname(__file__), 'data/questions.txt'), 'r') as question_file:
    for line in question_file.readlines():
        if line.isspace() or line.startswith('#'):
            continue

        question_text = line.strip()
        result = classifier.classify(question_text)
        print question_text
        print result
