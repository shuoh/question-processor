class PhraseTokenConceptExtractor(object):

    def __init__(self, debug=False):
        self._debug = debug

    def extract_all_concepts(self, query_interpretation, whole_query_parse_result):
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