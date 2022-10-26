---
layout: default
title: Slack - Accessform Usage
nav_order: 4
parent: Slack
---

# Configure AccessBot Form

This is a solution for requesting access to resources via a form page built using [Workflow Builder](https://slack.com/help/articles/360035692513-Guide-to-Workflow-Builder).

In case you already have an Access Form built from Workflow Builder, you can jump to the [Set Environment Variable](#Set-Environment-Variable). If you don't have one yet, please follow the next steps.

## Set Up Workflow Builder Access Form

In order to configure the access request form, you just need to add a new "Workflow shortcut" following the next images:

![image](https://user-images.githubusercontent.com/20745533/197523236-92cd845f-7875-4c13-84ef-ecd57c71e8e2.png)

![image](https://user-images.githubusercontent.com/20745533/197523285-aaa6c758-84f6-4021-92ff-53d75938b97b.png)

Then, you should be able to open the access form:

![image](https://user-images.githubusercontent.com/20745533/197523608-2e3abb8f-0e9c-4e11-9ffe-2171792480fe.png)

![image](https://user-images.githubusercontent.com/20745533/197523654-7c140d26-8915-4b5c-9917-f966cd2f99b2.png)


## Set Environment Variable

Now that you have an access form, let's configure the environment. You only need to add the environment variable `SDM_ACCESS_FORM_BOT_NICKNAME` in your `env-file` with the Workflow bot nickname.

To find out the Workflow bot's nickname run the following command in a terminal (in the project root):

```bash
$ python3 tools/get-slack-handle.py -d "AccessBot Form" 
```

After running this command, you should see something like this in the terminal:

```
The nick for that user is: @wb_bot_xxxxxxxxxxx
```

Finally, put that nickname as the value of the environment variable mentioned above.

```
SDM_ACCESS_FORM_BOT_NICKNAME=@wb_bot_xxxxxxxxxxx
```

## Usage Example

The following gif shows an example of how to use the AccessBot form to request a resource from StrongDM.

![accessbot-form](https://user-images.githubusercontent.com/82273420/163173633-243771d8-a31c-4f79-aaf6-102eb4265286.gif)
