from simplejson import loads
from nltk.tree import Tree
from ir_query_engine.qclassifier.utils import jsonrpc

CORENLP_SERVER_HOST = 'ec2-52-38-116-30.us-west-2.compute.amazonaws.com'
CORENLP_SERVER_PORT = 8080


class SentenceParser(object):
    """
    The performance of the NLTK wrapper for Stanford CoreNLP is unacceptable.
    This implementation is based on sending parsing request to a standalone server that runs CoreNLP Java library
    For more information, checkout https://github.com/dasmith/stanford-corenlp-python
    """

    def parse(self, text):
        """
        NOTE: since the Stanford tagger and parser libraries are case-sensitive, the casing of the output of this
              method is preserved. Caller must remember to normalize the casing when conducting comparison
        :param text: text to be parsed
        :return: a SentenceParseResult object
        }
        """
        server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),
                                     jsonrpc.TransportTcpIp(addr=(CORENLP_SERVER_HOST, CORENLP_SERVER_PORT)))

        parsed_sentences = loads(server.parse(text))['sentences']
        if len(parsed_sentences) > 1:
            raise Exception('Multi-sentence query is not supported')
        parsed_sentence = parsed_sentences[0]

        word_tokens = [ParsedWordToken(word_wire_format) for word_wire_format in parsed_sentence['words']]
        # word_tokens = self._recover_contractions(word_tokens)

        normalized_sentence = ' '.join([word_token.text for word_token in word_tokens])

        parsed_tree = Tree.fromstring(parsed_sentence['parsetree'])

        token_dependency = parsed_sentence['dependencies']

        return SentenceParseResult(word_tokens=word_tokens,
                                   normalized_sentence=normalized_sentence,
                                   parsed_tree=parsed_tree,
                                   token_dependency=token_dependency)

    @staticmethod
    def _recover_contractions(word_tokens):
        # TODO: http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
        return word_tokens


class SentenceParseResult(object):

    def __init__(self, word_tokens, normalized_sentence, parsed_tree, token_dependency):
        """
        :param word_tokens: list(ParsedWordToken)
        :param normalized_sentence: str
        :param parsed_tree: nltk.Tree
        :param token_dependency: list((dep_type, head_token, dependent_token))
        """
        self.word_tokens = word_tokens
        self.normalized_sentence = normalized_sentence
        self.parsed_tree = parsed_tree
        self.token_dependency = token_dependency


class ParsedWordToken(object):

    def __init__(self, core_nlp_result):
        """
        [u'What',
             {u'CharacterOffsetBegin': u'0',
              u'CharacterOffsetEnd': u'4',
              u'Lemma': u'what',
              u'NamedEntityTag': u'O',
              u'PartOfSpeech': u'WP'}]
        """
        self.text = core_nlp_result[0]
        self.lemma = core_nlp_result[1]['Lemma']
        self.pos = core_nlp_result[1]['PartOfSpeech']
