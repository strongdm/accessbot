# AccessBot
![GitHub release (latest by date)](https://img.shields.io/github/v/release/strongdm/accessbot)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/strongdm/accessbot/accessbot?label=tests)

AccessBot is a chatbot that manages access to strongDM (SDM) resources, initially via Slack

**Important**: This repo hosts two versions of AccessBot with the same set of funcionalities and corresponding documentation:
* v1.0.x ([branch](https://github.com/strongdm/accessbot/tree/1.0.x)). Uses the old Slack API (RTM) - _requires a Slack Classic App_
* v1.1.x ([main](https://github.com/strongdm/accessbot)). Uses the new Slack API (Bolt)

## Table of Contents
* [Installation](#installation)
* [Getting Started](#getting-started)
* [Contributing](#contributing)
* [Support](#support)

## Installation
In order to install AccessBot, you need to provide the following required variables:
* **SDM_BOT_PLATFORM**. The platform that the bot will be installed on, i.e. "ms-teams", "slack" or blank (which will be interpreted as Slack by default)
* **SDM_ADMINS**. List of admins, although it's not required, these users are usually SDM admins too 
  - For Slack platform: use the nick handles of all the admins
  - For MS Teams platform: use the email addresses of all the admins
* **SDM_API_ACCESS_KEY**. SDM API Access Key
* **SDM_API_SECRET_KEY**. SDM API Access Key Secret

### Slack Installation
For Slack platform, you need to provide the following required variables:
* **SLACK_APP_TOKEN**. Slack App-Level Token
* **SLACK_BOT_TOKEN**. Slack Bot User OAuth Token

### MS Teams Installation
For MS Teams platform, you need to provide the following required variables:
* **AZURE_APP_ID**. Azure Bot application ID
* **AZURE_APP_PASSWORD**. Azure Bot application password

For a full list of configuration variables please read: [Configure AccessBot](docs/CONFIGURE_ACCESSBOT.md)

Detailed instructions about how to configure Slack and SDM for AccessBot can be found here:
* [Configure Slack](docs/CONFIGURE_SLACK.md)
* [Configure SDM](docs/CONFIGURE_SDM.md)

For starting the bot enter all required variables in [docker-compose.yaml](docker-compose.yaml) and execute:
```
./docker-start.sh
```

The bot would start running in the background. In order to check logs.
```
docker logs accessbot_accessbot_1
```

If you want to install and execute the bot locally, please refer to: [Configure Local Environment](docs/CONFIGURE_LOCAL_ENV.md)

## Getting Started
Once AccessBot is up and running, you can add it as an app or to a channel and start using it!

First, check the bot and Slack interconnectivity state:

![image](docs/img/health-check.gif)

You would expect to see no error in your logs and the messages **Yes I am alive** and plugin available.

If that's the case, enter any of the following commands:
* `help`. Show available commands 
* `show available resources`. Show available resources - all or the ones assigned to a role
* `access to resource-name`. Grant temporary access to a resource
* `show available roles`. Show all roles
* `access to resource-name`. Grant temporary access to all resources assigned to a role

For example:

![image](docs/img/main-commands-tutorial.gif)

## Optional access configuration

1. Set `SDM_AUTO_APPROVE_ALL=true` to disable approval entirely.
2. Use the strongDM CLI or SDK to add the following tags to individual resources:
      - `SDM_AUTO_APPROVE_TAG=auto-approve` -- automatic approval for this resource
      - `SDM_ALLOW_RESOURCE_TAG=allow-resource` -- resource is displayed via `show` command; any access request auto-fails if the resource does not have the tag
      - `SDM_HIDE_RESOURCE_TAG=hide-resource` -- resource is not displayed via `show` command; any access request auto-fails

For more information, please refer to the [detailed guide for access configuration](docs/ACCESS_CONFIGURATION.md).

## Troubleshooting

A list of typical issues and resolutions can be found [here](docs/TROUBLESHOOTING.md).

## Contributing
In case you want to contribute to the project, please check our [guidelines](CONTRIBUTING.md).

## Support
In case you need support, please check our [Frequently Asked Questions](docs/FAQ.md) and [support](SUPPORT.md) documents.

