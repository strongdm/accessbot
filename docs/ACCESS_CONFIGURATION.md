# Access configuration
You can use the “access to resource-name” command for obtaining 1 hour access to a specific resource.

The default configuration relies on a “manual approval” workflow, which delegates access request approvals to the bot admins (`SDM_ADMINS`).

When an access request is registered, the bot assigns an `access_request_id` and notifies all the admins. In order to approve a request, 
it’s enough that one of the admins sends to the accessbot the message: **yes `access_request_id`** before the timeout (`SDM_ADMIN_TIMEOUT`) expires. 
If an access request times out without approval, it's automatically rejected and deleted.

<img src="https://user-images.githubusercontent.com/313803/116870875-9fc86a80-ac13-11eb-94a7-9d96e2682c36.png" width="60%" height="60%">

Besides the “manual approval” workflow, you can configure:
* Automatic approval for all resources (`SDM_AUTO_APPROVE_ALL`). Automatically grant access to all available resources - no need for admin approval.
* Automatic approval by tag for resources (`SDM_AUTO_APPROVE_TAG`). Automatically grant access to all tagged available resources. Delete the tag or set it false to disable. Auto-approve resources will be highlighted when executing: _show available resources_
* Hide tagged resources (`SDM_HIDE_RESOURCE_TAG`). Remove tagged resources from the list of available resources. The tag value is ignored, delete tag to disable. Hidden resources will not be shown when executing: _show available resources_
* Automatic approval for all roles (`SDM_AUTO_APPROVE_ROLE_ALL`). Automatically grant access to all available roles - no need for admin approval.
* Automatic approval by tag for roles (`SDM_AUTO_APPROVE_ROLE_TAG`). Automatically grant access to all tagged available roles. Delete the tag or set it false to disable. Auto-approve roles will be highlighted when executing: _show available roles_

## Possible workflows
Different workflows (permutations) can be configured using the flags mentioned above - adjustable at runtime via [plugin config](docs/CONFIGURE_ACCESSBOT.md).
* Manually approve all resources. Default workflow
* Manually approve all resources, but auto approve a subset: `SDM_AUTO_APPROVE_TAG`
* Manually approve all resources, but exclude a subset: `SDM_HIDE_RESOURCE_TAG`
* Manually approve all resources, but auto approve some and exclude others: `SDM_AUTO_APPROVE_TAG` + `SDM_HIDE_RESOURCE_TAG`
* Auto approve all: `SDM_AUTO_APPROVE_ALL`
* Auto approve all, but exclude a subset: `SDM_AUTO_APPROVE_ALL` + `SDM_HIDE_RESOURCE_TAG`

## Using tags
Following some sample commands you can use for configuring tags (e.g. `SDM_AUTO_APPROVE_TAG=auto-approve`):
```
$ sdm admin datasources list -e
Datasource ID           Name                 Type          ...         Tags
rs-4c29d3006066e7ef     snowflake-test-1     snowflake     ...
rs-3b4d153c6066effe     snowflake-test-2     snowflake     ...
$ sdm admin datasources update snowflake --id rs-4c29d3006066e7ef --tags 'auto-approve=true'
changed 1 out of 1 matching datasource
$ sdm admin datasources list -e
Datasource ID           Name                 Type          ...         Tags
rs-4c29d3006066e7ef     snowflake-test-1     snowflake     ...         **auto-approve=true**
rs-3b4d153c6066effe     snowflake-test-2     snowflake     ...
$ sdm admin datasources list --filter 'tags:auto-approve=true' -e
Datasource ID           Name                 Type          ...         Tags
rs-4c29d3006066e7ef     snowflake-test-1     snowflake     ...         **auto-approve=true**
```

For further information please refer to the [strongDM docs about tags](https://www.strongdm.com/docs/automation/getting-started/tags).
