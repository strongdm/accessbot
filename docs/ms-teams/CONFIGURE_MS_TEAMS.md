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

12. Now go to the Azure Active Directory page:

![image](https://user-images.githubusercontent.com/20745533/193577832-754365cd-18df-400e-9db5-78cff446bddd.png)

13. Finally, copy the `Tenant ID` and paste it into the environment variable `AZURE_AD_TENANT_ID`.

![image](https://user-images.githubusercontent.com/20745533/193578281-5c9c508c-ede2-45be-9712-1c8a90c8b3a3.png)

And now we can use AccessBot in Microsoft Teams via DMs. In the following section we'll configure the bot to use into the Microsoft Teams Organization.

**NOTE**: If you're passing environment variables via shell, ensure that you eclose the `AZURE_APP_PASSWORD` value between single quotes!

## Start the bot

Start accessbot with the following environment variables: 
* **AZURE_APP_ID** - The `Microsoft App ID` of the created Azure Bot
* **AZURE_APP_PASSWORD** - The created client secret in the previous section
* **AZURE_AD_TENANT_ID** - The `Tenant ID` value shown in the Azure Active Directory page
* **SDM_BOT_PLATFORM** - Must be `ms-teams`.
* **SDM_ADMINS** - The administrator's email addresses (separated by spaces)

The MS Teams version uses a webhook endpoint. Ideally setup a HTTP Server with a Reverse Proxy pointing to: `0.0.0.0:3141`. For developing purposes you could use [ngrok](https://ngrok.com/), see [here](https://github.com/strongdm/accessbot/tree/main/ms-teams/dev/http-server)

To make sure if AccessBot is working, you can go back to the `Channels` tab on the create Azure Bot resource page and click on `Open in Teams` in the actions of the Microsoft Teams application to send DM messages to AccessBot on MS Teams and try the available commands:

![screenshot-11](https://user-images.githubusercontent.com/49597325/190443933-e11eca22-9611-4d06-9041-4b07de8cee26.png)

## Register the App

1. Generate an app id and enter the bot id
* Download the [ms-teams/app folder](https://github.com/strongdm/accessbot/blob/main/ms-teams/app)
* Generate a random id [here](https://www.uuidgenerator.net/version1) and define it in the ["id" field of the manifest.json file](../../ms-teams/app/manifest.json#L5)
* Paste the **AZURE_APP_ID** on the ["botId" field of the manifest.json file](../../ms-teams/app/manifest.json#L38)

2. Create a zip file of the app folder
```
$ zip app.zip *
  adding: color.png (deflated 2%)
  adding: manifest.json (deflated 57%)
  adding: outline.png (stored 0%)
```

3. Open your `Microsoft Teams App`, go to `Apps` and search for `Developer Portal`, then click on The `Developer Portal` card:

![screenshot-13](https://user-images.githubusercontent.com/49597325/190476467-560c14e8-b44e-430c-89b5-95dfaf06d74b.png)

4. Click on the `Apps` tab of the `Developer Portal` app and click on the `Import app` button and select the created zip file:

![screenshot-14](https://user-images.githubusercontent.com/49597325/190476632-b4dc9f11-723d-41e0-9d2b-75ec6a1d20cc.png)

5. Once it finishes to upload the zip file data and load the app content, you can update the informations you prefer about the bot.

6. Then go to the `Publish` section and click on the `Publish to org` submenu and click on the `Publish your app` button:

![screenshot-15](https://user-images.githubusercontent.com/49597325/190476774-e53fd677-764f-450b-8e15-13426466b14c.png)

7. After a while, your app should be submitted:

![screenshot-16](https://user-images.githubusercontent.com/49597325/191028372-ebf9812c-43c5-44e4-8e4f-3f01d01fdb6d.png)

8. Then, go to `Teams`, click on the actions of the team you want to add the bot and click on `Manage Team`:

![screenshot-17](https://user-images.githubusercontent.com/49597325/191032343-c1d4abab-2659-48cd-876c-862817bec16a.png)

9. Click on the `Apps` tab and on the `More Apps` button:

![screenshot-18](https://user-images.githubusercontent.com/49597325/191029186-5ac64ab5-ffef-43e4-8991-ad163e726694.png)

10. Click on the submitted bot:

![screenshot-19](https://user-images.githubusercontent.com/49597325/191029760-fd0316d7-a9ea-4bf3-a268-2e02471e35e1.png)

11. Click on the `Add` button:

![screenshot-20](https://user-images.githubusercontent.com/49597325/191030231-9318becd-b9bd-46f2-b1bc-e08a3336f768.png)

And your bot is now installed on your organization and can be used on your teams.

## How to use

To use AccessBot commands on Teams, you need to add a mention to the bot before the command (see the image below for an example running the help command):

![screenshot-21](https://user-images.githubusercontent.com/49597325/191031228-eb2b7360-8c4f-4059-8ae3-cfc97b612902.png)

## Limitations

Due to some MS Teams current limitations, the following features are not supported:

- Request access commands via direct messages (DM): it is not possible to send messages to the admins when the bot receives a message via DM, therefore all the commands that request access are disabled via DM.
- Admins reachability: if you want the admins to manage the access requests via DMs, you need to make sure that all the
`SDM_ADMINS` belong to all teams inside your organization, because when a user requests an access the bot searches for 
the admins details inside the requester's team. So, because of this limitation we strongly recommend you to enable the
[SDM_ADMINS_CHANNEL](/docs/configure_accessbot/CONFIGURE_ACCESSBOT.md#Bot-configuration) feature.
