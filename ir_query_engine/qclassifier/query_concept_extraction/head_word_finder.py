def find_head_word_for_noun_phrase(words, word_dependency):
    """
    Simple implementation based on POS tags and universal dependency
    :param words: list(ParsedWordToken)
    :param word_dependency: SentenceWordDependency object
    :return: the single head word of the phrase, represented by a ParsedWordToken object
    """
    noun_words = [word for word in words if _is_noun_word_pos(word.pos)]

    # remove words that have dependency on other words
    dependency_heads = []
    for noun_word in noun_words:
        is_dependent = False
        for other_noun_word in noun_words:
            if noun_word is other_noun_word:
                continue
            if word_dependency.lookup_dependencies_on(head=other_noun_word.text,
                                                      dependent=noun_word.text,
                                                      transitive=True):
                is_dependent = True
                break
        if not is_dependent:
            dependency_heads.append(noun_word)

    # TODO: might need better handling on this case
    if len(dependency_heads) != 1:
        phrase_txt = ' '.join([word.text for word in words])
        noun_words_txt = ', '.join([word.text for word in noun_words])
        print 'WARNING: Found multiple nouns [%s] in phrase [%s]. Returning the rightmost noun...' \
              % (noun_words_txt, phrase_txt)

    return dependency_heads[-1]


def _is_noun_word_pos(word_pos):
    return word_pos in [
        'EX',
        'PRP',
        'NN',
        'NNS',
        'NNP',
        'NNPS'
    ]
