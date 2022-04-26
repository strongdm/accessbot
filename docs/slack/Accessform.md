---
layout: default
title: Slack Accessbot Form (setup) 
nav_order: 5
parent: Slack
---
# AccessForm

AccessForm is the free way to request access to a resource using a form within Slack.

## Create AccessForm

In order to configure the form, you'd need to create a new Slack App, take a look [here](accessform-manifest.yaml)

## Installation and configuration

1. After downloading the repository and [configuring AccessBot](https://github.com/strongdm/accessbot) on your machine, you can start configuring the AccessForm backend;
2. In order for the AccessForm server to be visible across the internet, you must tunnel between your computer and a link using [localtunnel](https://github.com/localtunnel/localtunnel) (I strongly suggest that you read the README of the localtunnel project to better understand how to create a tunnel):
    1. Install localtunnel by running the command `npm install -g localtunnel` (you may need administrator powers);
    2. Create the tunnel by running the command `lt --port 3000 --subdomain accessform`;
        > Confirm that the returned link is `https://accessform.loca.lt`. Otherwise, contact an AccessForm collaborator.

        > The localtunnel project is under the MIT license and its source code and contributors can be seen in its [repository on GitHub](https://github.com/localtunnel/localtunnel).
3. In another terminal, inside the `accessform` folder (which is inside the `accessbot/tools/` folder):
    1. Run the command `python3 -m venv .venv` to create the application's virtual environment;
    2. Activate the application's virtual environment by running `source .venv/bin/activate`;
    3. Run `pip install -r requirements.txt` to install project dependencies;
    4. Set and export the environment variables listed in the `env-file.example` file:
        - SLACK_BOT_TOKEN: obtained by accessing the settings page of the Slack AccessForm application (if you do not have access to this settings page, contact someone responsible for the AccessBot or AccessForm project);
        - SLACK_SIGNING_SECRET: obtained by accessing the settings page of the Slack AccessForm application (if you do not have access to this settings page, contact someone responsible for the AccessBot or AccessForm project);
        - SLACK_CHANNEL_ID: obtained by accessing a channel that can be communicated with AccessBot, clicking on the name of the channel in the upper left corner of your chat and copying the Channel ID informed at the end of the open mini-window;

            ![image](https://user-images.githubusercontent.com/49795183/163469393-c110df8c-10d8-4e11-9827-3f2fe73e5e23.png)

        - SDM_ACCESS_FORM_BOT_NICKNAME: obtained by executing the following command in a terminal inside the root folder of the `accessbot` project (remember to be inside the accessbot project virtual environment and to export the necessary environment variables, otherwise an error will occur) :
            
            ```shell
            python tools/get-slack-handle.py -d "AccessForm"
            ```
            > By default this nickname is `@accessform`.

## Run the AccessForm server 

Now inside the `accessform` folder (which is inside the `accessbot/tools/` folder) run the server with the `python3 app.py` command and test its operation by trying to open the resource access form in a channel of the Slack in a workspace that has the AccessForm app installed.

## Usage Example

The following GIF shows an example of using the resource access form within Slack.

![accessform-2](https://user-images.githubusercontent.com/49795183/163470488-ec502e31-6b54-4f0b-93f4-9c42acdbec46.gif)

