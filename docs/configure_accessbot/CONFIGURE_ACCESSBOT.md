---
layout: default
title: AccessBot Environment Variables
nav_order: 4
parent: Accessbot Configuration
---
# Configure AccessBot

There are a number of variables you can use for configuring AccessBot.

## Required configuration
* **SDM_ADMINS**. List of SDM Platform Admins, format: `@usernick` (for slack). Although it's not required, these users are often SDM admins too. You could use `whoami` for getting user nick (slack handle). 
* **SDM_API_ACCESS_KEY**. SDM API Access Key
* **SDM_API_SECRET_KEY**. SDM API Access Key Secret

### Slack (SDM_BOT_PLATFORM='slack' / default)
* **SLACK_APP_TOKEN**. Slack App-Level Token 
* **SLACK_BOT_TOKEN**. Slack Bot User OAuth Token

### Slack Classic (SDM_BOT_PLATFORM='slack-classic')
* **SLACK_TOKEN**. Slack Bot User OAuth Token for Classic Slack bot version

### MS Teams (SDM_BOT_PLATFORM='ms-teams')
* **AZURE_APP_ID**. Set to the **Microsoft App ID**
* **AZURE_APP_PASSWORD**. Set to the **Secret Value** 

## Internal configuration
* **LOG_LEVEL**. Logging level. Default = INFO
* **SDM_DOCKERIZED**. Logging type. Default = true (_when using docker_), meaning logs go to STDOUT
* **SDM_COMMANDS_ENABLED**. AccessBot commands to be enabled. Default = `access_resource assign_role show_resources show_roles approve deny`. You could also specify aliases for specific commands. In that case, only add `:alias` after the command name, for example: `access_resource:acres show_resources:sares`.

