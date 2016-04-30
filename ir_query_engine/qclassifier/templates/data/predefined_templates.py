from ir_query_engine.qclassifier.templates.question_template import QuestionTemplate


PREDEFINED_TEMPLATES = [

    # Factoid
    QuestionTemplate('(what|where|who|when) (is|are|was|were) [NP]'),
    QuestionTemplate('I want to know about [NP]'),
    QuestionTemplate('show me [NP]'),

    # Factoid.yes_no
    QuestionTemplate('(is|are) [NP] [NP|ADJP|PP]'),

    # Factoid.duration
    QuestionTemplate('How long does [NP] take'),
    QuestionTemplate('How long does it take to [VP]'),
    QuestionTemplate('How long do I need to wait for [NP]'),

    # Action
    QuestionTemplate('how to [VP]'),
    QuestionTemplate('[VP]'),
    QuestionTemplate('can I [VP]'),
    QuestionTemplate('can [NP] [VP]'),

    # Action.business
    QuestionTemplate('do you [VP]'),
    QuestionTemplate('do you [VP] [NP]'),

    # RequestExplanation
    QuestionTemplate('why [NP] [VP]'),
    QuestionTemplate('what if [NP] [VP]'),
    QuestionTemplate('[NP] [VP]'),
]