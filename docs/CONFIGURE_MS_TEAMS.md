# Configure MS Teams

In order to configure AccessBot integration with Slack follow the next steps:

## Create Azure Bot

1. Create an Azure Bot in [Azure Portal](https://portal.azure.com/)

![image](https://user-images.githubusercontent.com/313803/141980020-414d2355-79a7-40d1-a672-8e12b3afd559.png)

2. Enter the *Messaging endpoint* and get the **Microsoft App ID** from the Bot -> Configuration

![image](https://user-images.githubusercontent.com/313803/141983651-d6e3bd0b-65be-4e65-a018-2247ab2b79c9.png)

3. Get the **Secret Value** from the vault created with the App

* Configure access policies

![image](https://user-images.githubusercontent.com/313803/141981299-05caf3e2-36e4-4f99-9bae-17cf5f5a17fd.png)

* Get the secret

![image](https://user-images.githubusercontent.com/313803/141981551-5586276d-638e-438d-ab7a-751f1d7cde60.png)

The **Microsoft App ID** and **Secret Value** are the values for your variables **AZURE_APP_ID** and **AZURE_APP_PASSWORD** respectively. IMPORTANT: If you're passing environment variables via shell, ensure that you eclose the password between single quotes!

## Start the bot

Start accessbot with the following environment variables: 
* **AZURE_APP_ID**. Set to the **Microsoft App ID**
* **AZURE_APP_PASSWORD**. Set to the **Secret Value** 
* **SDM_BOT_PLATFORM**. Set to *ms-teams*
* **SDM_ADMINS**. Set to the administrator's email addresses (separated by spaces)

The MS Teams version uses a webhook endpoint. Ideally setup a HTTP Server with a Reverse Proxy pointing to: `0.0.0.0:3141`. For developing purposes you could use [ngrok](https://ngrok.com/), see [here](https://github.com/strongdm/accessbot/tree/main/ms-teams/dev/http-server)

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

- Admins channel: it is not possible to add an application inside a private channel. Because of that, the bot
will communicate with all the administrators via direct messages.
- Request access commands via direct messages (DM): it is not possible to send messages to the admins when the bot
receives a message via DM, therefore all the commands that request access are disabled via DM.
