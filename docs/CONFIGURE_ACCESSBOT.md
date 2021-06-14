# Configure AccessBot

There are a number of variables you can use for configuring AccessBot.

## Required configuration
* **SLACK_TOKEN**. Slack Bot User OAuth Token
* **SDM_ADMINS**. List of Slack admins, format: `@usernick`. Although it's not required, these users are often SDM admins too. You could use `whoami` for getting user nicks. 
* **SDM_API_ACCESS_KEY**. SDM API Access Key
* **SDM_API_SECRET_KEY**. SDM API Access Key Secret

## Internal configuration
* **LOG_LEVEL**. Logging level. Default = INFO
* **SDM_DOCKERIZED**. Logging type. Default = true (_when using docker_), meaning logs go to STDOUT
* **SDM_COMMANDS_ENABLED**. AccessBot commands to be enabled. Default = access_resources assign_role show_resources show_roles

## Bot configuration
The following variables can be changed at runtime via slack -by an SDM_ADMIN- using the `plugin config AccessBot` command:
* **SDM_ADMIN_TIMEOUT**. Timeout in seconds for a request to be manually approved. Default = 30 sec
* **SDM_SENDER_NICK_OVERRIDE**. Nickname to be used for all requests. Default = None (_useful for testing_)
* **SDM_SENDER_EMAIL_OVERRIDE**. Email to be used for all requests. Default = None (_useful for testing_)
* **SDM_AUTO_APPROVE_ALL**. Flag to enable auto-approve for all resources. Default = false
* **SDM_AUTO_APPROVE_TAG**. Tag to be used for auto-approve resources. The tag value is ignored, delete tag to disable. Default = None
* **SDM_HIDE_RESOURCE_TAG**. Tag to be used for hidden resources. The tag value is ignored, delete tag to disable. Default = None
* **SDM_GRANT_TIMEOUT**. Timeout in minutes for an access grant. Default = 60 min
* **CONTROL_RESOURCES_ROLE_NAME**. Role name to be used for getting available resources. Default = None
* **SDM_ADMINS_CHANNEL**. Channel name to be used by administrators for approval messages, for example: `#accessbot-private` (important to start with `#`). Default = None

See image below for more information:

![image](img/bot-config.gif)

### Some tricks
* Use `plugin config AccessBot {}` for setting config to initial state. This command needs to be executed in a direct chat with AccessBot, cannot be used in channels
* Use `plugin info AccessBot` for showing all configurations
* Use `whoami` for showing user configuration. Use the `nick` field for the `SDM_ADMINS` variable

### Known issues
* When using `plugin config` from a Mac, you will need to disable: 
`System Preferences > Keyboard > Text > Uncheck "Use smart quotes and dashes`. The `config` command fails to understand quotes as unicode characters.
