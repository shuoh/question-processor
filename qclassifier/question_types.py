class QuestionClassificationResult(object):

    def __init__(self):
        pass


class FactoidQuestion(QuestionClassificationResult):

    def get_answer_type(self):
        pass

    def get_entity(self):
        pass

    def get_property(self):
        pass


class WhQuestion(FactoidQuestion):
    """What/who/when/where questions about a fact"""
    pass


class YesNoQuestion(FactoidQuestion):
    """Questions about a fact that expect a yes/no answer"""
    pass


class HowToQuestion(QuestionClassificationResult):
    """Procedural questions about how to achieve a specific goal """

    def get_action_verb(self):
        pass

    def get_action_argument(self):
        pass

    def get_action_condition(self):
        pass


class RequestExplanationQuestion(QuestionClassificationResult):
    """Questions about why a specific thing happens, e.g. 'Why the shipment has not arrived yet?' """

    def get_fact(self):
        pass