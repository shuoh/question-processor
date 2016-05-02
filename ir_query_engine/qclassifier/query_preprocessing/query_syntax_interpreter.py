import re
import itertools
import time
from ir_query_engine.qclassifier.utils.tree_traverser import TreebankNodeVisitor, dfs_traverse_tree
from ir_query_engine.qclassifier.query_preprocessing.query_tokens import tokenize_interpreted_query, \
    QueryPhraseLabelToken


class QuerySyntaxInterpreter(object):

    def __init__(self, replaceable_phrase_labels={'NP', 'VP', 'ADJP', 'PP'}, debug=False):
        """
        :param replaceable_phrase_labels: by default includes noun-phrase, verb-phrase, adjective-phrase,
                                        prepositional-phrase
        :param debug: True to enable debug output
        :return:
        """
        self._replaceable_phrase_labels = replaceable_phrase_labels
        self._debug = debug

    def generate_all_interpretation(self, query_parse_result, metrics=None):
        """
        :param query_parse_result: a SentenceParseResult object
        :param metrics: the dict where the performance of this method call will be collected
        :return: list(QuerySyntaxInterpretation)
        """

        self._debug_print('Generating possible interpretations of the query...')

        # start timer
        start_time = time.time()

        normalized_sentence = query_parse_result.normalized_sentence
        parsed_tree = query_parse_result.parsed_tree

        self._debug_print('Normalized form: ' + normalized_sentence)

        if self._debug:
            parsed_tree.pretty_print()

        self._debug_print('All possible interpretations:')

        collector = PhraseStructureReplacementCollector(self._replaceable_phrase_labels)
        # collect possible interpretations while DFS traversing the parse tree
        dfs_traverse_tree(parsed_tree, collector)
        # gather the result
        interpretations = collector.get_collected_interpretations_for_subtree(parsed_tree)
        # apply to the original input
        for interp in interpretations:
            interp.apply_to(normalized_sentence)
            self._debug_print('- ' + interp.interpreted_query)

        # calculate time spent
        if metrics is not None:
            elapse = time.time() - start_time
            metrics[self.__class__.__name__] = elapse

        return interpretations

    def _debug_print(self, output):
        if self._debug:
            print output


class QuerySyntaxInterpretation(object):
    """
    Attributes:
        phrase_struct_replacements: all the phrase structure replacements that this interpretation is based upon,
                                    ordered by the position of their appearance in the original query
        interpreted_query: str (only available after apply_to is called)
        interpreted_query_tokens: list(QueryToken), (only available after apply_to is called)
        phrase_token_offsets: offset of each of the phrase tokens in the original tokenized query. list(int),
                              (only available after apply_to is called)
    """

    def __init__(self, phrase_struct_replacements):
        """
        :param phrase_struct_replacements: list(PhraseStructureReplacement)
        """
        self.phrase_struct_replacements = phrase_struct_replacements
        self.interpreted_query = None
        self.interpreted_query_tokens = None
        self.phrase_token_offsets = None

    def __repr__(self):
        return str(self.phrase_struct_replacements)

    def apply_to(self, normalized_sentence):
        """
        Note that this method will set the interpreted_query and interpreted_query_tokens attributes
        :param normalized_sentence: the query input in normalized form
        """
        replaced = normalized_sentence
        for replacement in self.phrase_struct_replacements:
            replaced = replacement.apply_to(replaced)

        self.interpreted_query = replaced
        self.interpreted_query_tokens = tokenize_interpreted_query(replaced)
        self.phrase_token_offsets = self._calculate_phrase_token_offsets(self.interpreted_query_tokens)

    def _calculate_phrase_token_offsets(self, interpreted_tokens):
        offsets = [-1 for _ in self.phrase_struct_replacements]
        replacement_idx = 0
        uninterpreted_token_idx = 0
        for token in interpreted_tokens:
            if isinstance(token, QueryPhraseLabelToken):
                offsets[replacement_idx] = uninterpreted_token_idx
                phrase_replacement = self.phrase_struct_replacements[replacement_idx]
                uninterpreted_token_idx += len(phrase_replacement.subtree_to_replace.leaves())
                replacement_idx += 1
            else:
                uninterpreted_token_idx += 1
        if not replacement_idx == len(offsets):
            raise Exception("Unexcepted condition - found some of the phrase token's offset is not found")
        return offsets

    @staticmethod
    def product(interp_list0, interp_list1):
        """
        :param interp_list0: list(QuerySyntaxInterpretation)
        :param interp_list1: list(QuerySyntaxInterpretation)
        :return: a new list of syntax interpretations, with each of the interpretation combining
        the phrase structure replacements from one of the first input list and one of the second list
        """
        product = []
        for interp_0, interp_1 in itertools.product(interp_list0, interp_list1):
            combined_replacements = interp_0.phrase_struct_replacements + interp_1.phrase_struct_replacements
            product.append(QuerySyntaxInterpretation(combined_replacements))
        return product


class PhraseStructureReplacement(object):
    """
    Attributes:
        text: the phrase text that appears in the original query
        phrase_label: the replacement label for the given phrase text
        subtree_to_replace: the treebank node for the given phrase text
    """

    def __init__(self, subtree_to_replace):
        self.text = ' '.join(subtree_to_replace.leaves())
        self.phrase_label = subtree_to_replace.label()
        self.subtree_to_replace = subtree_to_replace

    def __repr__(self):
        return '%s -> [%s]' % (self.text, self.phrase_label)

    def apply_to(self, normalized_sentence):
        old_text = self.text
        new_text = '[' + self.phrase_label + ']'

        # we need to make sure the replaced text is not a substring of another word
        # lookbehind -> not non-whitespace character
        # NOTE: that we can't simply use /s since we also want to capture ^
        regex = '(?<!\S)' + re.escape(old_text) + '(?!\S)'
        return re.sub(regex, new_text, normalized_sentence)


class PhraseStructureReplacementCollector(TreebankNodeVisitor):
    """
    Attributes:
        subtree_interpretations_map:
            all the interpretation result on the previously visited nodes are stored in this dict.
                key: the object id of a previously visited tree node
                val: all the possible syntax interpretations applied to any of the subtrees of the given node
    """

    def __init__(self, replaceable_phrase_labels):
        self._replaceable_phrase_labels = replaceable_phrase_labels

        # see attribute doc string
        self.subtree_interpretations_map = {}

    def visit(self, tree_node):

        interpretations = []

        for child in tree_node:
            # it's possible that the child node was not previously visited, if it's not a tree node
            if id(child) not in self.subtree_interpretations_map:
                continue
            child_interps = self.get_collected_interpretations_for_subtree(child)
            # cross product with the previous children
            interpretations.extend(QuerySyntaxInterpretation.product(interpretations, child_interps))
            # then add the interpretations for the child node itself
            interpretations.extend(child_interps)

        # at last, add replacement for the current node if it's replaceable
        if tree_node.label() in self._replaceable_phrase_labels:
            replacement = PhraseStructureReplacement(tree_node)
            interpretations.append(QuerySyntaxInterpretation([replacement]))

        # add the interpretation results to the map
        self._set_interpretations_for_subtree(tree_node, interpretations)

    def get_collected_interpretations_for_subtree(self, subtree):
        return self.subtree_interpretations_map[id(subtree)]

    def _set_interpretations_for_subtree(self, subtree, interpretations):
        self.subtree_interpretations_map[id(subtree)] = interpretations
