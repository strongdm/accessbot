# AccessBot
![GitHub release (latest by date)](https://img.shields.io/github/v/release/strongdm/accessbot)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/strongdm/accessbot/accessbot?label=tests)

AccessBot is a chatbot that manages access to strongDM (SDM) resources through temporary grants. 
Some main features are: 
you can have a manual approval flow and an automated one for specific resources (or all of them if you want);
you can configure specific approvers for specific resources;
you can configure what resources can be requested, or hide specific ones; 
the users can specify the duration of the temporary grants and even the reason behind it.
The resources can also be accessed by role grants, which means that the user can request access to a role, and they will have temporary access to all resources from that role. 

AccessBot can be installed on Slack or MS Teams.

A curated version of the documentation can be found [here](https://strongdm.github.io/accessbot/).

## Table of Contents
* [Installation](#installation)
* [Getting Started](#getting-started)
* [Contributing](#contributing)
* [Support](#support)

## Installation
In order to install AccessBot, first you need to define the following required environment variables:
* **SDM_BOT_PLATFORM**. The platform that the bot will be installed on, i.e. "ms-teams", "slack" or blank (which will be interpreted as Slack by default)
* **SDM_ADMINS**. List of admin users who will manage the bot and approve grant requests (by default).
  - For Slack platform: use the `username` (not Display Name) of each admin, e.g. `@user1 @user2` (See this [section](docs/TROUBLESHOOTING.md#getting-slack-usernames) for more.)
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

For a full list of configuration variables please read: [Configure AccessBot](docs/configure_accessbot/CONFIGURE_ACCESSBOT.md)

Detailed instructions about how to configure SDM and a platform (Slack, Slack Classic or MS Teams) for AccessBot can be found here:
* [Configure SDM](docs/configure_accessbot/CONFIGURE_SDM.md)
* [Configure Slack](docs/slack/CONFIGURE_SLACK.md)
* [Configure Slack Classic](docs/slack/CONFIGURE_SLACK_CLASSIC.md)
* [Configure MS Teams](docs/teams/CONFIGURE_MS_TEAMS.md)

For starting the bot we'll use [docker-compose](https://docs.docker.com/compose/install/). 
Enter all required variables in the [docker-compose.yaml](docker-compose.yaml) file and execute:
```
docker-compose build --no-cache 
docker-compose up -d
```

The bot should start running in the background. And if you want to check the logs you can run the following command: 
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
* `show available resources [--filter expression]`. Show available resources - all or a filtered subset. Filters are optional. 
Please refer to the following [doc](https://www.strongdm.com/docs/automation/getting-started/filters) for getting the list of available filters.
* `access to resource-name [--reason text] [--duration duration]`. Grant temporary access to a resource. Reason and Duration are optional.
* `show available roles`. Show all available roles*
* `access to resource-name`. Grant temporary access to all resources assigned to a role

NOTE: all AccessBot commands are case-insensitive.

For example:

![image](docs/img/main-commands-tutorial.gif)

## Optional access configuration
Here are some of the most used variables:

1. Set `SDM_AUTO_APPROVE_ALL=true` to disable approval entirely.
2. Use the strongDM CLI or SDK to add the following tags to individual resources:
      - `SDM_AUTO_APPROVE_TAG=auto-approve` -- automatic approval for this resource
      - `SDM_ALLOW_RESOURCE_TAG=allow-resource` -- resource is displayed via `show` command; any access request auto-fails if the resource does not have the tag
      - `SDM_HIDE_RESOURCE_TAG=hide-resource` -- resource is not displayed via `show` command; any access request auto-fails
3. Use the strongDM CLI or SDK to add the following tags to individual roles:
      - `SDM_AUTO_APPROVE_ROLE_TAG=auto-approve` -- automatic approval for this role
      - `SDM_ALLOW_ROLE_TAG=allow-role` -- role is displayed via `show` command; any access request auto-fails if the role does not have the tag

For more information and a full list of variables, please refer to the [detailed guide for access configuration](docs/configure_accessbot/ACCESS_CONFIGURATION.md).

## Troubleshooting

A list of typical issues and resolutions can be found [here](docs/TROUBLESHOOTING.md).

## Contributing
In case you want to contribute to the project, please check our [guidelines](CONTRIBUTING.md).

## Support
In case you need support, please check our [Frequently Asked Questions](docs/FAQ.md) and [support](SUPPORT.md) documents.

