# Configure MS Teams

In order to configure AccessBot integration with Microsoft Teams, follow the next steps:

## Create Azure Bot

1. Go to [Create a Resource](https://portal.azure.com/#create/hub) page on Microsoft Azure, search and click in the `Azure Bot` option:

![screenshot-1](https://user-images.githubusercontent.com/49597325/190436698-601d0252-8f48-4be0-8bea-bf97538365e4.png)

2. When the `Create an Azure Bot` page loads, define your `Bot handle`, `Resource Group` and define the `Type of App` as "Multi Tenant" (as defined in the screenshot below):

![screenshot-2](https://user-images.githubusercontent.com/49597325/190436895-99fdffa5-f01d-4d9a-882c-00be39023e9d.png)

3. You can go to the next step and define the tags as you prefer. Then, go to the final step ("Review + create") and click on "Create":

![screenshot-3](https://user-images.githubusercontent.com/49597325/190437280-9e42b4b0-a081-44fc-808e-bd4145e463ad.png)

4. After the creation of the Azure Bot finishes, go to the created Azure Bot resource page, click in the configuration tab and fill the `Messaging Endpoing` field with a valid endpoint to AccessBot, then click on the `Apply` button:

![screenshot-4](https://user-images.githubusercontent.com/49597325/190437585-1676d97a-6339-4706-b1c2-645845d5a656.png)

**NOTE**: The endpoint must finish with `/botframework`.

5. Copy the `Microsoft App ID` and save it as the `AZURE_APP_ID` and then click on the `Manage` link button:

![screenshot-5](https://user-images.githubusercontent.com/49597325/190438583-7382b2cf-0b2e-4ee6-9476-6638a0bdc188.png)

6. On the `Certificates & Secrets` tab show should see an already created `Client Secret` with a hided Value. This value is our `AZURE_APP_PASSWORD`. If you don't have access to the full value, click on the `New client secret` button:

![screenshot-6](https://user-images.githubusercontent.com/49597325/190439055-c85ee998-b8d0-418f-96b5-d09574258519.png)

7. A form in a side bar will appear to create a new client secret. Define a description to the new and a expire time if you want to and then click on the `Add` button:

![screenshot-7](https://user-images.githubusercontent.com/49597325/190439658-2f4fa522-6872-4470-aaeb-fb397a610522.png)

8. After it finishes, you should be able to see the value of the created `Client Secret`. Copy this one and save it as the `AZURE_APP_PASSWORD`.

9. Go back to the create Azure Bot resource page, click on the `Channels` tab and then click on the `Microsoft Teams` application:

![screenshot-8](https://user-images.githubusercontent.com/49597325/190440440-adb0d234-e48d-454b-a0a2-6e013b5f0978.png)

10. A dialog will appear to ask you about the terms of service related to Microsoft Teams. To continue you need to aggree checking the `I Agree...` box and then clicking on the `Aggree` button:

![screenshot-9](https://user-images.githubusercontent.com/49597325/190440728-d6533b00-07c0-4d02-8bc0-03021d815b98.png)

11. On the Microsoft Teams application page, you need to select the `Microsoft Teams Commercial (most common)` option and then click on the `Apply` button:

![screenshot-10](https://user-images.githubusercontent.com/49597325/190441039-72546561-8d0e-4ca2-b64d-634bbaf8ea8e.png)

And now we can use AccessBot in Microsoft Teams via DMs. In the following section we'll configure the bot to use into the Microsoft Teams Organization.

**NOTE**: If you're passing environment variables via shell, ensure that you eclose the `AZURE_APP_PASSWORD` value between single quotes!

## Start the bot

Start accessbot with the following environment variables: 
* **AZURE_APP_ID** - The `Microsoft App ID` of the created Azure Bot
* **AZURE_APP_PASSWORD** - The created client secret in the previous section
* **SDM_BOT_PLATFORM** - Must be `ms-teams`.
* **SDM_ADMINS** - The administrator's email addresses (separated by spaces)

The MS Teams version uses a webhook endpoint. Ideally setup a HTTP Server with a Reverse Proxy pointing to: `0.0.0.0:3141`. For developing purposes you could use [ngrok](https://ngrok.com/), see [here](https://github.com/strongdm/accessbot/tree/main/ms-teams/dev/http-server)

To make sure if AccessBot is working, you can go back to the `Channels` tab on the create Azure Bot resource page and click on `Open in Teams` in the actions of the Microsoft Teams application to send DM messages to AccessBot on MS Teams and try the available commands:

![screenshot-11](https://user-images.githubusercontent.com/49597325/190443933-e11eca22-9611-4d06-9041-4b07de8cee26.png)

## Register the App

1. Generate an app id and enter the bot id
* Download the [ms-teams/app folder](https://github.com/strongdm/accessbot/blob/main/ms-teams/app)
* Generate an app id [here](https://www.uuidgenerator.net/version1) and enter it into the [manifest file](https://github.com/strongdm/accessbot/blob/main/ms-teams/app/manifest.json#L5)
* Enter the **AZURE_APP_ID** into the [manifest file](https://github.com/strongdm/accessbot/blob/main/ms-teams/app/manifest.json#L42)

2. Create a zip file of the app folder
```
$ zip app.zip *
  adding: color.png (deflated 2%)
  adding: manifest.json (deflated 64%)
  adding: outline.png (stored 0%)
```

3. Upload the app.zip file to [register the app](https://admin.teams.microsoft.com/) in your Org 

![image](https://user-images.githubusercontent.com/313803/141984124-60ab1eb8-ef3c-4cbb-9179-6c3767b86f34.png)

## Add the Bot to your Team

![image](https://user-images.githubusercontent.com/313803/141984925-d847d84a-c4ff-49f8-be14-c2c632616fbf.png)

## Limitations

Due to some MS Teams current limitations, the following features are not supported:

- Admins channel: it is not possible to add an application inside a private channel. Because of that, the bot will communicate with all the administrators via direct messages.
- Request access commands via direct messages (DM): it is not possible to send messages to the admins when the bot receives a message via DM, therefore all the commands that request access are disabled via DM.
