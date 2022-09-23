# Troubleshooting

## Getting Slack usernames

Most interactions in Slack are done using the _Display Name_, which can be edited by users. For this configuration, you will need to use the Slack `username`. You can find this by replacing `WORKSPACE_URL_ID` in the following URL:
```
https://WORKSPACE_URL_ID.slack.com/account/settings#username
```

NOTE: you will find your workspace URL ID in Slack. On the upper left corner click on your workspace name and you will find your workspace URL inside the pop-up menu. Then you can extract your workspace URL ID from it.

Finally, open the link and scroll to the bottom of the page to find your username.

Another option is to use [this Python script](../tools/get-slack-handle.py), which will output your Slack username.

## Getting logs
```bash
# Getting logs
$ docker logs accessbot_accessbot_1 
# Following logs
$ docker logs -f accessbot_accessbot_1
```

## Changing log level
The default logging level is set to `INFO`. In case you want to get more information, you could add the following env variable:
```yaml
version: "3.9"
services:
  accessbot:
    build: .
    environment:
    - LOG_LEVEL=DEBUG
    # ...(rest of variables)...
```

For getting specific AccessBot logs, you could use:
```bash
$ docker logs -f accessbot_accessbot_1 2>&1 | grep "##SDM##"
```

## Error messages  
<details><Summary><code>"I cannot contact the approvers for this resource, their channel is unreachable"</code></Summary>
This means that either:

* The admin channel doesn’t exist  
* The bot is not part of the channel

Ensure that the bot is added to the channel by mentioning it in the channel.
</details>

<details><Summary><code>"You cannot use the requester flag." (Accessform)</code>
</Summary>
  
It's likely the `SDM_ACCESS_FORM_BOT_NICKNAME` is not set or has been set incorrectly. Verify that it is set for *both* the Accessbot and Accessform environments
  
</details>

<details><Summary><code>"Sorry, cannot find your account!"</code></Summary>
  
The email field (or the field set in `SDM_EMAIL_SLACK_FIELD` *must*  match exactly with the email that identified the user in strongDM. Verify that there are no differences between the two.

</details>

<details><Summary><code>"List resources failed: ('unauthenticated',16)"</code></Summary>
  
The strongDM API key is likely incorrect. Verify that the key has been entered properly -- this can also be caused by incorrect formatting in the spec for a container. 

</details>

<details><Summary><code>"errbot.backend_plugin_manager.PluginNotFoundException: Could not find the plugin named SlackBolt in ['/opt/conda/lib/python3.9/site-packages/errbot/backends']"</code></Summary>
  
This can occur when the repository is cloned directly, without updating submodules.  More information on setting up directly [here](./CONFIGURE_LOCAL_ENV.md).
  
</details>
