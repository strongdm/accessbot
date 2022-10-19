# Deployment Infrastructures

AccessBot has different Infrastructures depending on the Platform you want to use.

## Slack

When using Slack, AccessBot uses [Slack Socket Mode](https://api.slack.com/apis/connections/socket) to communicate with Slack, as you can see in the diagram below:

<img src="https://user-images.githubusercontent.com/49597325/196509052-563074d2-54ec-47f2-9b1f-9fa955e4f8fd.png" height="600px" />

Because of that, AccessBot doesn't support Load Balancing. And doesn't support [Slack Incomming Webhooks](https://api.slack.com/messaging/webhooks).

In this scenario, for basic operations you don't need to configure any ingress rule.

## MS Teams

When using MS Teams, AccessBot needs to expose an endpoint on port 3141 that Azure is going to hit whenever there is a user request. After that, AccessBot uses the Teams API ([BotFramework API](https://learn.microsoft.com/en-us/azure/bot-service/rest-api/bot-framework-rest-overview?view=azure-bot-service-4.0)) to send messages. This communication you can see in the diagram below:

<img src="https://user-images.githubusercontent.com/49597325/196511762-57c30642-59e1-48e7-802c-db50f8bea590.png" height="500px" />

## General Characteristics

Putting aside the platform you want to use, there are some points you need to pay attention to:

1. AccessBot has an endpoint on port 3141 that you can use for checking the health status: `http://localhost:3141/health-check`
2. AccessBot needs an ingress port on 3142 for monitoring metrics
