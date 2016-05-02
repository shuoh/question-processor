import re
from ir_query_engine.qclassifier.query_preprocessing.query_tokens import *

VALID_CHAR_REGEX = '[^\W_]'  # \w except underscore
VALID_SINGLE_WORD_REGEX = VALID_CHAR_REGEX+'+'  # abc
VALID_MULTI_WORD_REGEX = '\('+'('+VALID_SINGLE_WORD_REGEX+'\|)*'+VALID_SINGLE_WORD_REGEX+'\)'  # (abc|123)
VALID_PHRASE_LABEL_REGEX = '\['+'([A-Z]+\|)*'+'[A-Z]+'+'\]'  # [NP|VP]
VALID_TOKEN_REGEX = '('+VALID_SINGLE_WORD_REGEX+')|('+VALID_MULTI_WORD_REGEX+')|('+VALID_PHRASE_LABEL_REGEX+')'
VALID_TEMPLATE_REGEX = '(('+VALID_TOKEN_REGEX+') )*('+VALID_TOKEN_REGEX+')'


class QuestionTemplate(object):

    def __init__(self, template_str):
        self._check_valid_template(template_str)
        self.template_str = template_str
        self.template_tokenized = self._tokenize_template_string(template_str)

    def __repr__(self):
        return self.template_str

    def to_knowledge_base_query(self, extracted_concepts):
        """
        :param extracted_concepts: a list of PhraseTokenConcept objects
        """
        return None

    @staticmethod
    def _check_valid_template(template_str):
        if not re.match('^'+VALID_TEMPLATE_REGEX+'$', template_str):
            raise Exception('Invalid template: ' + template_str)

    @staticmethod
    def _tokenize_template_string(template_string):
        """
        :param template_string: the template string to be tokenized
        :return: list containing either TemplateWordToken (whose word(s) is lower-cased)
        or PhraseStructureToken (whose phrase label(s) is unwrapped and upper-cased)
        """
        tokens = []
        for token in template_string.split(' '):
            if re.match('^'+VALID_SINGLE_WORD_REGEX+'$', token):
                tokens.append(TemplateWordToken(_lower_all([token])))
            elif re.match('^'+VALID_MULTI_WORD_REGEX+'$', token):
                tokens.append(TemplateWordToken(_lower_all(token[1:-1].split('|'))))
            elif re.match('^'+VALID_PHRASE_LABEL_REGEX+'$', token):
                tokens.append(TemplatePhraseStructureToken(_upper_all(token[1:-1].split('|'))))
            else:
                raise Exception('Unexpected token %s in the question template' % token)
        return tokens


def _upper_all(str_list):
    return [e.upper() for e in str_list]


def _lower_all(str_list):
    return [e.lower() for e in str_list]


class TemplateToken(object):

    def match(self, query_token):
        """
        :param query_token: a QueryToken object
        :return: True if this template token matches with the query token
        """
        raise NotImplementedError()


class TemplateWordToken(TemplateToken):
    """
    Either single or multi word token
    """

    def __init__(self, words):
        """
        :param words: list(str)
        """
        self.words = words

    def match(self, query_token):
        if not isinstance(query_token, QueryToken):
            raise NotImplementedError('I only know how to match with a QueryToken')
        if isinstance(query_token, QueryWordToken):
            return query_token.word in self.words
        else:
            return False


class TemplatePhraseStructureToken(TemplateToken):
    """
    Either single or multi phrase token
    """

    def __init__(self, phrase_labels):
        """
        :param phrase_labels: list(str)
        """
        self.phrase_labels = phrase_labels

    def match(self, query_token):
        if not isinstance(query_token, QueryToken):
            raise NotImplementedError('I only know how to match with a QueryToken')
        if isinstance(query_token, QueryPhraseLabelToken):
            return query_token.phrase_label in self.phrase_labels
        else:
            return False
