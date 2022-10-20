# Frequently Asked Questions


## Can a user request and grant access to resources to themselves? (like in the gif)
Not really, what you see in the gif happens because the requester is the bot admin. The normal flow is actually what you’d expect: user x requests access, and users y or z (bot admins) approve.
You might want to take a look at the [ACCESS_CONFIGURATION](ACCESS_CONFIGURATION.md) - _specially the possible workflows_

## Is it possible to only allow a different person to approve than who requested?
Absolutely, it’s an independent config. Everyone can be a user. However, bot admins are configured at installation time via env variable (`SDM_ADMINS`) or via bot config at run time (`SDM_ADMINS_CHANNEL` or `SDM_APPROVERS_CHANNEL_TAG`)
 
## Where does the list of "available resources" populate from?
The resources you see and can request access to, are all the ones available in your account. That’s because the bot uses API Keys. You can restrict certain resources using tags setting the var `SDM_HIDE_RESOURCE_TAG` or you can hide all resources by enabling the var `SDM_ALLOW_RESOURCE_TAG` and adding the correspondent tag only to the resources that you want to show.
Besides, you can use `CONTROL_RESOURCES_ROLE_NAME` for listing only resources associated with a specific role. See [CONFIGURE_ACCESSBOT](configure_accessbot/CONFIGURE_ACCESSBOT.md)

## Can the bot send the approval requests to SDM admins via a Slack DM? Or only post to a channel?
You can do both, it’s configurable. Most of the users prefer to communicate with AccessBot through a channel and leave all messages there (as a log) 

## How can I invite AccessBot to my channel?
Just mention `@accessbot` in your channel

## How can I use AccessBot in a private channel?
Invite AccessBot to your private channel and add the scope `usergroups:read` to your bot

## How can I get my AccessBot version?
Send the following direct message to the Bot: `plugin config AccessBot`
