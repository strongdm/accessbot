---
layout: default
title: SDM Token requirements
nav_order: 2
parent: Accessbot Configuration
---


# Configure SDM

In order to configure SDM you need to [create an API Key](https://www.strongdm.com/docs/admin-ui-guide/settings/admin-tokens/api-keys) 
with -at least- the following permissions:
* **datasource:list**
* **grant:read**
* **grant:write**
* **user:list**
* **role:list** (only when using _CONTROL_RESOURCES_ROLE_NAME_)

**Use the API Key ID and SECRET as SDM_ACCESS_KEY and SDM_SECRET_KEY respectively** 
