def find_head_word_for_noun_phrase(words, word_dependency):
    return _find_head_word(words, word_dependency, _is_noun_word_pos)


def find_head_word_for_verb_phrase(words, word_dependency):
    return _find_head_word(words, word_dependency, _is_verb_word_pos)


def find_head_word_for_adjective_phrase(words, word_dependency):
    return _find_head_word(words, word_dependency, _is_adjective_word_pos)


def _find_head_word(words, word_dependency, candidate_selector):
    """
    Simple implementation based on POS tags and universal dependency
    :param words: list(ParsedWordToken)
    :param word_dependency: SentenceWordDependency object
    :param candidate_selector: the function used to pre-filter head word candidates
    :return: (head_word_token, all_candidates)
    """
    candidate_words = [word for word in words if candidate_selector(word.pos)]

    # remove words that have dependency on other words
    dependency_heads = []
    for candidate in candidate_words:
        is_dependent = False
        for other_candidate in candidate_words:
            if candidate is other_candidate:
                continue
            if word_dependency.lookup_dependencies_on(head=other_candidate.text,
                                                      dependent=candidate.text,
                                                      transitive=True):
                is_dependent = True
                break
        if not is_dependent:
            dependency_heads.append(candidate)

    # TODO: might need better handling on this case
    if len(dependency_heads) != 1:
        phrase_txt = ' '.join([word.text for word in words])
        all_heads_txt = ', '.join([word.text for word in dependency_heads])
        print 'WARNING: Found multiple head words [%s] in phrase [%s]. Returning the rightmost candidate...' \
              % (all_heads_txt, phrase_txt)

    return dependency_heads[-1], candidate_words


def _is_noun_word_pos(word_pos):
    return word_pos in ['EX', 'PRP', 'NN', 'NNS', 'NNP', 'NNPS']


def _is_verb_word_pos(word_pos):
    return word_pos in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def _is_adjective_word_pos(word_pos):
    return word_pos in ['JJ', 'JJR', 'JJS', 'VBG', 'VBN']
