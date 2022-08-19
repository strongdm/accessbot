---
layout: default
title: Configure Slack(Classic)
nav_order: 3
parent: Slack
---

# Configure Slack Classic

## NOTE: The Slack Classic app version is no longer supported. Please use the default Slack version (Bolt)

In order to configure AccessBot integration with Slack follow the next steps:

1. Go to https://api.slack.com/apps?new_classic_app=1 and create a classic app

![image](https://user-images.githubusercontent.com/313803/115708663-936d2380-a370-11eb-94d2-b5edb1596af7.png)

2. Go to OAuth & Permissions and add bot scope in the Scopes 

![image](https://user-images.githubusercontent.com/313803/115709326-653c1380-a371-11eb-9346-f2fa81c7fd24.png)

IMPORTANT: The reason why you need a classic app and the bot scope, is because the current AccessBot implementation uses the RTM API, which is not available 
when updating to the new bot scopes. 

4. Go to App Home 

![image](https://user-images.githubusercontent.com/313803/115710249-6cafec80-a372-11eb-9071-bad38cf0d4bf.png)

5. Click Add Legacy Bot User and set its name

![image](https://user-images.githubusercontent.com/313803/115710432-a2ed6c00-a372-11eb-8fda-b8ef9c874e49.png)

6. Go to Install App 

![image](https://user-images.githubusercontent.com/313803/115710557-c6181b80-a372-11eb-95dd-72927c81e53a.png)


**Use "Bot User OAuth Token" for your _SLACK_TOKEN_ variable**

_Original instructions from [this thread](https://github.com/slackapi/python-slack-sdk/issues/609#issuecomment-6398872129)_
