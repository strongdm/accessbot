# Local environment

## Environment configuration
The installation of grpcio can be challenging, for that reason you might want to use [conda](https://docs.conda.io/en/latest/). In that case, just go through the following steps
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
export SDM_ADMINS=@admin1 # if multiple, use: @admin1 @admin2
```

See [Configure Slack](CONFIGURE_SLACK.md) and [Configure SDM](CONFIGURE_SDM.md)

## Initialize errbot
```
mv config.py config.py.back
errbot --init
pip install errbot[slack]
mv config.py.back config.py
```

## Update submodules
```
git submodule init
git submodule update
```

## Run the bot
```
pytest # run tests
errbot # starts bot
```
