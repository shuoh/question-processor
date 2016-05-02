from ir_query_engine.qclassifier.query_concept_extraction.head_word_finder import find_head_word_for_noun_phrase, \
    find_head_word_for_verb_phrase, find_head_word_for_adjective_phrase


class PhraseTokenConceptExtractor(object):

    def __init__(self, debug=False):
        self._debug = debug

    def extract_all_concepts(self, query_interpretation, whole_query_parse_result):

        word_dependency = whole_query_parse_result.word_dependency
        word_tokens = whole_query_parse_result.word_tokens

        concepts = []
        for phrase_token_idx, phrase_token_replacement in enumerate(query_interpretation.phrase_struct_replacements):
            phrase_parse_tree = phrase_token_replacement.subtree_to_replace
            phrase_offset = query_interpretation.phrase_token_offsets[phrase_token_idx]
            phrase_size = len(phrase_parse_tree.leaves())
            phrase_word_tokens = word_tokens[phrase_offset:phrase_offset+phrase_size]

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

            concepts.append(extractor(phrase_parse_tree, phrase_word_tokens, word_dependency))

        if self._debug:
            for i, concept in enumerate(concepts):
                print '%d --> %s' % (i, concept)

        return concepts

    def _extract_noun_phrase_concept(self, phrase_parse_tree, word_tokens, word_dependency):

        head_word, all_nouns = find_head_word_for_noun_phrase(word_tokens, word_dependency)

        entity_token = head_word
        attribute_token = None

        # some of relation types need to be treated differently
        for head_word_relation in word_dependency.lookup_dependencies_on(head_word.text):
            # for prep_of|poss relations, the dependent should be "promoted" as the entity
            if head_word_relation[0] == 'prep_of' or head_word_relation[0] == 'poss':
                poss_dependent = self._find_word_token(head_word_relation[2], all_nouns)
                if poss_dependent:
                    entity_token = poss_dependent
                    attribute_token = head_word
                    break

        # TODO: consider other types of relations?
        entity_modifiers = self._collect_modifiers(entity_token.text, word_dependency,
                                                   {'amod', 'poss', 'nn', 'conj_or', 'conj_and'})
        attribute_modifiers = self._collect_modifiers(attribute_token.text, word_dependency,
                                                      {'amod', 'nn', 'conj_or', 'conj_and'}) \
            if attribute_token else []

        concept = NounPhraseTokenConcept(entity=entity_token.lemma,
                                         entity_modifiers=entity_modifiers,
                                         attribute=attribute_token.lemma if attribute_token else None,
                                         attribute_modifiers=attribute_modifiers)
        # print '%s --> %s' % (' '.join(phrase_parse_tree.leaves()), concept)
        return concept

    def _extract_verb_phrase_concept(self, phrase_parse_tree, word_tokens, word_dependency):

        head_word, _ = find_head_word_for_verb_phrase(word_tokens, word_dependency)

        action_token = head_word
        object_token = None

        # find object through dobj relation
        for action_relation in word_dependency.lookup_dependencies_on(action_token.text):
            if action_relation[0] == 'dobj':
                object_token = self._find_word_token(action_relation[2], word_tokens)

        # "are damaged" --> (dep, are, damaged)
        action_modifiers = self._collect_modifiers(action_token.text, word_dependency,
                                                   {'advmod', 'xcomp', 'dep', 'neg',
                                                    'prep_in', 'prep_on', 'prep_during', 'prep_from',
                                                    'conj_or', 'conj_and'})
        object_modifiers = self._collect_modifiers(object_token.text, word_dependency,
                                                   {'amod', 'poss', 'nn', 'conj_or', 'conj_and'}) \
            if object_token else []

        concept = VerbPhraseTokenConcept(action=action_token.lemma,
                                         action_modifiers=action_modifiers,
                                         object=object_token.lemma if object_token else None,
                                         object_modifiers=object_modifiers)
        # print '%s --> %s' % (' '.join(phrase_parse_tree.leaves()), concept)
        return concept

    def _extract_adjective_phrase_concept(self, phrase_parse_tree, word_tokens, word_dependency):

        adjective_token, _ = find_head_word_for_adjective_phrase(word_tokens, word_dependency)
        adjective_modifiers = self._collect_modifiers(adjective_token.text, word_dependency,
                                                      {'neg',
                                                       'prep_in', 'prep_on', 'prep_during', 'prep_from',
                                                       'conj_or', 'conj_and'})

        concept = AdjectivePhraseTokenConcept(adjective=adjective_token.lemma,
                                              adjective_modifiers=adjective_modifiers)
        # print '%s --> %s' % (' '.join(phrase_parse_tree.leaves()), concept)
        return concept

    def _extract_prepositional_phrase_concept(self, phrase_parse_tree, word_tokens, word_dependency):
        # TODO: extract head word of the noun
        return PrepositionalPhraseTokenConcept(phrase=' '.join(phrase_parse_tree.leaves()))

    @staticmethod
    def _find_word_token(word_text, word_tags):
        for word in word_tags:
            if word.text == word_text:
                return word
        return None

    @staticmethod
    def _collect_modifiers(word_text, word_dependency, relation_type_filter=None):
        # TODO: change relation_type_filter to lambda to be more expressive
        modifiers = []
        for relation in word_dependency.lookup_dependencies_on(word_text):
            if relation_type_filter is None or relation[0] in relation_type_filter:
                modifiers.append((relation[0], relation[2]))
        return modifiers

    def _debug_print(self, output):
        if self._debug:
            print output


class PhraseTokenConcept(object):
    pass


class NounPhraseTokenConcept(PhraseTokenConcept):

    def __init__(self, entity, entity_modifiers, attribute, attribute_modifiers):
        """
        :param entity: str
        :param entity_modifiers: list((str, str))
        :param attribute: str
        :param attribute_modifiers: list((str, str))
        """
        self.entity = entity
        self.entity_modifiers = entity_modifiers
        self.attribute = attribute
        self.attribute_modifiers = attribute_modifiers

    def __repr__(self):
        return 'Entity: %s(%s), Attribute: %s(%s)' \
               % (self.entity, self.entity_modifiers, self.attribute, self.attribute_modifiers)


class VerbPhraseTokenConcept(PhraseTokenConcept):

    def __init__(self, action, action_modifiers, object, object_modifiers):
        """
        :param action: str
        :param action_modifiers: list((str, str))
        :param object: str
        :param object_modifiers: list((str, str))
        """
        self.action = action
        self.action_modifiers = action_modifiers
        self.object = object
        self.object_modifiers = object_modifiers

    def __repr__(self):
        return 'Action: %s(%s), Object: %s(%s)' \
               % (self.action, self.action_modifiers, self.object, self.object_modifiers)


class AdjectivePhraseTokenConcept(PhraseTokenConcept):

    def __init__(self, adjective, adjective_modifiers):
        self.adjective = adjective
        self.adjective_modifiers = adjective_modifiers

    def __repr__(self):
        return 'Adjective: %s(%s)' % (self.adjective, self.adjective_modifiers)


class PrepositionalPhraseTokenConcept(PhraseTokenConcept):

    def __init__(self, phrase):
        self.phrase = phrase

    def __repr__(self):
        return self.phrase
