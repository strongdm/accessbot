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
```
# Getting logs
docker logs accessbot_accessbot_1 
# Following logs
docker logs -f accessbot_accessbot_1
```

## Changing log level
The default logging level is set to `INFO`. In case you want to get more information, you could add the following env variable:
```
version: "3.9"
services:
  accessbot:
    build: .
    environment:
    - LOG_LEVEL=DEBUG
    # ...(rest of variables)...
```

For getting specific AccessBot logs, you could use:
```
docker logs -f accessbot_accessbot_1 2>&1 | grep "##SDM##"
```
