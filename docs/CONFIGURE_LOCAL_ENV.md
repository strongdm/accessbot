# Local environment

## Environment configuration
The installation of grpcio can be challenging, for that reason you might want to use [conda](https://docs.conda.io/en/latest/). In that case, just go though the following steps
```
conda create --prefix venv
conda install --prefix venv pip
conda activate venv
pip install -r requirements.txt
```

## Variables configuration
You need to fill in the details for this file
```
. set-env.sh
```

## Configure plugins directory
You could change [config.py](../config.py) or use a symbolic link
```
ln -s FULL_PATH_TO_SDM_FOLDER plugins
```

## Create Slack App
Follow this instructions: https://github.com/slackapi/python-slack-sdk/issues/609#issuecomment-639887212 
