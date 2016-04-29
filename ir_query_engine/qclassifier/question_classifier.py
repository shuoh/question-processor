from ir_query_engine.qclassifier.query_preprocessing.query_syntax_interpreter import QuerySyntaxInterpreter
from ir_query_engine.qclassifier.templates.template_matcher import TemplateMatcher
from ir_query_engine.qclassifier.templates.data.predefined_templates import PREDEFINED_TEMPLATES

NUM_TOP_CANDIDATES = 5


class QuestionTypeClassifier(object):

    def __init__(self, debug=False):
        self._debug = debug

        # initialize each sub components
        self._syntax_interpreter = QuerySyntaxInterpreter(debug=debug)
        self._template_matcher = TemplateMatcher(PREDEFINED_TEMPLATES, debug=debug)

    def classify(self, question, metrics=None):
        """
        :param question: the un-normalized raw text of the question to be classified
        :param metrics: the dict where the performance of this method call will be collected
        :return: a QuestionType object, with all the parsed data inside
        """

        self._debug_print('Input: ' + question)

        # generate interpretations
        syntax_interpretations = self._syntax_interpreter.generate_all_interpretation(question, metrics)

        # find best matched templates
        top_matches = self._template_matcher.get_best_N_matches(syntax_interpretations, NUM_TOP_CANDIDATES, metrics)

        # TODO: extract entity data

        return None

    def _debug_print(self, output):
        if self._debug:
            print output
