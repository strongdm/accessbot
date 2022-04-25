---
title: Teams Accessbot How-to
nav_order: 10
parent: Teams
layout: default
---
# Access bot (GitHub)

## Creating yourAzure Bot

1. Create the AccessBot resource in the [Azure Portal](https://portal.azure.com/) by adding an “Azure Bot” resource
2. On the creation page, change the “type of app” to Multi Tenant as this is what create the secret already generated in the key store that is created along side the Azure bot.

![Create Bot](https://user-images.githubusercontent.com/6556218/157345332-c2137703-0978-4b12-ae6f-67ee875f0caa.png)


3. Get the App ID from the “Configuration” blade of the Azure bot. The Microsoft App ID is listed there. Store this in your notes as we will need it once we configure the AccessBot server.

![App ID](https://user-images.githubusercontent.com/6556218/157345362-dbaa80e9-6ef1-4c62-ba93-78c5266312c8.png)

4. After your bot is created go to “[key vaults](https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.KeyVault%2Fvaults)” to to get the secret. This can be found by searching for Key Vault in the main search bar. Your newly created vault will be there with a random name. Look for one in the same security group that you selected when creating the Azure bot.
5. We need to add ourselves to the vault to gain permissions to see the secret. Select Access policies, and add a policy with yourself having at least List and Get permissions for secrets.

![Key Vault Permissions](https://user-images.githubusercontent.com/6556218/157345405-6b960b35-91e2-4bd3-84f3-ed60913afe69.png)

6. Then select on Secrets blade, then current version, and lastly the show secret value button to to get the key. Store it somewhere safe as we will need it when confiuring AccessBot on the server.


![Secret](https://user-images.githubusercontent.com/6556218/157345456-cee10d78-9dd6-4a6b-a6c7-a3b91525048a.png)


### Add MS Teams to Azure bot Channels

7. On the Channels blade of your Azure bot, add ms-teams as an approved channel.

![Channels Add Teams](https://user-images.githubusercontent.com/6556218/157345481-017e4317-ed2f-4fb7-820d-8cf59e5d625b.png)

## Acessbot Server

Acessbot is run via a docker iamge using docker-compose. You will also need Nginx on this server to serve as the webhook/reverse proxy. Other server and website configurations are possible but this is the easiest to manage.

8. Use the [env-file.example](https://github.com/strongdm/accessbot/blob/main/env-file.example) file to configure the settings for AccessBot. Below you will see an example for MS teams. Modify the file with your data; the API key, platform to ms-teams, put in the Azure app ID and password we stored from earlier steps.

```bash
# You can copy this file as "env-file" for your docker-compose
# IMPORTANT: Do not enclose values in double or single quotes 

# ------------------------------------------------------------------------------
# |                           GENERAL ENV VARS                                 |
# ------------------------------------------------------------------------------
# These vars are required for any SDM_BOT_PLAFORM.

SDM_BOT_PLATFORM=ms-teams # possible values: slack, slack-classic, ms-teams
SDM_API_ACCESS_KEY=YourAccessKeyFromSDM
SDM_API_SECRET_KEY=YourSecretKeyFromSDM

# ------------------------------------------------------------------------------
# |                            MS-TEAMS ENV VARS                               |
# ------------------------------------------------------------------------------
# You need to use the following vars when SDM_BOT_PLATFORM var is "ms-teams":

SDM_ADMINS=shane@strongdm.com
AZURE_APP_ID=YourAzureAppID
AZURE_APP_PASSWORD=YourAzureKeyStoreSecret

# ------------------------------------------------------------------------------
# |                              OPTIONAL VARS                                 |
# ------------------------------------------------------------------------------
# See: docs/CONFIGURE_ACCESSBOT.md
# Other variables you want to set at run time.
SDM_ADMIN_TIMEOUT=90
SDM_GRANT_TIMEOUT=90
#Useful when troubleshooting
#LOG_LEVEL=DEBUG
```

9. Install docker
10. Install docker-compose
11. Create the docker-compose.yaml

```jsx
version: "3.9"
services:
   accessbot:
     image: public.ecr.aws/strongdm/accessbot:latest
     env_file:
       # You could use env-file.example as a reference
       - env-file
     ports:
       - 3141:3141
     restart: always
```

12. Start the app with `docker-compose up`
   a. This will show logging which is helpful during initial setup. Once you are happy with the deployment use `docker-compose up -d` to run the app in the background. You can also turn on debug in the logs via the env-file settings if further troubleshooting is needed.

## Messaging Endpoint Creation

13. [Install ngnix](https://ubuntu.com/tutorials/install-and-configure-nginx#1-overview) (this example is for Ubuntu options will vary depending on host OS)
14. Copy default file in /etc/nginx/sites-enabled to have a backup, then modify default site to be have this configuration.
15. Note after making changes to the config file restart the nginx service

```jsx
server {
    server_name yourDNSNameorIPhere.com;

    location / {
            proxy_pass http://127.0.0.1:3141;
    }

}
```

16. Setup your site to be a valid HTTPS server. [Follow steps here to get certbot setup for HTTPS traffic](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal) (example output below)

![Certbot Verified](https://user-images.githubusercontent.com/6556218/157345912-d8937d94-a95f-49d3-95ff-38950e21db7c.png)

## Generate / Register App

17. Create an App ID via online tool like [UUID Gen](https://www.uuidgenerator.net/version1)

```bash
47799de2-98f6-11ec-b909-0242ac120002
```

18. Put that ID into the [manifest.json](https://github.com/strongdm/accessbot/blob/main/ms-teams/app/manifest.json#L5) see example below

```json
{
    "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.11/MicrosoftTeams.schema.json",
    "manifestVersion": "1.11",
    "version": "1.0.0",
    "id": "YOUR-GENERATED-UUID-ID",
    "packageName": "com.strongdm.teams.app",
    "developer": {
        "name": "strongDM",
        "websiteUrl": "https://strongdm.com",
        "privacyUrl": "https://privacy.microsoft.com/en-ca/privacystatement",
        "termsOfUseUrl": "https://privacy.microsoft.com/en-ca/privacystatement"
    },
    "icons": {
        "color": "color.png",
        "outline": "outline.png"
    },
    "name": {
        "short": "AccessBot",
        "full": ""
    },
    "description": {
        "short": "Accessbot is a chatbot that manages access to strongDM resources",
        "full": "Accessbot is a chatbot that manages access to strongDM resources"
    },
    "accentColor": "#FFFFFF",
    "staticTabs": [
        {
            "entityId": "conversations",
            "scopes": [
                "personal"
            ]
        },
        {
            "entityId": "about",
            "scopes": [
                "personal"
            ]
        }
    ],
    "bots": [
        {
            "botId": "YOUR-MICROSOFT-BOT-ID",
            "scopes": [
                "personal",
                "team",
                "groupchat"
            ],
            "supportsFiles": false,
            "isNotificationOnly": false
        }
    ],
    "permissions": [
        "identity",
        "messageTeamMembers"
    ],
    "validDomains": []
}
```

19. Take the [icons and manifest file](https://github.com/strongdm/accessbot/tree/main/ms-teams/app) you just modifed and zip them up. This is now your AccessBot app to be submitted into your MS Teams environment.

### Getting your App into Teams

20. Upload the app.zip file to [register the app](https://admin.teams.microsoft.com/) in your Org
21. Log into MS teams, and then go to Apps —> Manage your apps —> Submit an app to your org.

![Upload your Zip/App](https://user-images.githubusercontent.com/6556218/157347518-ee5434ec-a0b2-45f6-a5ef-8e10a77752d6.png)

22. Attached the zip file above.
23. Message your IT team to approve the application submission.
24. Add the AccessBot App to your individual team

![Manage AccessBot](https://user-images.githubusercontent.com/6556218/157347688-3015c400-2762-476a-b740-984c553c794e.png)

25. Use “@AccessBot help “to get a list of the available commands

![AccessBot Commands](https://user-images.githubusercontent.com/6556218/157347756-fbd58d83-b746-43cf-ae04-5b740b930b74.png)

## Limitations

- Admins channel: it is not possible to add an application inside a private channel. Because of that, the bot will communicate with all the administrators via direct messages.
- Request access commands via direct messages (DM): it is not possible to send messages to the admins when the bot receives a message via DM, therefore all the commands that request access are disabled via DM.
