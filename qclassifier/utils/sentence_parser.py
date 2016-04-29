from nltk import word_tokenize, sent_tokenize
from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordPOSTagger


class SentenceParser(object):

    _stanford_pos_tagger = StanfordPOSTagger('english-bidirectional-distsim.tagger')
    _stanford_parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

    def parse(self, text):
        """
        :param text: text to be parsed
        :return: dict including the following entries
        {
            'word_tokens': list(str),
            'normalized_sentence': str,
            'pos_tags': list(tuple(str, str)),
            'parsed_tree': Tree
        }
        """
        text = text.lower()
        sentences = sent_tokenize(text)
        if len(sentences) > 1:
            raise Exception('Multi-sentence query is not supported')

        word_tokens = word_tokenize(sentences[0])
        normalized_sentence = ' '.join(word_tokens)
        pos_tags = self._stanford_pos_tagger.tag(word_tokens)
        parsed_tree_list = list(self._stanford_parser.tagged_parse(pos_tags))

        return {
            'word_tokens': word_tokens,
            'normalized_sentence': normalized_sentence,
            'pos_tags': pos_tags,
            'parsed_tree': parsed_tree_list[0],
        }


PARSER = SentenceParser()
