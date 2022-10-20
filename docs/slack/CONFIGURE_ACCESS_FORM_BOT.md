---
layout: default
title: Slack Accessbot Form (setup) 
nav_order: 5
parent: Slack
---
# AccessForm

AccessForm is the free way to request access to a resource using a form within Slack.

## Create AccessForm

In order to configure the form, you need to create a new Slack App.

1. First, go to [https://api.slack.com/apps](https://api.slack.com/apps), log in and click on "Create New App".

![image](https://user-images.githubusercontent.com/20745533/170760649-6f6e87ce-6436-42cd-9a31-b1ab0a801edb.png)

2. Then click on "From an app manifest".

![image](https://user-images.githubusercontent.com/20745533/170760802-59f037fc-3299-40c5-9d95-cf8c95556cdf.png)

3. On step 1, select your organization and click on "Next".

4. On step 2, copy and paste the content of the [access-form-manifest.yaml](/tools/access-form/access-form-manifest.yaml) file into the "YAML" field, and click on "Next".

![image](https://user-images.githubusercontent.com/20745533/170761741-5184ab7f-496e-4be2-a818-42079524ad28.png)

5. On step 3, review all the scopes and click on "Create".

![image](https://user-images.githubusercontent.com/20745533/170761924-d5f22dd9-4913-4144-8838-923f873e6725.png)

6. Finally, we need to add the bot into the organization. Go to the "OAuth & Permissions" page, click on "Install to Workspace" and in the next page click on "Allow".

![image](https://user-images.githubusercontent.com/20745533/170762982-9c7fd6ea-3c98-4d30-a8a5-f2395b00a49d.png)


## Installation and configuration

Now, after creating the Access Form Bot and configuring AccessBot on your machine, you can start configuring the Access Form backend.

1. First, we need to build the container image using the Dockerfile located in [tools/access-form](/tools/access-form):
    ```bash
    $ docker build -t accessform tools/access-form
    ```
    - Note: in this example we are using Docker, but you can use your preferred container orchestrator.
2. Now you need to configure the Access Form environment file following the template [access-form-env-file.example](/tools/access-form/access-form-env-file.example) file. Inside you will find the following required variables:
   - `SLACK_ACCESS_FORM_BOT_TOKEN`: obtained by accessing the "OAuth & Permissions" page of the Slack Access Form application:
      ![image](https://user-images.githubusercontent.com/20745533/170764833-22c9d936-5e45-42b5-b137-2a801a2435e0.png)

    - `SLACK_ACCESS_FORM_SIGNING_SECRET`: obtained by accessing the "Basic Information" page of the Slack Access Form application:
   ![image](https://user-images.githubusercontent.com/20745533/170765095-ed5d87ab-918d-462b-96fc-56a688948761.png)
      
    - `SLACK_ACCESS_FORM_CHANNEL_ID`: obtained by accessing a channel where AccessBot is present, clicking on the name of the channel in the upper left corner of the chat and copying the Channel ID informed at the bottom of the modal:
   ![image](https://user-images.githubusercontent.com/49795183/163469393-c110df8c-10d8-4e11-9827-3f2fe73e5e23.png)

   - `SDM_ACCESS_FORM_BOT_NICKNAME`: obtained by executing the following command in a terminal inside the root folder of the `accessbot` project:
            
    ```bash
    $ python tools/get-slack-handle.py -d "AccessForm"
    ```
    > By default this nickname is `@accessform`.

      - Note: remember to define in the current session the AccessBot `SLACK_BOT_TOKEN` environment variable in order to execute the script, otherwise an error will occur.
    
  - `NGROK_AUTHTOKEN`: obtained on [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken) after creating an account on [https://ngrok.com](https://ngrok.com)
 
   
3. Now we are ready to run the Access Form Bot container:

```bash
$ docker run --env-file /path/to/access-form-env-file accessform
⚡️ Bolt app is running! (development server)
```

4. Access [http://localhost:4040/inspect/http](http://localhost:4040/inspect/http) to see your ngrok links:

<img width="616" alt="image" src="https://user-images.githubusercontent.com/49597325/197025165-99fc8dcd-9200-4f0a-ad04-f8e9f75cdac3.png">

You will only need the HTTPS one. Copy it.

5. Now, go to the "App Manifest" page, and find the "interactivity" section inside the YAML field.

![image](https://user-images.githubusercontent.com/49597325/196991273-e02fd462-fdf9-4a81-b44d-9fe02b3239cf.png)

Then, under the `request_url` field replace "https://your-link.ngrok.io" with your HTTPS Ngrok link generated in a previous step and click on "Save Changes" in the top right corner of the page.

6. Finally, go to your Slack Workspace and add the bot into the channel which you got the Channel ID from. To do that, you can simply send a message mentioning the Access Form bot. In other words, just send a message with "@accessform", if that is the handle of your bot.


## Usage Example

The following GIF shows an example of using the resource access form within Slack.

![accessform-2](https://user-images.githubusercontent.com/49795183/163470488-ec502e31-6b54-4f0b-93f4-9c42acdbec46.gif)


## Access Form with Workflow Builder

In case you want to use Workflow Builder to build the form, please refer to [CONFIGURE_WORKFLOW_BUILDER_ACCESSBOT_FORM.md](/docs/slack/CONFIGURE_WORKFLOW_BUILDER_ACCESSBOT_FORM.md).
