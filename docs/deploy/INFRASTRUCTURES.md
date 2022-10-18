# Deployment Infrastructures

AccessBot has different Infrastructures depending on the Platform you want to use.

## Slack

When using Slack, AccessBot opens a Socket Connection to communicate with Slack, as you can see in the diagram below:

<img src="https://user-images.githubusercontent.com/49597325/196509052-563074d2-54ec-47f2-9b1f-9fa955e4f8fd.png" height="600px" />

## MS Teams

When using MS Teams, AccessBot needs to expose an endpoint on port 3141 that Azure is going to hit whenever there is a user request. After that, AccessBot uses the Teams API (BotFramework API) to send messages. This communication you can see in the diagram below:

<img src="https://user-images.githubusercontent.com/49597325/196511762-57c30642-59e1-48e7-802c-db50f8bea590.png" height="500px" />

## General Characteristics

Putting aside the platform you want to use, there are some points you need to pay attention:

1. AccessBot needs an ingress port on 3141 for health checks
2. AccessBot needs an ingress port on 3142 for monitoring metrics
