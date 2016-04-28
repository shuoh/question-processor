from qclassifier.question_types import *


class QuestionTypeClassifier(object):

    def classify(self, question):
        """
        :param question: the un-normalized raw text of the question to be classified
        :return: a QuestionType object, with all the parsed data inside
        """
        return None