
def is_hidden_resource(config, sdm_resource):
    hide_resource_tag = config['HIDE_RESOURCE_TAG']
    return hide_resource_tag and \
            hide_resource_tag in sdm_resource.tags and \
            (sdm_resource.tags.get(hide_resource_tag) is not False or sdm_resource.tags.get(hide_resource_tag))
