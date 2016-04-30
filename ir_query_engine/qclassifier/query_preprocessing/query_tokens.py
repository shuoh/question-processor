import re


VALID_QUERY_PHRASE_LABEL_REGEX = '\[[A-Z]+\]'
# NOTE: if the query input itself contains phrase-label-like substring like '[NP]', it would have been split into
# multiple tokens by the interpreter, so you should see something like '[ NP ]' in the interpreted string
VALID_QUERY_WORD_TOKEN_REGEX = '.*[a-zA-Z0-9].*'


def tokenize_interpreted_query(interpreted_query):
    """
    :param interpreted_query: normalized input query, with phrase label replacement applied. Example: what is [NP] ?
    :return: a list of QueryToken objects
    """
    tokens = []
    for token in interpreted_query.split(' '):
        if not token:
            raise Exception('Unexpected condition')
        # make sure check phrase first
        if re.match('^'+VALID_QUERY_PHRASE_LABEL_REGEX+'$', token):
            tokens.append(QueryPhraseLabelToken(token[1:-1].upper()))
        elif re.match('^'+VALID_QUERY_WORD_TOKEN_REGEX+'$', token):
            tokens.append(QueryWordToken(token.lower()))
        else:
            # all the other stuff are treated as punctuation, which are given a lower weight during matching
            tokens.append(QueryPunctuationToken(token.lower()))
    return tokens


class QueryToken(object):
    pass


class QueryWordToken(QueryToken):

    def __init__(self, word):
        self.word = word


class QueryPhraseLabelToken(QueryToken):

    def __init__(self, phrase_label):
        self.phrase_label = phrase_label


class QueryPunctuationToken(QueryToken):

    def __init__(self, punct_str):
        self.punct_str = punct_str
