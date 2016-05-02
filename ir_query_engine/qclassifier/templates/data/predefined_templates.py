from ir_query_engine.qclassifier.templates.question_template import QuestionTemplate
from ir_query_engine.knowledge_base.query.query_language import FactoidQuery, ActionQuery, RequestExplanationQuery

# NOTE: question templates should contain either literal words (e.g. 'how'), word variants (e.g. '(a|b|c)'),
#       phrase labels (e.g. '[NP|VP]'). Phrase label must be in uppercase, words can be in either case. No punctuation
#       is allowed. For more information, see question_template.py

PREDEFINED_TEMPLATES = [

    # Factoid
    QuestionTemplate('(what|where|who|when) (is|are|was|were) [NP]',
                     lambda np: FactoidQuery.make_np_query(np)),
    QuestionTemplate('I want to know about [NP]',
                     lambda np: FactoidQuery.make_np_query(np)),
    QuestionTemplate('show me [NP]',
                     lambda np: FactoidQuery.make_np_query(np)),
    QuestionTemplate('(how|where) (do|can) I (know|check|find) [NP]',
                     lambda np: FactoidQuery.make_np_query(np)),

    # Factoid.yes_no
    QuestionTemplate('(is|are|was|were) [NP] [NP|ADJP|PP|VP]',
                     lambda np, value: FactoidQuery.make_np_value_query(np, value)),
    QuestionTemplate('(is|are|was|were) there (a|an|any) [NP] [ADJP|PP|VP]',
                     lambda np, value: FactoidQuery.make_np_value_query(np, value)),
    QuestionTemplate('will there be (a|an|any) [NP] [ADJP|PP|VP]',
                     lambda np, value: FactoidQuery.make_np_value_query(np, value)),

    # Factoid.duration
    QuestionTemplate('how long (does|will) [NP] take',
                     lambda np: FactoidQuery.make_np_duration_query(np)),
    QuestionTemplate('how long do I need to wait for [NP]',
                     lambda np: FactoidQuery.make_np_duration_query(np)),
    QuestionTemplate('how long does it take to [VP]',
                     lambda vp: FactoidQuery.make_vp_duration_query(vp)),

    # Factoid.deadline
    QuestionTemplate('when (can|do|will) I (get|expect) [NP]',
                     lambda np: FactoidQuery.make_np_deadline_query(np)),
    QuestionTemplate('when (can|do|will) I (get|expect) [NP] [ADJP|PP|VP]',
                     lambda np, condition: FactoidQuery.make_np_deadline_query(np, condition)),
    QuestionTemplate('when is [NP] (ready|available)',
                     lambda np: FactoidQuery.make_np_deadline_query(np)),
    QuestionTemplate('when will [NP] be (ready|available)',
                     lambda np: FactoidQuery.make_np_deadline_query(np)),
    QuestionTemplate('when (is|are|was|were) [NP] [NP|ADJP|PP|VP]',
                     lambda np, condition: FactoidQuery.make_np_deadline_query(np, condition)),
    QuestionTemplate('when (do|does|did|will|have|has) [NP] [VP]',
                     lambda np, condition: FactoidQuery.make_np_deadline_query(np, condition)),

    # Action.customer
    QuestionTemplate('how to [VP]',
                     lambda vp: ActionQuery.make_customer_action_query(vp)),
    QuestionTemplate('how (do|can|should) I [VP]',
                     lambda vp: ActionQuery.make_customer_action_query(vp)),
    QuestionTemplate('what do I need to do to [VP]',
                     lambda vp: ActionQuery.make_customer_action_query(vp)),
    QuestionTemplate('what should I do to [VP]',
                     lambda vp: ActionQuery.make_customer_action_query(vp)),
    QuestionTemplate('what if I (need|want) to [VP]',
                     lambda vp: ActionQuery.make_customer_action_query(vp)),
    QuestionTemplate('[VP]',
                     lambda vp: ActionQuery.make_customer_action_query(vp)),
    QuestionTemplate('can I [VP]',
                     lambda vp: ActionQuery.make_customer_action_query(vp, asking_for_perm=True)),
    QuestionTemplate('how do I (know|check) (if|whether) [NP] [VP]',
                     lambda np, vp: ActionQuery.make_customer_checking_action_query(np, vp)),
    QuestionTemplate('how do I (know|check) (if|whether) [NP] (is|are|was|were) [NP|ADJP|PP|VP]',
                     lambda np, condition: ActionQuery.make_customer_checking_action_query(np, condition)),
    QuestionTemplate('how do I (know|check) (if|whether) there (is|are|was|were) (a|an|any) [NP] [ADJP|PP|VP]',
                     lambda np, condition: ActionQuery.make_customer_checking_action_query(np, condition)),

    # Action.someone_else
    QuestionTemplate('can [NP] [VP]',
                     lambda np, vp: ActionQuery.make_someone_else_action_query(np, vp, asking_for_perm=True)),
    QuestionTemplate('(do|does|did|will|have|has) [NP] [VP]',
                     lambda np, vp: ActionQuery.make_someone_else_action_query(np, vp, asking_for_perm=True)),

    # Action.business
    QuestionTemplate('(do|can) you [VP]',
                     lambda vp: ActionQuery.make_business_action_query(vp, asking_for_perm=True)),
    QuestionTemplate('(do|can) you (offer|allow|have) [NP]',
                     lambda np: ActionQuery.make_business_offering_action_query(np)),

    # RequestExplanation
    QuestionTemplate('why (is|are) [NP] [NP|ADJP|PP|VP]',
                     lambda np, des: RequestExplanationQuery.make_np_description_query(np, des)),
    QuestionTemplate('why (do|does|did|will|have|has) [NP] [VP]',
                     lambda np, vp: RequestExplanationQuery.make_np_description_query(np, vp)),
    QuestionTemplate('why [NP] [VP]',
                     lambda np, vp: RequestExplanationQuery.make_np_description_query(np, vp)),
    QuestionTemplate('how come [NP] [VP]',
                     lambda np, vp: RequestExplanationQuery.make_np_description_query(np, vp)),
    QuestionTemplate('what if [NP] [VP]',
                     lambda np, vp: RequestExplanationQuery.make_np_description_query(np, vp)),
    QuestionTemplate('what if [NP] (is|are|was|were) [VP]',
                     lambda np, vp: RequestExplanationQuery.make_np_description_query(np, vp)),
    QuestionTemplate('[NP] [VP]',
                     lambda np, vp: RequestExplanationQuery.make_np_description_query(np, vp)),
]