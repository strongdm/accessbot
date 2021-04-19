# Local environment

## Environment configuration
The installation of grpcio can be challenging, for that reason you might want to use [conda](https://docs.conda.io/en/latest/). In that case, just go though the following steps
```
conda create --prefix venv
conda install --prefix venv pip
conda activate venv/
pip install -r requirements/dev.txt
```

## Variables configuration
```
export SLACK_TOKEN=slack-token
export SDM_API_ACCESS_KEY=api-access-key
export SDM_API_SECRET_KEY=api-secret-key
export SDM_ADMIN=@admin1 # if multiple, use: @admin1 @admin2
#export SDM_ADMIN_TIMEOUT=timeout-in-seconds
#export SDM_SENDER_NICK_OVERRIDE=sender-nick
#export SDM_SENDER_EMAIL_OVERRIDE=sender-email # valid strongDM email
#export SDM_AUTO_APPROVE_ALL=true # default: false
#export SDM_AUTO_APPROVE_TAG=auto-approve
#export SDM_HIDE_RESOURCE_TAG=hide-resource
```

## Initialize errbot
```
mv config.py config.py.back
errbot --init
pip install errbot[slack]
mv config.py.back config.py
```

## Create Slack App
Follow this instructions: https://github.com/slackapi/python-slack-sdk/issues/609#issuecomment-639887212 

## Run the bot
```
errbot
```
