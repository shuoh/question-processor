from ir_query_engine.qclassifier.query_concept_extraction.phrase_token_concept_extractor import *


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

    def __repr__(self):
        if self.value:
            return 'SELECT value=="%s" FROM Factoid WHERE entity=%s[%s], attribute=%s[%s]' \
                   % (self.value, self.entity, ','.join(self.entity_modifiers),
                      self.attribute, ','.join(self.attribute_modifiers))
        else:
            return 'SELECT answer FROM Factoid WHERE entity=%s[%s], attribute=%s[%s]' \
                   % (self.entity, ','.join(self.entity_modifiers), self.attribute, ','.join(self.attribute_modifiers))

    @staticmethod
    def make_np_query(np_concept, attribute_literal=None):
        """
        Variations of "what is [NP]?"
        :param np_concept: NounPhraseTokenConcept
        :param attribute_literal: queried attribute according to the template (e.g. duration, deadline)
        """
        entity = np_concept.entity
        if np_concept.attribute:
            attribute = np_concept.attribute + '.' + attribute_literal if attribute_literal else np_concept.attribute
        else:
            attribute = attribute_literal
        entity_mod = [mod[1] for mod in np_concept.entity_modifiers]
        attribute_mod = [mod[1] for mod in np_concept.attribute_modifiers]
        return FactoidQuery(entity, attribute, entity_mod, attribute_mod)

    @staticmethod
    def make_vp_query(vp_concept, attribute_literal=None):
        """
        Variations of "what is the blabla of [VP]?"
        :param vp_concept: VerbPhraseTokenConcept
        :param attribute_literal: queried attribute according to the template (e.g. duration, deadline)
        """
        if vp_concept.object:
            entity = vp_concept.action + ' ' + vp_concept.object
        else:
            entity = vp_concept.action
        entity_mod = [mod[1] for mod in vp_concept.action_modifiers]
        return FactoidQuery(entity, attribute_literal, entity_mod, [])

    @staticmethod
    def make_np_value_query(np_concept, value_concept, attribute_literal=None):
        """
        Variations of "is [NP] <value>?"
        :param np_concept: NounPhraseTokenConcept
        :param value_concept: any PhraseTokenConcept object
        :param attribute_literal: queried attribute according to the template (e.g. duration, deadline)
        """
        query = FactoidQuery.make_np_query(np_concept, attribute_literal)
        query.value = value_concept.to_simple_text()
        return query

    @staticmethod
    def make_np_duration_query(np_concept):
        """
        Variations of "how long does [NP] take?"
        :param np_concept: NounPhraseTokenConcept
        """
        return FactoidQuery.make_np_query(np_concept, 'duration')

    @staticmethod
    def make_vp_duration_query(vp_concept):
        """
        Varations of "how long does it take to [VP]?"
        :param vp_concept: VerbPhraseTokenConcept
        """
        return FactoidQuery.make_vp_query(vp_concept, 'duration')

    @staticmethod
    def make_np_deadline_query(np_concept, condition_concept=None):
        """
        Variations of "when will [NP] be <condition>?"
        :param np_concept: NounPhraseTokenConcept
        :param condition_concept:: any PhraseTokenConcept
        """
        query = FactoidQuery.make_np_query(np_concept, 'deadline')
        if condition_concept:
            query.attribute_modifiers.append(condition_concept.to_simple_text())
        return query


