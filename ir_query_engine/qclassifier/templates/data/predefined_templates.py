from ir_query_engine.qclassifier.templates.question_templates import QuestionTemplate


PREDEFINED_TEMPLATES = [
    QuestionTemplate('What is [NP]'),
    QuestionTemplate('I want to know about [NP]'),
    QuestionTemplate('show me [NP]'),
    QuestionTemplate('is [NP] [NP]'),
    QuestionTemplate('do you [VP] [NP]'),
    QuestionTemplate('how to [VP]'),
    QuestionTemplate('[VP]'),
    QuestionTemplate('can I [VP]'),
    QuestionTemplate('can [NP] [VP]'),
    QuestionTemplate('why [NP] [VP]'),
    QuestionTemplate('what if [NP] [VP]'),
    QuestionTemplate('[NP] [VP]'),
]