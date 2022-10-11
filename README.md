# AccessBot
![GitHub release (latest by date)](https://img.shields.io/github/v/release/strongdm/accessbot)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/strongdm/accessbot/accessbot?label=tests)

**IMPORTANT: The Slack Classic implementation has been deprecated. In case you're still using it, please migrate ASAP to the [Slack Bolt implementation](https://github.com/strongdm/accessbot/blob/main/docs/slack/CONFIGURE_SLACK.md).**

AccessBot is a chatbot that manages access to strongDM (SDM) resources through temporary grants. 
Some main features are: 
you can have a manual approval flow and an automated one for specific resources (or all of them if you want);
you can configure specific approvers for specific resources;
you can configure what resources can be requested, or hide specific ones; 
the users can specify the duration of the temporary grants and even the reason behind it.
The resources can also be accessed by role grants, which means that the user can request access to a role, and they will have temporary access to all resources from that role. 

AccessBot can be installed on Slack or MS Teams.

A curated version of the documentation can be found [here](https://strongdm.github.io/accessbot/).

You can also watch our [demo video](https://www.youtube.com/watch?v=LfsbXl0b3G8) of AccessBot on YouTube.

## Table of Contents
* [Configuration](#configuration)
* [Deploy](#deploy)
* [Getting Started](#getting-started)
* [Contributing](#contributing)
* [Support](#support)

## Configuration
In order to deploy AccessBot, first you need to define the following required environment variables:
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
* **AZURE_AD_TENANT_ID_**. Azure Active Directory Tenant ID

For a full list of configuration variables please read: [Configure AccessBot](docs/configure_accessbot/CONFIGURE_ACCESSBOT.md)

Detailed instructions about how to configure SDM and a platform (Slack, Slack Classic or MS Teams) for AccessBot can be found here:
* [Configure SDM](docs/configure_accessbot/CONFIGURE_SDM.md)
* [Configure Slack](docs/slack/CONFIGURE_SLACK.md)
* [Configure Slack Classic](docs/slack/CONFIGURE_SLACK_CLASSIC.md)
* [Configure MS Teams](docs/ms-teams/CONFIGURE_MS_TEAMS.md)


## Deploy

AccessBot is available as a Docker image. For deploying it we recommend you to use a container orchestrator, e.g. Kubernetes. Here's a [k8s deployment descriptor](k8s-descriptor.yaml) that you can use as a reference.

Most customers deploy AccessBot as a k8s deployment of *one* replica using the bot's [healthcheck endpoint](.), so the Orchestrator ensures that there's always an instance of the bot available. At the moment, the bot doesn't support load balancing nor slack webhooks. 

### Using disposable containers

If you're using technologies that dispose containers, e.g. [Fargate](https://aws.amazon.com/fargate/), and manual approvals, you should enable state handling via `SDM_ENABLE_BOT_STATE_HANDLING` to persist manual grant requests. Please refer to the [documentation](docs/configure_accessbot/CONFIGURE_ACCESSBOT.md#bot-configuration) for more details of this variable.

To make the persistency work in this scenario, you need to mount a folder pointing to the path `/errbot/data/grant_requests` inside the container. This folder will store the grant requests state, persisting the data while the containers are disposed and redeployed.

If you decide to deploy on Fargate and need some help, please refer to the [Fargate deployment docs](./docs/deploy/FARGATE.md).

### Run locally

#### Using Docker Compose

For starting the bot with [docker compose](https://docs.docker.com/compose/install/). 
Enter all required variables in the [docker-compose.yaml](docker-compose.yaml) file and execute:

```
docker compose build --no-cache 
docker compose up -d
```

Then, the bot should start running in the background. If you want to check the logs you can run the following command: 
```bash
$ docker logs accessbot_accessbot_1
```

#### Without Docker

If you want to install and execute the bot locally without Docker, please refer to: [Configure Local Environment](docs/CONFIGURE_LOCAL_ENV.md)
If you want to expose a Prometheus endpoint with AccessBot Metrics, please refer to [Configure Monitoring](docs/configure_accessbot/CONFIGURE_MONITORING.md)

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

NOTE: All AccessBot commands are case-insensitive.

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

