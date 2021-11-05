import re
import os
import enum
from fuzzywuzzy import fuzz

FUZZY_MATCH_THRESHOLD = 50 # Base 100

class HiddenTagEnum(enum.Enum):
    RESOURCE = 'HIDE_RESOURCE_TAG'
    ROLE = 'HIDE_ROLE_TAG'

def is_hidden(config, hidden_tag_enum, sdm_entity):
    hide_entity_tag = config[hidden_tag_enum.value]
    return hide_entity_tag and \
           hide_entity_tag in sdm_entity.tags and \
           (sdm_entity.tags.get(hide_entity_tag) is None or str(sdm_entity.tags.get(hide_entity_tag)).lower().strip() != 'false')

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

def clean_up_message(text):
    bot_platform = os.getenv('SDM_BOT_PLATFORM')
    if bot_platform == 'ms-teams':
        text = re.sub(r'<at>.+</at>', '', text).strip()
    return text
