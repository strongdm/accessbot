# AccessBot

AccessBot is a chatbot that manages access to strongDM (SDM) resources, initially via Slack

## Table of Contents
* [Installation](#installation)
* [Getting Started](#getting-started)
* [Contributing](#contributing)
* [Support](#support)

## Installation
In order to install AccessBot you need to provide -at least- the following required variables:
* **SLACK_TOKEN**. Slack Bot User OAuth Token
* **SDM_ADMINS**. List of Slack admins, although it's not required, this users are usually SDM admins too  
* **SDM_API_ACCESS_KEY**. SDM API Access Key
* **SDM_API_SECRET_KEY**. SDM API Access Key Secret

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

![image](https://user-images.githubusercontent.com/313803/115704509-bf39da80-a36b-11eb-8bc1-07f2958679d0.png)

You would expect to see no error in your logs (see command above) and the message **Yes I am alive**. If that's the case, enter any of the available commands:
* `help`. Show available commands help
* `show available resources`. Show all available resources
* `access to resource-name`. Grant access to a resource (using the requester's email address)

For example:

![image](https://user-images.githubusercontent.com/313803/115705178-864e3580-a36c-11eb-8696-f100ad70d55c.png)

You can find detailed instructions for the main available commands:
* [Show Resources](docs/COMMAND_SHOW_RESOURCES.md)
* [Access](docs/COMMAND_ACCESS.md)

A list of typical issues and resolutions can be found [here](docs/TROUBLESHOOTING.md).

## Contributing
In case you want to contribute to the project, please check our [guidelines](CONTRIBUTING.md).

## Support
In case you need support, please check our [support](CONTRIBUTING.md) document.
