# Access configuration

You can use the “access to resource-name” command for obtaining 1 hour access to a specific resource.

The default configuration relies on a “manual approval” workflow, which delegates access request approvals to the bot admins (`SDM_ADMINS`).

When an access request is registered, the bot assigns an `access_request_id` and notifies all the admins. In order to approve a request, 
it’s enough that one of the admins sends to the accessbot the message: **yes `access_request_id`** before the timeout (`SDM_ADMIN_TIMEOUT`) expires. 
If an access request times out without approval, it's automatically rejected and deleted.

<img src="https://user-images.githubusercontent.com/313803/116870875-9fc86a80-ac13-11eb-94a7-9d96e2682c36.png" width="60%" height="60%">

Besides the “manual approval” workflow, you can configure:
* Automatic approval for all (`SDM_AUTO_APPROVE_ALL`). Automatically grant access to all available resources - no need for admin approval.
* Automatic approval by tag (`SDM_AUTO_APPROVE_TAG`). Automatically grant access to all tagged available resources. Auto-approve resources will be highlighted when executing: _show available resources_
* Hide tagged resources (`SDM_HIDE_RESOURCE_TAG`). Remove tagged resources from the list of available resources. Hidden resources will not be shown when executing: _show available resources_

## Possible workflows

Different workflows (permutations) can be configured using the flags mentioned above - adjustable at runtime via [plugin config](docs/CONFIGURE_ACCESSBOT.md).
* Manually approve all resources. Default workflow
* Manually approve all resources, but auto approve a subset: `SDM_AUTO_APPROVE_TAG`
* Manually approve all resources, but exclude a subset: `SDM_HIDE_RESOURCE_TAG`
* Manually approve all resources, but auto approve some and exclude others: `SDM_AUTO_APPROVE_TAG` + `SDM_HIDE_RESOURCE_TAG`
* Auto approve all: `SDM_AUTO_APPROVE_ALL`
* Auto approve all, but exclude a subset: `SDM_AUTO_APPROVE_ALL` + `SDM_HIDE_RESOURCE_TAG`