class ActionQuery(object):

    def __init__(self, subject, action, object_, asking_for_perm=False, action_modifiers=[], object_modifiers=[]):
        self.subject = subject
        self.action = action
        self.object = object_
        self.asking_for_perm = asking_for_perm
        self.action_modifiers = action_modifiers
        self.object_modifiers = object_modifiers

    def __repr__(self):
        if self.asking_for_perm:
            return 'SELECT allowed FROM Action WHERE subject=%s, action=%s[%s], object=%s[%s]' \
                   % (self.subject, self.action, ','.join(self.action_modifiers),
                      self.object, ','.join(self.object_modifiers))
        else:
            return 'SELECT answer FROM Action WHERE subject=%s, action=%s[%s], object=%s[%s]' \
                   % (self.subject, self.action, ','.join(self.action_modifiers),
                      self.object, ','.join(self.object_modifiers))

    @staticmethod
    def make_customer_action_query(vp_concept, asking_for_perm=False):
        return ActionQuery._make_action_query('customer', vp_concept, asking_for_perm)

    @staticmethod
    def make_business_action_query(vp_concept, asking_for_perm=False):
        return ActionQuery._make_action_query('business', vp_concept, asking_for_perm)

    @staticmethod
    def _make_action_query(subject, vp_concept, asking_for_perm):
        action_mod = [mod[1] for mod in vp_concept.action_modifiers]
        object_mod = [mod[1] for mod in vp_concept.object_modifiers]
        return ActionQuery(subject, vp_concept.action, vp_concept.object, asking_for_perm, action_mod, object_mod)

    @staticmethod
    def make_customer_checking_action_query(np_concept, expected_status_concept):
        object_mod = [mod[1] for mod in np_concept.entity_modifiers]
        query = ActionQuery(subject='customer', action='check', object_=np_concept.entity,
                            asking_for_perm=False, action_modifiers=[], object_modifiers=object_mod)
        if expected_status_concept:
            query.object_modifiers.append(expected_status_concept.to_simple_text())
        return query

    @staticmethod
    def make_business_offering_action_query(np_concept):
        object_mod = [mod[1] for mod in np_concept.entity_modifiers]
        query = ActionQuery(subject='business', action='offer', object_=np_concept.entity,
                            asking_for_perm=True, action_modifiers=[], object_modifiers=object_mod)
        return query

    @staticmethod
    def make_someone_else_action_query(np_concept, vp_concept, asking_for_perm=False):
        action_mod = [mod[1] for mod in vp_concept.action_modifiers]
        object_mod = [mod[1] for mod in vp_concept.object_modifiers]
        query = ActionQuery(subject=np_concept.entity,
                            action=vp_concept.action,
                            object_=vp_concept.object,
                            asking_for_perm=asking_for_perm,
                            action_modifiers=action_mod,
                            object_modifiers=object_mod)
        return query


class RequestExplanationQuery(object):

    def __init__(self, subject, action, object_, subject_modifiers=[], action_modifiers=[], object_modifiers=[]):
        self.subject = subject
        self.action = action
        self.object = object_
        self.subject_modifiers = subject_modifiers
        self.action_modifiers = action_modifiers
        self.object_modifiers = object_modifiers

    def __repr__(self):
        return 'SELECT explanation FROM RequestExplanation WHERE subject=%s, action=%s[%s], object=%s[%s]' \
               % (self.subject, self.action, ','.join(self.action_modifiers),
                  self.object, ','.join(self.object_modifiers))

    @staticmethod
    def make_np_description_query(np_concept, description_concept):
        subject = np_concept.entity
        subject_mod = [mod[1] for mod in np_concept.entity_modifiers]
        if isinstance(description_concept, VerbPhraseTokenConcept):
            action = description_concept.action
            action_mod = [mod[1] for mod in description_concept.action_modifiers]
            object_ = description_concept.object
            object_mod = [mod[1] for mod in description_concept.object_modifiers]
        else:
            action = 'be'
            action_mod = []
            if isinstance(description_concept, NounPhraseTokenConcept):
                object_ = description_concept.to_simple_text()
                object_mod = [mod[1] for mod in description_concept.entity_modifiers]
            elif isinstance(description_concept, AdjectivePhraseTokenConcept):
                object_ = description_concept.adjective
                object_mod = [mod[1] for mod in description_concept.adjective_modifiers]
            else:
                object_ = description_concept.to_simple_text()
                object_mod = []
        query = RequestExplanationQuery(subject=subject, action=action, object_=object_, subject_modifiers=subject_mod,
                                        action_modifiers=action_mod, object_modifiers=object_mod)
        return query

