# Local environment

## Environment configuration
The installation of grpcio can be challenging, for that reason you might want to use [conda](https://docs.conda.io/en/latest/). In that case, just go though the following steps
```
conda create --prefix venv
conda install --prefix venv pip
conda activate venv
pip install -r requirements/dev.txt
pip install errbot -U
```

## Variables configuration
```
export SLACK_TOKEN="[SLACK TOKEN HERE]
export SDM_API_ACCESS_KEY="[SDM TOKEN HERE]"
export SDM_API_SECRET_KEY="[SDM SECRET HERE]"
export SDM_ADMIN="[@SLACK_HANDLE]"
# Below is optional, default is 30 seconds
export SDM_ADMIN_TIMEOUT="[TIMEOUT IN SECONDS]"
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
