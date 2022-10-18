---
layout: default
title: AccessBot Environment Variables
nav_order: 4
parent: Accessbot Configuration
---
# Configure AccessBot

There are a number of variables you can use for configuring AccessBot. Here you will find the complete list of environment variables that you can use, and some of them can be changed at runtime (see the [Bot configuration](#bot-configuration) section below).

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
* **AZURE_APP_ID**. Azure Bot application ID
* **AZURE_APP_PASSWORD**. Azure Bot application password
* **AZURE_AD_TENANT_ID_**. Azure Active Directory Tenant ID

## Internal configuration
* **LOG_LEVEL**. Logging level. Default = INFO
* **SDM_DOCKERIZED**. Logging type. Default = true (_when using docker_), meaning logs go to STDOUT
* **SDM_COMMANDS_ENABLED**. AccessBot commands to be enabled. Default = `access_resource assign_role show_resources show_roles approve deny`. You could also specify aliases for specific commands. In that case, only add `:alias` after the command name, for example: `access_resource:acres show_resources:sares`.

## Bot configuration
The following variables can be changed at runtime via Slack or MS Teams -by a bot admin- using the `plugin config AccessBot {}` command.
You just need to remove the "SDM_" prefix when configuring them. Here's a usage example of the command: `plugin config AccessBot {'ADMINS_CHANNEL': '#my-channel', 'ADMIN_TIMEOUT': 60}`.

* **SDM_ADMIN_TIMEOUT**. Timeout in seconds for a request to be manually approved. Default = 30 sec
* **SDM_ADMINS_CHANNEL**. Channel name to be used by administrators for approval messages. Disabled by default. See the following usage examples:
  - For Slack: `SDM_ADMINS_CHANNEL=#accessbot-private`, the value needs to start with a `#` symbol, i.e., the channel name needs to come after a `#` symbol.
  - For MS Teams: `SDM_ADMINS_CHANNEL=Admin Team###Admin Channel`, the team and the channel name must be separated by `###`. If you want to use the default channel (General) of a team, you only need to define the team name, e.g., `SDM_ADMINS_CHANNEL=Admin Team`.
    - **IMPORTANT**: in order to enable this feature on MS Teams, you'll need to [configure Azure Active Directory](/docs/ms-teams/CONFIGURE_AZURE_ACTIVE_DIRECTORY.md).
* **SDM_ADMINS_CHANNEL_ELEVATE**. Boolean flag to allow usage of admin commands to all users inside the configured SDM_ADMINS_CHANNEL. When this is enabled the admin commands can no longer be sent via DM, only via the configured channel. Default = false
* **SDM_ALLOW_RESOURCE_ACCESS_REQUEST_RENEWAL**. Flag to enable renewal of resource account grants. When enabled allows a user to make a new access request to a resource even if they already have access to it. Default = false
* **SDM_ALLOW_RESOURCE_TAG**. Resource tag to be used for only showing the allowed resources. Ideally set the value to `true` or `false` (e.g. `allow-resource=true`). When there's no tag assigned, all resources are allowed (default behavior). Disabled by default ([see below](#using-tags) for more info about using tags)
* **SDM_ALLOW_RESOURCE_GROUPS_TAG**. Resource tag to be used for only showing the allowed resources to the configured allowed user groups. The tag value should be the list of allowed user groups (see `SDM_GROUPS_TAG`) for that resource separated by comma. If this tag or the `SDM_GROUPS_TAG` is not configured, all resources are allowed (default behavior). Disabled by default ([see below](#Allow-Resource-By-Groups) for more info about using tags)
* **SDM_ALLOW_ROLE_TAG**. Role tag to be used for only showing the allowed roles. Ideally set the value to `true` or `false` (e.g. `allow-role=true`). When there's no tag assigned, all roles are allowed (default behavior). Disabled by default ([see below](#using-tags) for more info about using tags)
* **SDM_ALLOW_ROLE_GROUPS_TAG**. Role tag to be used for only showing the allowed roles to the configured allowed user groups. The tag value should be the list of allowed user groups (see `SDM_GROUPS_TAG`) for that role separated by comma. If this tag or the `SDM_GROUPS_TAG` is not configured, all resources are allowed (default behavior). Disabled by default ([see below](#Allow-Role-By-Groups) for more info about using tags)
* **SDM_APPROVERS_CHANNEL_TAG**. Resource/Account tag to be used for specifying the responsible approvers channel name for individual resources or accounts. Disabled by default. See the following usage examples:
  - For Slack: `SDM_APPROVERS_CHANNEL_TAG=approvers-channel` and inside the tags of a resource we would have `approvers-channel=#resource-approvers`, in this scenario all access requests for that resource would be sent only to the `#resource-approvers` Slack channel. In another case, if an account is tagged with `approvers-channel=#account-approvers`, all access requests from that user would go to the `#account-approvers` Slack channel.
  - For MS Teams: `SDM_APPROVERS_CHANNEL_TAG=approvers-channel` and inside the tags of a resource we would have `approvers-channel=Approvers Team###Approvers Channel`, in this scenario all access requests for that resource would be sent only to the `Approvers Channel` Teams channel. Note that in the tag value the team and the channel name must be separated by `###`. If you want to use the default channel (General) of a team, you only need to define the team name, e.g., `approvers-channel=Approvers Team`.
* **SDM_AUTO_APPROVE_ALL**. Flag to enable auto-approve for all resources. Default = false
* **SDM_AUTO_APPROVE_GROUPS_TAG**. Resource tag to be used for auto-approve groups. The tag value should be a list of groups (see `SDM_GROUPS_TAG`) separated by comma. Disabled by default
* **SDM_AUTO_APPROVE_ROLE_ALL**. Flag to enable auto-approve for all roles. Default = false
* **SDM_AUTO_APPROVE_ROLE_TAG**. Role tag to be used for auto-approve roles. The tag value is not ignored, delete tag or set it false to disable. Disabled by default
* **SDM_AUTO_APPROVE_TAG**. Resource tag to be used for auto-approve resources. The tag value is not ignored, delete tag or set it false to disable. Disabled by default
* **SDM_CONCEAL_RESOURCE_TAG**. Resource tag to be used for concealing resources, meaning that they are not going to be shown but remain accessible. Ideally set value to `true` or `false` (e.g. `conceal-resource=true`). If there's no value, it's interpreted as `true`. Disabled by default ([see below](#using-tags) for more info about using tags)
* **SDM_CONTROL_RESOURCES_ROLE_NAME**. Role name to be used for getting available resources. Disabled by default
* **SDM_EMAIL_SLACK_FIELD**. Slack Profile Tag to be used for specifying an SDM email. For further information, please refer to [CONFIGURE_ALTERNATIVE_EMAILS.md](./CONFIGURE_ALTERNATIVE_EMAILS.md).
* **SDM_EMAIL_SUBADDRESS**. Flag to be used for specifying a subaddress for the SDM email (e.g. "user@email.com" becomes "user+sub@email.com" when SDM_EMAIL_SUBADDRESS equals to "sub"). Disabled by default
* **SDM_ENABLE_BOT_STATE_HANDLING**. Boolean flag to enable persistent grant requests. When enabled, all grant requests will be synced in a local file, that way if AccessBot goes down, all ongoing requests will be restored. Default = false
* **SDM_ENABLE_RESOURCES_FUZZY_MATCHING**. Flag to enable fuzzy matching for resources when a perfect match is not found. Default = true
* **SDM_GRANT_TIMEOUT**. Timeout in minutes for an access grant. Default = 60 min
* **SDM_GRANT_TIMEOUT_LIMIT**. Timeout limit in minutes for an access grant when using the `--duration` flag. Disabled by default
* **SDM_GROUPS_TAG**. User tag to be used for specifying the groups a user belongs to. Disabled by default ([see below](#user-groups) for more info about using tags)
* **SDM_HIDE_RESOURCE_TAG**. Resource tag to be used for hiding available resources, meaning that they are not going to be shown nor accessible. Ideally set value to `true` or `false` (e.g. `hide-resource=true`). If there's no value, it's interpreted as `true`. Disabled by default ([see below](#using-tags) for more info about using tags)
* **SDM_HIDE_ROLE_TAG**. Role tag to be used for hiding available roles, meaning that they are not going to be shown nor accessible. Ideally set value to `true` or `false` (e.g. `hide-role=true`). If there's no value, it's interpreted as `true`. Disabled by default ([see below](#using-tags) for more info about using tags)
* **SDM_MAX_AUTO_APPROVE_USES** and **SDM_MAX_AUTO_APPROVE_INTERVAL**. Max number of times that the auto-approve functionality can be used in an interval of configured minutes. Disabled by default
* **SDM_REQUIRED_FLAGS**. List of flags that should be required when using the "access" command. The flags should be separated by space, e.g. `reason duration`. By default, there are no required flags
* **SDM_RESOURCE_GRANT_TIMEOUT_TAG**. Resource tag to be used for registering the custom time (in minutes) that a specific resource will be made available for the user.
* **SDM_SENDER_EMAIL_OVERRIDE**. Email to be used for all requests. Disabled by default (_useful for testing_)
* **SDM_SENDER_NICK_OVERRIDE**. Nickname to be used for all requests. Disabled by default (_useful for testing_)
* **SDM_USER_ROLES_TAG**. User tag to be used for controlling the roles a user can request. Disabled by default

NOTE: you need to remove the "SDM_" prefix from the variable name when using `plugin config`.

See image below for more information:

![image](../img/bot-config.gif)

### Some tricks
* Use `plugin config AccessBot {}` for setting config to initial state. This command can be executed in a direct chat with AccessBot or in the `SDM_ADMINS_CHANNEL` if `SDM_ADMINS_CHANNEL_ELEVATE` is enabled
* Use `plugin info AccessBot` for showing all configurations, including remaining auto-approve uses
* Use `whoami` for showing user configuration. Use the `nick` field for the `SDM_ADMINS` variable

NOTE: In the whoami command, the email field will show you the email that will be used in all your requests, but this value can change according to your configuration, e.g. defining the `SDM_SENDER_EMAIL_OVERRIDE`, `SDM_EMAIL_SLACK_FIELD` and/or `SDM_EMAIL_SUBADDRESS`.

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

#### Allow Resource By Groups
```bash
$ sdm admin ssh list
Server ID               Name
rs-xxxxxxxxxxxxxxx     public-key-ssh
$ sdm admin ssh update --id rs-xxxxxxxxxxxxxxx --tags 'allow-groups=my-group'
changed 1 out of 1 matching datasource
$ sdm admin ssh list -e
Server ID               Name               Hostname                Port     Username           Port Override     Port Forwarding     Healthy     Secret Store ID     Egress Filter     Tags
rs-xxxxxxxxxxxxxxx     public-key-ssh     my-gw.example.com     2222     linuxserver.io     14760             false               true                                              allow-groups=my-group
$ sdm admin ssh update --id rs-xxxxxxxxxxxxxxx --delete-tags 'allow-groups'
changed 1 out of 1 matching datasource
```

In order to configure the resource properly, you need to get the resource id and then add a tag with the name you've configured in `SDM_ALLOW_RESOURCE_GROUPS_TAG`. The tag value should be a list, separated by comma, of user groups that should be able to see and request access to that resource.

In the example above, we're assuming that `SDM_ALLOW_RESOURCE_GROUPS_TAG=allow-groups`. If a user from the group `my-group` requests access to the resource `public-key-ssh`, they will have no problem. But if another user from another group requests access to that same resource, they will get an error instead. 

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

#### User Groups

```bash
$ sdm admin users list
User ID                First Name         Last Name        Email                  Tags
a-xxxxxxxxxxxxxxxx     John               Doe              user@email.com
$ sdm admin users update --id a-43346ba36140a424 --tags "groups=dev,test"
$ sdm admin users list
User ID                First Name         Last Name        Email                  Tags
a-xxxxxxxxxxxxxxxx     John               Doe              john@email.com         groups=dev,test
$ sdm admin users update --id a-43346ba36140a424 --delete-tags groups
```

In this example we're assuming that `SDM_GROUPS_TAG=groups`. In the second command we added our user to 2 groups: "dev" and "test". And in the final command we removed all groups from our user.

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

#### Allow Role By Groups
```bash
$ sdm admin roles list
Role ID                Name             Composite     Tags
r-xxxxxxxxxxxxxxx      my-role          false         
r-xxxxxxxxxxxxxxx      another-role     false         
$ sdm admin roles update --tags allow-groups=my-group my-role
$ sdm admin roles list
Role ID                Name             Composite     Tags
r-xxxxxxxxxxxxxxx      my-role          false         allow-groups=my-group
r-xxxxxxxxxxxxxxx      another-role     false          
$ sdm admin roles update --delete-tags allow-groups my-role
```

In order to configure the role properly, you need to add a tag with the name you've configured in `SDM_ALLOW_ROLE_GROUPS_TAG` to the roles you want to allow. The tag value should be a list, separated by comma, of user groups that should be able to see and request access to that role.

In the example above, we're assuming that `SDM_ALLOW_ROLE_GROUPS_TAG=allow-groups`. If a user from the group `my-group` requests access to the role `my-role`, they will have no problem. But if another user from another group requests access to that same role, they will get an error instead. 

## Resources access request form bot configuration

* **SDM_ACCESS_FORM_BOT_NICKNAME**. Nickname of the access form bot. For further information, please refer to [CONFIGURE_ACCESSBOT_FORM.md](../slack/CONFIGURE_ACCESSBOT_FORM.md).
