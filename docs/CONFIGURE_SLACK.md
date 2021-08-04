# Configure Slack

In order to configure AccessBot integration with Slack follow the next steps:

1. Go to https://api.slack.com/apps and create an app from a manifest

![image](https://user-images.githubusercontent.com/313803/128012837-79be22d5-72ec-4e6a-92c3-da422332d524.png)

2. Enter the content of [slack-manifest.yaml](../slack-manifest.yaml)

![image](https://user-images.githubusercontent.com/313803/128013483-87b62077-cfc0-44d0-b64e-2f42a0a0d5bb.png)

NOTE: Adjust the YAML config according to your needs

3. Install App 

![image](https://user-images.githubusercontent.com/313803/128013824-acd31ba8-447f-423e-ada5-6e8585819501.png)

4. Assign a channel and click the "Allow" button:

![image](https://user-images.githubusercontent.com/313803/128013997-c35646af-5c24-4fcd-9417-a5e246492fb3.png)

5. On the Basic Information page, scroll down to the **App-Level Tokens** section and click the **Generate Tokens and Scopes** button:

![image](https://user-images.githubusercontent.com/313803/128014405-ed373269-994c-41dd-9b30-e7730a0fa242.png)

NOTE: Use scope: `connections:write`

6. Copy the generated `SLACK_APP_TOKEN`

![image](https://user-images.githubusercontent.com/313803/128014632-9e2cec27-21ee-445c-80a2-375088c19b68.png)

7. On the left side, click **OAuth & Permissions**, and copy the **Bot User OAuth Token**:

![image](https://user-images.githubusercontent.com/313803/128014877-911f5ef0-c766-43d1-8f30-6a66abc5e4e2.png)

**Use "App-Level Token" for _SLACK_APP_TOKEN_ and "Bot User OAuth Token" for _SLACK_BOT_TOKEN_ variables**
