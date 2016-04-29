import re

VALID_TEMPLATE_REGEX = '^[a-zA-Z0-9 \[\]]+$'


class QuestionTemplate(object):

    def __init__(self, template_str):
        self._check_valid_template(template_str)
        self.template_str = template_str
        self.template_tokenized = tokenize_templated_string(template_str)

    def __repr__(self):
        return self.template_str

    @staticmethod
    def _check_valid_template(template_str):
        if not re.match(VALID_TEMPLATE_REGEX, template_str):
            raise Exception('Invalid template: ' + template_str)


def tokenize_templated_string(templated_string):
    """
    :param templated_string: the template string to be tokenized
    :return: list containing either WordToken (whose word is lower-cased)
    or PhraseStructureToken (whose phrase label is unwrapped and upper-cased)
    """
    tokens = []
    for token in templated_string.split(' '):
        if token.startswith('[') and token.endswith(']'):
            tokens.append(PhraseStructureToken(token[1:-1].upper()))
        elif token:
            tokens.append(WordToken(token.lower()))
    return tokens


class WordToken(object):

    def __init__(self, word):
        self.word = word

    def __eq__(self, other):
        if isinstance(other, WordToken):
            return other.word == self.word
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class PhraseStructureToken(object):

    def __init__(self, phrase_label):
        self.phrase_label = phrase_label

    def __eq__(self, other):
        if isinstance(other, PhraseStructureToken):
            return other.phrase_label == self.phrase_label
        return False

    def __ne__(self, other):
        return not self.__eq__(other)




