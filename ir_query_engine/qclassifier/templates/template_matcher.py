import itertools
import heapq
import time
from ir_query_engine.qclassifier.templates.question_templates import WordToken, PhraseStructureToken

INSERT_QUERY_EXACT_WORD_PENALTY = 2
INSERT_QUERY_PHRASE_PENALTY = 1
INSERT_TEMPLATE_EXACT_WORD_PENALTY = 1
INSERT_TEMPLATE_PHRASE_PENALTY = 0.5


class TemplateMatcher(object):

    def __init__(self, templates, debug=False):
        """
        :param templates: list(QuestionTemplate)
        """
        self._templates = templates
        self._debug = debug

    def get_best_N_matches(self, query_interps, num_matches, metrics=None):
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
            edit_dist = self._calculate_weighted_edit_dist(interp.interpreted_query_tokens, template.template_tokenized)
            results.append((interp, template, edit_dist))

        top_matches = heapq.nsmallest(num_matches, results, key=lambda x: x[2])

        if self._debug:
            for match in top_matches:
                print '%s  <-->  %s, dist: %.1f' % (match[0].interpreted_query, match[1], match[2])

        # calculate time spent
        if metrics is not None:
            elapse = time.clock() - start_time
            metrics[self.__class__.__name__] = elapse

        return top_matches

    @staticmethod
    def _calculate_weighted_edit_dist(query_tokens, template_tokens):

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
            if isinstance(template_token, WordToken):
                dp_matrix[i][0] = dp_matrix[i - 1][0] + INSERT_QUERY_EXACT_WORD_PENALTY
            elif isinstance(template_token, PhraseStructureToken):
                dp_matrix[i][0] = dp_matrix[i - 1][0] + INSERT_QUERY_PHRASE_PENALTY
            else:
                raise Exception('Unexpected token type')

        for j in range(1, dp_matrix_w):
            query_token = query_tokens[j - 1]
            if isinstance(query_token, WordToken):
                dp_matrix[0][j] = dp_matrix[0][j - 1] + INSERT_TEMPLATE_EXACT_WORD_PENALTY
            elif isinstance(query_token, PhraseStructureToken):
                dp_matrix[0][j] = dp_matrix[0][j - 1] + INSERT_TEMPLATE_PHRASE_PENALTY
            else:
                raise Exception('Unexpected token type')

        # Inductive cases

        for i, j in itertools.product(range(1, dp_matrix_h), range(1, dp_matrix_w)):
            template_token = template_tokens[i - 1]
            query_token = query_tokens[j - 1]

            if template_token == query_token:
                dp_matrix[i][j] = dp_matrix[i - 1][j - 1]

            else:
                # if choose to edit the query to match the template
                if isinstance(template_token, WordToken):
                    insert_query = dp_matrix[i - 1][j] + INSERT_QUERY_EXACT_WORD_PENALTY
                else:
                    insert_query = dp_matrix[i - 1][j] + INSERT_QUERY_PHRASE_PENALTY

                # or if choose to edit the template to match the query
                if isinstance(query_token, WordToken):
                    insert_template = dp_matrix[i][j - 1] + INSERT_TEMPLATE_EXACT_WORD_PENALTY
                else:
                    insert_template = dp_matrix[i][j - 1] + INSERT_TEMPLATE_PHRASE_PENALTY

                dp_matrix[i][j] = min(insert_query, insert_template)

        return dp_matrix[-1][-1]

    def _debug_print(self, output):
        if self._debug:
            print output
