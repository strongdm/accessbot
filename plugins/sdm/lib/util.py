import enum
from fuzzywuzzy import fuzz

FUZZY_MATCH_THRESHOLD = 50 # Base 100

class HiddenTagEnum(enum.Enum):
    RESOURCE = 'HIDE_RESOURCE_TAG'
    ROLE = 'HIDE_ROLE_TAG'

class AllowedTagEnum(enum.Enum):
    RESOURCE = 'ALLOW_RESOURCE_TAG'

def is_hidden(config, hidden_tag_enum, sdm_entity):
    hide_entity_tag = config[hidden_tag_enum.value]
    return hide_entity_tag and \
           hide_entity_tag in sdm_entity.tags and \
           (sdm_entity.tags.get(hide_entity_tag) is None or str(sdm_entity.tags.get(hide_entity_tag)).lower().strip() != 'false')

def is_allowed(config, allowed_tag_enum, sdm_entity):
    allowed_entity_tag = config[allowed_tag_enum.value]
    return not allowed_entity_tag \
        or (allowed_entity_tag in sdm_entity.tags and (sdm_entity.tags.get(allowed_entity_tag) is None
            or str(sdm_entity.tags.get(allowed_entity_tag)).lower().strip() != 'false'))

def is_concealed(config, sdm_resource):
    conceal_resource_tag = config['CONCEAL_RESOURCE_TAG']
    return conceal_resource_tag and \
           conceal_resource_tag in sdm_resource.tags and \
           (sdm_resource.tags.get(conceal_resource_tag) is None or str(sdm_resource.tags.get(conceal_resource_tag)).lower().strip() != 'false')

def can_auto_approve_by_tag(config, sdm_object, tag_key):
    auto_approve_by_tag = config[tag_key]
    return auto_approve_by_tag and \
            auto_approve_by_tag in sdm_object.tags and \
            (sdm_object.tags.get(auto_approve_by_tag) is None or str(sdm_object.tags.get(auto_approve_by_tag)).lower().strip() != 'false')

def can_auto_approve_by_groups_tag(config, sdm_object, sdm_account):
    auto_approve_groups_tag = config['AUTO_APPROVE_GROUPS_TAG']
    groups_tag = config['GROUPS_TAG']
    return auto_approve_groups_tag and \
            groups_tag and \
            auto_approve_groups_tag in sdm_object.tags and \
            groups_tag in sdm_account.tags and \
            sdm_object.tags.get(auto_approve_groups_tag) is not None and \
            sdm_account.tags.get(groups_tag) is not None and \
            has_intersection(sdm_object.tags[auto_approve_groups_tag].strip().split(','), sdm_account.tags[groups_tag].strip().split(','))

def fuzzy_match(term_list, searched_term):
    names = [item.name for item in term_list]
    if len(names) == 0:
        return None
    max_ratio = 0
    max_ratio_name = None
    for name in names:
        # DISCLAIMER: token_sort_ratio is CPU demanding compared to other options, like: ratio or partial_ratio
        ratio = fuzz.token_sort_ratio(name, searched_term)
        if ratio > max_ratio:
            max_ratio = ratio
            max_ratio_name = name
    return max_ratio_name if max_ratio >= FUZZY_MATCH_THRESHOLD else None

def has_intersection(list_a, list_b):
    for a in list_a:
        for b in list_b:
            if a == b:
                return True
    return False
