class FactoidQuery(object):

    def __init__(self, entity, attribute, entity_modifiers=[], attribute_modifiers=[], value=None):
        """
        :param entity: str
        :param attribute: str (dot-separated string if the question involves query on a nested attribute).
                          For example, query structure for "what is the year of Obama's birth?" can be described sa
                          entity=Obama, attribute=birth.year
        :param entity_modifiers: list(str)
        :param attribute_modifiers: list(str)
        :param value: str (optional, only specified when the input is a yes/no question)
        """
        self.entity = entity
        self.attribute = attribute
        self.entity_modifiers = entity_modifiers
        self.attribute_modifiers = attribute_modifiers
        self.value = value

    @staticmethod
    def make_np_query(np_concept, attribute_literal=None):
        """
        variations of "what is [NP]?"
        :param np_concept: NounPhraseTokenConcept
        :param attribute_literal: queried attribute according to the template (e.g. duration, deadline)
        """
        return FactoidQuery()

    @staticmethod
    def make_vp_query(vp_concept, attribute_literal=None):
        """
        variations of "what is the blabla of [VP]?"
        :param vp_concept: VerbPhraseTokenConcept
        :param attribute_literal: queried attribute according to the template (e.g. duration, deadline)
        """
        return FactoidQuery()

    @staticmethod
    def make_np_value_query(np_concept, value_concept, attribute_literal=None):
        """
        variations of "
        :param np_concept: NounPhraseTokenConcept
        :param value_concept: any PhraseTokenConcept object
        :param attribute_literal: queried attribute according to the template (e.g. duration, deadline)
        """
        return FactoidQuery

    @staticmethod
    def make_np_duration_query(np_concept):
        return FactoidQuery.make_np_query(np_concept, 'duration')

    @staticmethod
    def make_vp_duration_query(vp_concept):
        return FactoidQuery.make_vp_query(vp_concept, 'duration')

    @staticmethod
    def make_np_deadline_query(np_concept, condition_concept=None):
        return


class ActionQuery(object):

    def __init__(self, subject, action, object_, asking_for_perm=False, action_modifiers=[], object_modifiers=[]):
        self.subject = subject
        self.action = action
        self.object = object_
        self.asking_for_perm = asking_for_perm
        self.action_modifiers = action_modifiers
        self.object_modifiers = object_modifiers

    @staticmethod
    def make_customer_action_query(vp_concept, asking_for_perm=False):
        return

    @staticmethod
    def make_customer_checking_action_query(np_concept, expected_status_concept):
        return

    @staticmethod
    def make_business_action_query(vp_concept, asking_for_perm=False):
        return

    @staticmethod
    def make_business_offering_action_query(np_concept):
        return

    @staticmethod
    def make_someone_else_action_query(np_concept, vp_concept, asking_for_perm=False):
        return


class RequestExplanationQuery(object):

    def __init__(self, subject, action, object_, subject_modifiers=[], action_modifiers=[], object_modifiers=[]):
        self.subject = subject
        self.action = action
        self.object = object_
        self.subject_modifiers = subject_modifiers
        self.action_modifiers = action_modifiers
        self.object_modifiers = object_modifiers

    @staticmethod
    def make_np_description_query(np_concept, description_concept):
        return
