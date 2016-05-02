from ir_query_engine.qclassifier.templates.question_template import QuestionTemplate

# NOTE: question templates should contain either literal words (e.g. 'how'), word variants (e.g. '(a|b|c)'),
#       phrase labels (e.g. '[NP|VP]'). Phrase label must be in uppercase, words can be in either case. No punctuation
#       is allowed. For more information, see question_template.py

PREDEFINED_TEMPLATES = [

    # Factoid
    QuestionTemplate('(what|where|who|when) (is|are|was|were) [NP]'),
    QuestionTemplate('I want to know about [NP]'),
    QuestionTemplate('show me [NP]'),
    QuestionTemplate('(how|where) (do|can) I (know|check|find) [NP]'),

    # Factoid.yes_no
    QuestionTemplate('(is|are|was|were) [NP] [NP|ADJP|PP|VP]'),  # seed
    QuestionTemplate('(do|does|did|will|have|has) [NP] [VP]'),  # seed
    QuestionTemplate('(is|are|was|were) there (a|an|any) [NP] [ADJP|PP|VP]'),
    QuestionTemplate('will there be (a|an|any) [NP] [ADJP|PP|VP]'),
    QuestionTemplate('how do I (know|check) (if|whether) [NP] [VP]'),
    QuestionTemplate('how do I (know|check) (if|whether) [NP] (is|are|was|were) [NP|ADJP|PP|VP]'),
    QuestionTemplate('how do I (know|check) (if|whether) there (is|are|was|were) (a|an|any) [NP] [ADJP|PP|VP]'),

    # Factoid.time
    QuestionTemplate('how long (does|will) [NP] take'),
    QuestionTemplate('how long do I need to wait for [NP]'),
    QuestionTemplate('when (can|do|will) I (get|expect) [NP]'),
    QuestionTemplate('when (can|do|will) I (get|expect) [NP] [ADJP|PP|VP]'),
    QuestionTemplate('when is [NP] (ready|available)'),
    QuestionTemplate('when will [NP] be (ready|available)'),
    QuestionTemplate('how long does it take to [VP]'),
    QuestionTemplate('when (is|are|was|were) [NP] [NP|ADJP|PP|VP]'),
    QuestionTemplate('when (do|does|did|will|have|has) [NP] [VP]'),

    # Action.customer
    QuestionTemplate('how to [VP]'),
    QuestionTemplate('how (do|can|should) I [VP]'),
    QuestionTemplate('what do I need to do to [VP]'),
    QuestionTemplate('what should I do to [VP]'),
    QuestionTemplate('what if I (need|want) to [VP]'),
    QuestionTemplate('[VP]'),
    QuestionTemplate('can I [VP]'),

    # Action.else
    QuestionTemplate('can [NP] [VP]'),

    # Action.business
    QuestionTemplate('(do|can) you [VP]'),
    QuestionTemplate('(do|can) you [VP] [NP]'),
    QuestionTemplate('(do|can) you (offer|allow|have) [NP]'),

    # RequestExplanation
    QuestionTemplate('why (is|are) [NP] [NP|ADJP|PP|VP]'),
    QuestionTemplate('why (do|does|did|will|have|has) [NP] [VP]'),
    QuestionTemplate('why [NP] [VP]'),
    QuestionTemplate('how come [NP] [VP]'),
    QuestionTemplate('what if [NP] [VP]'),
    QuestionTemplate('what if [NP] (is|are|was|were) [VP]'),
    QuestionTemplate('[NP] [VP]'),
]