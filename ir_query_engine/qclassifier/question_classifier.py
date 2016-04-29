from ir_query_engine.qclassifier.query_preprocessing.query_syntax_interpreter import *


class QuestionTypeClassifier(object):

    def __init__(self, debug=False):
        self._debug = debug

    def classify(self, question, metrics=None):
        """
        :param question: the un-normalized raw text of the question to be classified
        :param metrics: the dict where the performance of this method call will be collected
        :return: a QuestionType object, with all the parsed data inside
        """

        self._debug_print('Input: ' + question)

        self._debug_print('Expanding phrase structures...')
        syntax_interpreter = QuerySyntaxInterpreter(debug=self._debug)
        syntax_interpreter.generate_all_interpretation(question, metrics)

        return None

    def _debug_print(self, output):
        if self._debug:
            print output