## Bot configuration
The following variables can be changed at runtime via slack -by an SDM_ADMIN- using the `plugin config AccessBot` command:
* **SDM_ADMIN_TIMEOUT**. Timeout in seconds for a request to be manually approved. Default = 30 sec
* **SDM_SENDER_NICK_OVERRIDE**. Nickname to be used for all requests. Disabled by default (_useful for testing_)
* **SDM_SENDER_EMAIL_OVERRIDE**. Email to be used for all requests. Disabled by default (_useful for testing_)
* **SDM_AUTO_APPROVE_ALL**. Flag to enable auto-approve for all resources. Default = false
* **SDM_AUTO_APPROVE_TAG**. Resource tag to be used for auto-approve resources. The tag value is not ignored, delete tag or set it false to disable. Disabled by default
* **SDM_AUTO_APPROVE_ROLE_ALL**. Flag to enable auto-approve for all roles. Default = false
* **SDM_AUTO_APPROVE_ROLE_TAG**. Role tag to be used for auto-approve roles. The tag value is not ignored, delete tag or set it false to disable. Disabled by default
* **SDM_AUTO_APPROVE_GROUPS_TAG**. Resource tag to be used for auto-approve groups. The tag value should be a list of groups (see `SDM_GROUPS_TAG`) separated by comma. Disabled by default
* **SDM_ALLOW_RESOURCE_TAG**. Resource tag to be used for only showing the allowed resources. Ideally set the value to `true` or `false` (e.g. `allow-resource=true`). When there's no tag assigned, all resources are allowed (default behavior). Disabled by default ([see below](#using-tags) for more info about using tags)
* **SDM_ALLOW_ROLE_TAG**. Role tag to be used for only showing the allowed roles. Ideally set the value to `true` or `false` (e.g. `allow-role=true`). When there's no tag assigned, all roles are allowed (default behavior). Disabled by default ([see below](#using-tags) for more info about using tags)
* **SDM_HIDE_RESOURCE_TAG**. Resource tag to be used for hiding available resources, meaning that they are not going to be shown nor accessible. Ideally set value to `true` or `false` (e.g. `hide-resource=true`). If there's no value, it's interpreted as `true`. Disabled by default ([see below](#using-tags) for more info about using tags)
* **SDM_HIDE_ROLE_TAG**. Role tag to be used for hiding available roles, meaning that they are not going to be shown nor accessible. Ideally set value to `true` or `false` (e.g. `hide-role=true`). If there's no value, it's interpreted as `true`. Disabled by default ([see below](#using-tags) for more info about using tags)
* **SDM_CONCEAL_RESOURCE_TAG**. Resource tag to be used for concealing resources, meaning that they are not going to be shown but remain accessible. Ideally set value to `true` or `false` (e.g. `conceal-resource=true`). If there's no value, it's interpreted as `true`. Disabled by default ([see below](#using-tags) for more info about using tags)
* **SDM_GRANT_TIMEOUT**. Timeout in minutes for an access grant. Default = 60 min
* **SDM_CONTROL_RESOURCES_ROLE_NAME**. Role name to be used for getting available resources. Disabled by default
* **SDM_ADMINS_CHANNEL**. Channel name to be used by administrators for approval messages, for example: `#accessbot-private` (important to start with `#`). Disabled by default
* **SDM_ADMINS_CHANNEL_ELEVATE**. Boolean flag to allow usage of admin commands to all users inside the configured SDM_ADMINS_CHANNEL. When this is enabled the admin commands can no longer be sent via DM, only via the configured channel. Default = false
* **SDM_APPROVERS_CHANNEL_TAG**. Resource tag to be used for specifying the responsible approvers channel name for individual resources. For example: `SDM_APPROVERS_CHANNEL_TAG=approvers-channel` and inside the tags of a resource we would have `approvers-channel=my-resource-approvers`, in this scenario all access requests for that resource would be sent only to the `#my-resource-approvers` Slack channel. Disabled by default
* **SDM_MAX_AUTO_APPROVE_USES** and **SDM_MAX_AUTO_APPROVE_INTERVAL**. Max number of times that the auto-approve functionality can be used in an interval of configured minutes. Disabled by default
* **SDM_USER_ROLES_TAG**. User tag to be used for controlling the roles a user can request. Disabled by default
* **SDM_ENABLE_RESOURCES_FUZZY_MATCHING**. Flag to enable fuzzy matching for resources when a perfect match is not found. Default = true
* **SDM_RESOURCE_GRANT_TIMEOUT_TAG**. Resource tag to be used for registering the custom time (in minutes) that a specific resource will be made available for the user.
* **SDM_EMAIL_SLACK_FIELD**. Slack Profile Tag to be used for specifying a SDM email. For further information, please refer to [CONFIGURE_ALTERNATIVE_EMAILS.md](./CONFIGURE_ALTERNATIVE_EMAILS.md).
* **SDM_EMAIL_SUBADDRESS**. Flag to be used for specifying a subaddress for the SDM email (e.g. "user@email.com" becomes "user+sub@email.com" when SDM_EMAIL_SUBADDRESS equals to "sub"). Disabled by default
* **SDM_GROUPS_TAG**. User tag to be used for specifying the groups a user belongs to. Disabled by default
* **SDM_REQUIRED_FLAGS**. List of flags that should be required when using the "access" command. The flags should be separated by space, e.g. `reason duration`. By default, there are no required flags
* **SDM_ALLOW_RESOURCE_ACCESS_REQUEST_RENEWAL**. Flag to enable renewal of resource account grants. When enabled allows a user to make a new access request to a resource even if they already have access to it. Default = false

See image below for more information:

![image](img/bot-config.gif)

### Some tricks
* Use `plugin config AccessBot {}` for setting config to initial state. This command needs to be executed in a direct chat with AccessBot, cannot be used in channels
* Use `plugin info AccessBot` for showing all configurations, including remaining auto-approve uses
* Use `whoami` for showing user configuration. Use the `nick` field for the `SDM_ADMINS` variable

### Known issues
* When using `plugin config` from a Mac, you will need to disable: 
`System Preferences > Keyboard > Text > Uncheck "Use smart quotes and dashes`. The `config` command fails to understand quotes as unicode characters.

### Using Tags
A snippet that might help:

#### Allow Resource
```bash
$ sdm admin ssh list
Server ID               Name
rs-xxxxxxxxxxxxxxx     public-key-ssh
$ sdm admin ssh update --id rs-xxxxxxxxxxxxxxx --tags 'allow-resource=true'
changed 1 out of 1 matching datasource
$ sdm admin ssh list -e
Server ID               Name               Hostname                Port     Username           Port Override     Port Forwarding     Healthy     Secret Store ID     Egress Filter     Tags
rs-xxxxxxxxxxxxxxx     public-key-ssh     my-gw.example.com     2222     linuxserver.io     14760             false               true                                              allow-resource=true
$ sdm admin ssh update --id rs-xxxxxxxxxxxxxxx --delete-tags 'allow-resource'
changed 1 out of 1 matching datasource
```

Basically, you need to get the resource id and then add a tag with the name you've configured in `SDM_ALLOW_RESOURCE_TAG`. In the example above, we're assuming that `SDM_ALLOW_RESOURCE_TAG=allow-resource`. When this tag is configured only the resources with the tag value set to `true` will be displayed. In order to hide the resource, just delete the tag from it.

#### Hide Resource
```bash
$ sdm admin ssh list
Server ID               Name
rs-xxxxxxxxxxxxxxx     public-key-ssh
$ sdm admin ssh update --id rs-xxxxxxxxxxxxxxx --tags 'hide-resource='
changed 1 out of 1 matching datasource
$ sdm admin ssh list -e
Server ID               Name               Hostname                Port     Username           Port Override     Port Forwarding     Healthy     Secret Store ID     Egress Filter     Tags
rs-xxxxxxxxxxxxxxx     public-key-ssh     my-gw.example.com     2222     linuxserver.io     14760             false               true                                              hide-resource=
$ sdm admin ssh update --id rs-xxxxxxxxxxxxxxx --delete-tags 'hide-resource'
changed 1 out of 1 matching datasource
```

Basically, you need to get the resource id and then add a tag with the name you've configured in `SDM_HIDE_RESOURCE_TAG`. In the example above, we're assuming that `SDM_HIDE_RESOURCE_TAG=hide-resource`. In order to "unhide" the resource, just delete the tag.

From [AccessBot v1.0.3](https://github.com/strongdm/accessbot/releases/tag/1.0.3) the value of the tag is interpreted (see [here](https://github.com/strongdm/accessbot/issues/83)). You could use: `hide-resource=false` instead of deleting the tag. For more information about using tags please refer to the [documentation](https://www.strongdm.com/docs/automation/getting-started/tags).

#### User Roles
```bash
$ sdm admin users list
User ID                First Name     Last Name     Email                            Tags
a-xxx                  Firstname1     Lastname1     user1@example.com
a-yyy                  Firstname2     Lastname2     user2@example.com
$ sdm admin users update --email user1@example.com --tags 'sdm-roles="dev,prod"'
$ sdm admin users list
User ID                First Name     Last Name     Email                              Tags
a-xxx                  Firstname1     Lastname1     user1@example.com          sdm-roles="dev,prod"
a-yyy                  Firstname2     Lastname2     user2@example.com
$ sdm admin users update --email user1@example.com --delete-tags 'sdm-roles'
```

#### Allow Roles
```bash
$ sdm admin roles list
Role ID                Name             Composite     Tags
r-xxxxxxxxxxxxxxx      my-role          false         
r-xxxxxxxxxxxxxxx      another-role     false         
$ sdm admin roles update --tags allow-role=true my-role
$ sdm admin roles list
Role ID                Name             Composite     Tags
r-xxxxxxxxxxxxxxx      my-role          false         allow-role=true
r-xxxxxxxxxxxxxxx      another-role     false          
$ sdm admin roles update --delete-tags allow-role my-role
```

Basically, you need to add a tag with the name you've configured in `SDM_ALLOW_ROLE_TAG` to the roles you want to allow. In the example above, we're assuming that `SDM_ALLOW_ROLE_TAG=allow-role`. When this tag is configured only the roles with the tag value set to `true` will be displayed. In order to hide the role, just delete the tag from it.

IMPORTANT:
* Remember to separate values with commas
* Remember to enclose multiple values between double quotes (`"`)
