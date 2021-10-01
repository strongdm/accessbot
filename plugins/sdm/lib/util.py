from fuzzywuzzy import fuzz

FUZZY_MATCH_THRESHOLD = 50 # Base 100

def is_hidden_resource(config, sdm_resource):
    hide_resource_tag = config['HIDE_RESOURCE_TAG']
    return hide_resource_tag and \
            hide_resource_tag in sdm_resource.tags and \
            (sdm_resource.tags.get(hide_resource_tag) is None or str(sdm_resource.tags.get(hide_resource_tag)).lower().strip() != 'false')

def is_hidden_role(config, sdm_role):
    hide_role_tag = config['HIDE_ROLE_TAG']
    return hide_role_tag and \
           hide_role_tag in sdm_role.tags and \
           (sdm_role.tags.get(hide_role_tag) is None or str(sdm_role.tags.get(hide_role_tag)).lower().strip() != 'false')

def can_auto_approve_by_tag(config, sdm_object, tag_key):
    auto_approve_by_tag = config[tag_key]
    return auto_approve_by_tag and \
            auto_approve_by_tag in sdm_object.tags and \
            (sdm_object.tags.get(auto_approve_by_tag) is None or str(sdm_object.tags.get(auto_approve_by_tag)).lower().strip() != 'false')

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
