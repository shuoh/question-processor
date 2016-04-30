import itertools
import heapq
import time
from ir_query_engine.qclassifier.templates.question_template import TemplateWordToken, TemplatePhraseStructureToken
from ir_query_engine.qclassifier.query_preprocessing.query_tokens import QueryWordToken, QueryPhraseLabelToken, QueryPunctuationToken

EXACT_WORD_MATCH_REWARD = 4
PHRASE_MATCH_REWARD = 2
INSERT_EXACT_WORD_TO_QUERY_PENALTY = 2
INSERT_PHRASE_TO_QUERY_PENALTY = 2
INSERT_EXACT_WORD_TO_TEMPLATE_PENALTY = 1
INSERT_PHRASE_TO_TEMPLATE_PENALTY = 1
INSERT_PUNCTUATION_TO_TEMPLATE_PENALTY = 0


class TemplateMatcher(object):

    def __init__(self, templates, debug=False):
        """
        :param templates: list(QuestionTemplate)
        """
        self._templates = templates
        self._debug = debug

    def get_best_n_matches(self, query_interps, num_matches, metrics=None):
        """
        Find the top N matches from all the templates by comparing the edit distance with the given query
        :param query_interps: all the possible interpretations of the input query,
                            represented by a list of QuerySyntaxInterpretation object
        :param num_matches: number of top matches
        :param metrics: metrics dict where the perf data will be collected
        :return: list((QuerySyntaxInterpretation, QuestionTemplate, edit_dist))
        """

        self._debug_print('Finding top %d matches from the %d templates...' % (num_matches, len(self._templates)))

        # start timer
        start_time = time.clock()

        results = []
        for interp, template in itertools.product(query_interps, self._templates):
            match_score = self._calculate_match_score(interp.interpreted_query_tokens, template.template_tokenized)
            results.append((interp, template, match_score))

        top_matches = heapq.nlargest(num_matches, results, key=lambda x: x[2])

        if self._debug:
            for match in top_matches:
                print '%s  <-->  %s, score: %.1f' % (match[0].interpreted_query, match[1], match[2])

        # calculate time spent
        if metrics is not None:
            elapse = time.clock() - start_time
            metrics[self.__class__.__name__] = elapse

        return top_matches

    @staticmethod
    def _calculate_match_score(query_tokens, template_tokens):

        #  ------->  query (j)
        #  |
        #  |
        #  \/
        #  template (i)
        dp_matrix_h = len(template_tokens) + 1
        dp_matrix_w = len(query_tokens) + 1
        dp_matrix = [[0 for j in range(dp_matrix_w)] for i in range(dp_matrix_h)]

        # Initialize base cases

        for i in range(1, dp_matrix_h):
            template_token = template_tokens[i - 1]
            if isinstance(template_token, TemplateWordToken):
                dp_matrix[i][0] = dp_matrix[i - 1][0] - INSERT_EXACT_WORD_TO_QUERY_PENALTY
            elif isinstance(template_token, TemplatePhraseStructureToken):
                dp_matrix[i][0] = dp_matrix[i - 1][0] - INSERT_PHRASE_TO_QUERY_PENALTY
            else:
                raise Exception('Unexpected token type')

        for j in range(1, dp_matrix_w):
            query_token = query_tokens[j - 1]
            if isinstance(query_token, QueryWordToken):
                dp_matrix[0][j] = dp_matrix[0][j - 1] - INSERT_EXACT_WORD_TO_TEMPLATE_PENALTY
            elif isinstance(query_token, QueryPhraseLabelToken):
                dp_matrix[0][j] = dp_matrix[0][j - 1] - INSERT_PHRASE_TO_TEMPLATE_PENALTY
            elif isinstance(query_token, QueryPunctuationToken):
                dp_matrix[0][j] = dp_matrix[0][j - 1] - INSERT_PUNCTUATION_TO_TEMPLATE_PENALTY
            else:
                raise Exception('Unexpected token type')

        # Inductive cases

        for i, j in itertools.product(range(1, dp_matrix_h), range(1, dp_matrix_w)):
            template_token = template_tokens[i - 1]
            query_token = query_tokens[j - 1]

            if template_token.match(query_token):
                if isinstance(template_token, TemplateWordToken):
                    dp_matrix[i][j] = dp_matrix[i - 1][j - 1] + EXACT_WORD_MATCH_REWARD
                else:
                    dp_matrix[i][j] = dp_matrix[i - 1][j - 1] + PHRASE_MATCH_REWARD

            else:
                # if choose to edit the query to match the template
                if isinstance(template_token, TemplateWordToken):
                    insert_query = dp_matrix[i - 1][j] - INSERT_EXACT_WORD_TO_QUERY_PENALTY
                else:
                    insert_query = dp_matrix[i - 1][j] - INSERT_PHRASE_TO_QUERY_PENALTY

                # or if choose to edit the template to match the query
                if isinstance(query_token, QueryWordToken):
                    insert_template = dp_matrix[i][j - 1] - INSERT_EXACT_WORD_TO_TEMPLATE_PENALTY
                elif isinstance(query_token, QueryPhraseLabelToken):
                    insert_template = dp_matrix[i][j - 1] - INSERT_PHRASE_TO_TEMPLATE_PENALTY
                else:
                    insert_template = dp_matrix[i][j - 1] - INSERT_PUNCTUATION_TO_TEMPLATE_PENALTY

                dp_matrix[i][j] = max(insert_query, insert_template)

        return dp_matrix[-1][-1]

    def _debug_print(self, output):
        if self._debug:
            print output
