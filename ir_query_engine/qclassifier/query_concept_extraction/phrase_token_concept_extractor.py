from ir_query_engine.qclassifier.query_concept_extraction.head_word_finder import find_head_word_for_noun_phrase


class PhraseTokenConceptExtractor(object):

    def __init__(self, debug=False):
        self._debug = debug

    def extract_all_concepts(self, query_interpretation, whole_query_parse_result):
        word_dependency = whole_query_parse_result.word_dependency
        word_token_tags = whole_query_parse_result.word_tokens

        concepts = []
        for phrase_token_idx, phrase_token_replacement in enumerate(query_interpretation.phrase_struct_replacements):
            phrase_parse_tree = phrase_token_replacement.subtree_to_replace
            phrase_offset = query_interpretation.phrase_token_offsets[phrase_token_idx]
            phrase_size = len(phrase_parse_tree.leaves())
            phrase_word_tags = word_token_tags[phrase_offset:phrase_offset+phrase_size]

            if phrase_token_replacement.phrase_label == 'NP':
                extractor = self._extract_noun_phrase_concept
            elif phrase_token_replacement.phrase_label == 'VP':
                extractor = self._extract_verb_phrase_concept
            elif phrase_token_replacement.phrase_label == 'ADJP':
                extractor = self._extract_adjective_phrase_concept
            elif phrase_token_replacement.phrase_label == 'PP':
                extractor = self._extract_prepositional_phrase_concept
            else:
                raise Exception('Unknown phrase label: ' + phrase_token_replacement.phrase_label)

            concepts.append(extractor(phrase_parse_tree, phrase_word_tags, word_dependency))

        return concepts

    def _extract_noun_phrase_concept(self, phrase_parse_tree, word_tags, word_dependency):
        head_word = find_head_word_for_noun_phrase(word_tags, word_dependency)

    def _extract_verb_phrase_concept(self, phrase_parse_tree, word_tags, word_dependency):
        pass

    def _extract_adjective_phrase_concept(self, phrase_parse_tree, word_tags, word_dependency):
        pass

    def _extract_prepositional_phrase_concept(self, phrase_parse_tree, word_tags, word_dependency):
        pass

    def _debug_print(self, output):
        if self._debug:
            print output


class PhraseTokenConcept(object):
    pass


class NounPhraseTokenConcept(PhraseTokenConcept):

    def __init__(self, entity, attribute, modifiers):
        """
        :param entity:
        :param attribute:
        :param modifiers:
        :return:
        """
        self.entity = entity
        self.attribute = attribute
        self.modifiers = modifiers


class VerbPhraseTokenConcept(PhraseTokenConcept):
    pass


class AdjectivePhraseTokenConcept(PhraseTokenConcept):
    pass


class PrepositionalPhraseTokenConcept(PhraseTokenConcept):
    pass