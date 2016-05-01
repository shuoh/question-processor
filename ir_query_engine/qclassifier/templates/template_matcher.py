import itertools
import heapq
import time
from ir_query_engine.qclassifier.templates.question_template import TemplateWordToken, TemplatePhraseStructureToken
from ir_query_engine.qclassifier.query_preprocessing.query_tokens import QueryWordToken, QueryPhraseLabelToken, \
    QueryPunctuationToken

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
        Find the top N matches from all the templates by comparing the matching score with the given query
        :param query_interps: all the possible interpretations of the input query,
                            represented by a list of QuerySyntaxInterpretation object
        :param num_matches: number of top matches
        :param metrics: metrics dict where the perf data will be collected
        :return: list((QuerySyntaxInterpretation, QuestionTemplate, match_score, phrase_match_mapping))
        """

        self._debug_print('Finding top %d matches from the %d templates...' % (num_matches, len(self._templates)))

        # start timer
        start_time = time.time()

        results = []
        for interp, template in itertools.product(query_interps, self._templates):
            match_score, phrase_match_mapping = self._calculate_match_score(
                template.template_tokenized, interp.interpreted_query_tokens)
            results.append(TemplateMatchResult(template, interp, match_score, phrase_match_mapping))

        top_matches = heapq.nlargest(num_matches, results, key=lambda x: x.match_score)

        if self._debug:
            for match in top_matches:
                print match

        # calculate time spent
        if metrics is not None:
            elapse = time.time() - start_time
            metrics[self.__class__.__name__] = elapse

        return top_matches

    @staticmethod
    def _calculate_match_score(template_tokens, query_tokens):
        """
        :param template_tokens: list of TemplateToken objects
        :param query_tokens: list of QueryToken objects
        :return: (match_score, template_phrase_token_to_query_phrase_token_mapping)
        """

        #  ------->  query (j)
        #  |
        #  |
        #  \/
        #  template (i)
        dp_matrix_h = len(template_tokens) + 1
        dp_matrix_w = len(query_tokens) + 1
        score_dp_matrix = [[0 for _ in range(dp_matrix_w)] for _ in range(dp_matrix_h)]
        backtrack_dp_matrix = [[None for _ in range(dp_matrix_w)] for _ in range(dp_matrix_h)]

        # Initialize base cases

        for i in range(1, dp_matrix_h):
            template_token = template_tokens[i - 1]
            if isinstance(template_token, TemplateWordToken):
                score_dp_matrix[i][0] = score_dp_matrix[i - 1][0] - INSERT_EXACT_WORD_TO_QUERY_PENALTY
            elif isinstance(template_token, TemplatePhraseStructureToken):
                score_dp_matrix[i][0] = score_dp_matrix[i - 1][0] - INSERT_PHRASE_TO_QUERY_PENALTY
            else:
                raise Exception('Unexpected token type')

        for j in range(1, dp_matrix_w):
            query_token = query_tokens[j - 1]
            if isinstance(query_token, QueryWordToken):
                score_dp_matrix[0][j] = score_dp_matrix[0][j - 1] - INSERT_EXACT_WORD_TO_TEMPLATE_PENALTY
            elif isinstance(query_token, QueryPhraseLabelToken):
                score_dp_matrix[0][j] = score_dp_matrix[0][j - 1] - INSERT_PHRASE_TO_TEMPLATE_PENALTY
            elif isinstance(query_token, QueryPunctuationToken):
                score_dp_matrix[0][j] = score_dp_matrix[0][j - 1] - INSERT_PUNCTUATION_TO_TEMPLATE_PENALTY
            else:
                raise Exception('Unexpected token type')

        # Inductive cases

        for i, j in itertools.product(range(1, dp_matrix_h), range(1, dp_matrix_w)):
            template_token = template_tokens[i - 1]
            query_token = query_tokens[j - 1]

            if template_token.match(query_token):
                if isinstance(template_token, TemplateWordToken):
                    score_dp_matrix[i][j] = score_dp_matrix[i - 1][j - 1] + EXACT_WORD_MATCH_REWARD
                else:
                    score_dp_matrix[i][j] = score_dp_matrix[i - 1][j - 1] + PHRASE_MATCH_REWARD
                backtrack_dp_matrix[i][j] = (i - 1, j - 1)

            else:
                # if choose to edit the query to match the template
                if isinstance(template_token, TemplateWordToken):
                    insert_query = score_dp_matrix[i - 1][j] - INSERT_EXACT_WORD_TO_QUERY_PENALTY
                else:
                    insert_query = score_dp_matrix[i - 1][j] - INSERT_PHRASE_TO_QUERY_PENALTY

                # or if choose to edit the template to match the query
                if isinstance(query_token, QueryWordToken):
                    insert_template = score_dp_matrix[i][j - 1] - INSERT_EXACT_WORD_TO_TEMPLATE_PENALTY
                elif isinstance(query_token, QueryPhraseLabelToken):
                    insert_template = score_dp_matrix[i][j - 1] - INSERT_PHRASE_TO_TEMPLATE_PENALTY
                else:
                    insert_template = score_dp_matrix[i][j - 1] - INSERT_PUNCTUATION_TO_TEMPLATE_PENALTY

                if insert_template > insert_query:
                    score_dp_matrix[i][j] = insert_template
                    backtrack_dp_matrix[i][j] = (i, j - 1)
                else:
                    score_dp_matrix[i][j] = insert_query
                    backtrack_dp_matrix[i][j] = (i - 1, j)

        best_score = score_dp_matrix[-1][-1]

        # construct phrase structure mapping from the backtrack table
        template_phrase_token_to_query_phrase_token_mapping = {}
        pos = (dp_matrix_h - 1, dp_matrix_w - 1)
        while True:
            prev_pos = backtrack_dp_matrix[pos[0]][pos[1]]
            if prev_pos is None:
                break
            template_idx = pos[0] - 1
            query_idx = pos[1] - 1
            if prev_pos[0] == pos[0] - 1 and prev_pos[1] == pos[1] - 1 \
                    and isinstance(template_tokens[template_idx], TemplatePhraseStructureToken):
                template_phrase_token_to_query_phrase_token_mapping[template_idx] = query_idx
            # keep the iteration going
            pos = prev_pos

        return best_score, template_phrase_token_to_query_phrase_token_mapping

    def _debug_print(self, output):
        if self._debug:
            print output


class TemplateMatchResult(object):
    """
    Attributes:
        template_phrase_token_to_query_parse_subtree_mapping: a list in the length same as the number of phrase tokens
        in the template, with each element being the matched parsing subtree of the query if the corresponding phrase
        token is matched in the query, None otherwise.
    """

    def __init__(self, template, query_interpretation, match_score, phrase_match_mapping):
        """
        :param template: a QuestionTemplate object
        :param query_interpretation: a QuerySyntaxInterpretation object
        :param match_score: the matching score between the template and the query interpretation
        :param phrase_match_mapping: index mapping from the phrase tokens in the template to those matched
                                     in the query interpretation
        """
        self.template = template
        self.query_interpretation = query_interpretation
        self.match_score = match_score
        self.phrase_match_mapping = phrase_match_mapping

        self.template_phrase_token_to_query_parse_subtree_mapping = \
            self._to_template_phrase_token_to_query_parse_subtree_mapping(phrase_match_mapping)

    def __repr__(self):
        return '%s, score: %.1f, matched_subtrees: %s' % (self.template, self.match_score,
                                                          self.template_phrase_token_to_query_parse_subtree_mapping)

    def _to_template_phrase_token_to_query_parse_subtree_mapping(self, phrase_match_mapping):

        # first reconstruct mapping from query token index to query interpretation replacement index
        replacement_cur_idx = -1
        replacement_idxes = [-1 for i in range(len(self.query_interpretation.interpreted_query_tokens))]
        for query_token_idx, query_token in enumerate(self.query_interpretation.interpreted_query_tokens):
            if isinstance(query_token, QueryPhraseLabelToken):
                replacement_cur_idx += 1
                replacement_idxes[query_token_idx] = replacement_cur_idx

        # now we are ready to construct the desired mapping
        matched_subtrees = []
        for template_token_idx, template_token in enumerate(self.template.template_tokenized):
            if isinstance(template_token, TemplatePhraseStructureToken):
                if template_token_idx in phrase_match_mapping:
                    matched_query_token_idx = phrase_match_mapping[template_token_idx]
                    replacement_idx = replacement_idxes[matched_query_token_idx]
                    replacement_data = self.query_interpretation.phrase_struct_replacements[replacement_idx]
                    # the parsed subtree is inside the replacement unit that was applied to the phrase token
                    matched_subtrees.append(replacement_data.subtree_to_replace)
                else:
                    matched_subtrees.append(None)

        return matched_subtrees
