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

        word_dependency = SentenceWordDependency(parsed_sentence['dependencies'])

        return SentenceParseResult(word_tokens=word_tokens,
                                   normalized_sentence=normalized_sentence,
                                   parsed_tree=parsed_tree,
                                   word_dependency=word_dependency)

    @staticmethod
    def _recover_contractions(word_tokens):
        # TODO: http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
        return word_tokens


class SentenceParseResult(object):

    def __init__(self, word_tokens, normalized_sentence, parsed_tree, word_dependency):
        """
        :param word_tokens: list(ParsedWordToken)
        :param normalized_sentence: str
        :param parsed_tree: nltk.Tree
        :param word_dependency: SentenceWordDependency
        """
        self.word_tokens = word_tokens
        self.normalized_sentence = normalized_sentence
        self.parsed_tree = parsed_tree
        self.word_dependency = word_dependency


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


class SentenceWordDependency(object):

    def __init__(self, core_nlp_result):
        """
        [[u'root', u'ROOT', u'take'],
         [u'advmod', u'long', u'How'],
         [u'dep', u'take', u'long'],
         [u'aux', u'take', u'does'],
         [u'nsubj', u'take', u'shipping']]
        """
        self._head_word_lookup_dict = self._construct_head_word_lookup_dict(core_nlp_result)

    @staticmethod
    def _construct_head_word_lookup_dict(core_nlp_result):
        lookup_dict = {}
        for triple in core_nlp_result:
            # ignore root dependency
            if triple[0] == 'root':
                continue
            # ignore self relation
            if triple[1] == triple[2]:
                continue
            head_word = triple[1]
            if head_word not in lookup_dict:
                lookup_dict[head_word] = []
            lookup_dict[head_word].append(triple)
        return lookup_dict

    def __repr__(self):
        return str(self._head_word_lookup_dict)

    def lookup_dependencies_on(self, head, dependent=None, transitive=False):
        """
        :param head: the head (governor) of the relation
        :param dependent: the dependent (optional)
        :param transitive: True if transitive dependencies are also considered.
                           This parameter is ignored if dependent is None
        :return: a list of dependencies if there's any found, empty list otherwise
        """
        results = []
        if head in self._head_word_lookup_dict:
            direct_relations = self._head_word_lookup_dict[head]
            if dependent:
                results = [triple for triple in direct_relations if triple[2] == dependent]
                if not results and transitive:
                    for intermediate in direct_relations:
                        if self.lookup_dependencies_on(intermediate[2], dependent, True):
                            return [(None, head, dependent)]
            else:
                results = direct_relations

        return results
