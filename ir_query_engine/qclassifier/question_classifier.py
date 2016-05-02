from ir_query_engine.qclassifier.query_preprocessing.query_syntax_interpreter import QuerySyntaxInterpreter
from ir_query_engine.qclassifier.query_preprocessing.sentence_parser import SentenceParser
from ir_query_engine.qclassifier.templates.template_matcher import TemplateMatcher
from ir_query_engine.qclassifier.templates.data.predefined_templates import PREDEFINED_TEMPLATES
from ir_query_engine.qclassifier.query_concept_extraction.phrase_token_concept_extractor import \
    PhraseTokenConceptExtractor

NUM_TOP_CANDIDATES = 5


class QuestionClassifier(object):
    """
    The entry point for classifying an incoming question and converting it into knowledge base query language
    """

    def __init__(self, debug=False):
        self._debug = debug

        # initialize each sub components
        self._sentence_parser = SentenceParser()
        self._syntax_interpreter = QuerySyntaxInterpreter(debug=debug)
        self._template_matcher = TemplateMatcher(PREDEFINED_TEMPLATES, debug=debug)
        self._token_concept_extractor = PhraseTokenConceptExtractor(debug=debug)

    def classify(self, question, metrics=None):
        """
        :param question: the un-normalized raw text of the question to be classified
        :param metrics: the dict where the performance of this method call will be collected
        :return: list of QuestionClassificationResult objects, ordered by their match score
        """

        self._debug_print('Input: ' + question)

        # syntax parsing
        parse_result = self._sentence_parser.parse(question)

        # generate interpretations
        syntax_interpretations = self._syntax_interpreter.generate_all_interpretation(parse_result, metrics)

        # find best matched templates
        top_matches = self._template_matcher.get_best_n_matches(syntax_interpretations, NUM_TOP_CANDIDATES, metrics)

        results = []
        for match in top_matches:
            matched_template = match.template

            # extract concepts of all the phrase tokens in the interpretation
            concepts = self._token_concept_extractor.extract_all_concepts(match, parse_result)
            # generate kb query through the template
            kb_query = matched_template.to_knowledge_base_query(concepts)

            # TODO: syntax type
            results.append(QuestionClassificationResult(QuestionSyntaxTypes.WH_QUESTION, match, kb_query))

        return results

    def _debug_print(self, output):
        if self._debug:
            print output


class QuestionClassificationResult(object):
    """
    Attributes:
        question_syntax_type: see all the possible values in the QuestionSyntaxTypes class
        template_match_result: a TemplateMatchResult object
        kb_query: a KnowledgeBaseQuery object
    """

    def __init__(self, question_syntax_type, template_match_result, kb_query):
        self.question_syntax_type = question_syntax_type
        self.template_match_result = template_match_result
        self.kb_query = kb_query


class QuestionSyntaxTypes(object):
    WH_QUESTION = 'wh_question'
    YES_NO_QUESTION = 'yes_no_question'
    OTHER = 'other'
