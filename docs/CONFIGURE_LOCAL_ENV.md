# Local environment

## Environment configuration
The installation of grpcio can be challenging, for that reason you might want to use [conda](https://docs.conda.io/en/latest/). In that case, just go through the following steps
```bash
$ conda create --prefix venv
$ conda install --prefix venv pip
$ conda activate venv/
$ pip install -r requirements/dev.txt
```

## Variables configuration
```bash
$ export SDM_API_ACCESS_KEY=api-access-key
$ export SDM_API_SECRET_KEY=api-secret-key
$ export SDM_ADMINS=@admin1 # if multiple, use: @admin1 @admin2
```

### BOT PLATFORM variables configuration

See the subsessions about SDM_BOT_PLATFORM specific variables:

#### SDM_BOT_PLATFORM is `slack`
```bash
$ export SLACK_APP_TOKEN=slack-app-token
$ export SLACK_BOT_TOKEN=slack-bot-token
```

See [Configure Slack](slack/CONFIGURE_SLACK.md)

#### SDM_BOT_PLATFORM is `slack-classic`
```bash
$ export SLACK_TOKEN=slack-token
```

See [Configure Slack Classic Bot](slack/CONFIGURE_SLACK_CLASSIC.md)

#### SDM_BOT_PLATFORM is `ms-teams`:
```bash
$ export SDM_ADMINS=shane@strongdm.com # if multiple, use: user1@domain.com user2@domain.com
$ export AZURE_APP_ID=app-id
$ export AZURE_APP_PASSWORD=app-password
```

See [Configure Microsoft Teams](teams/CONFIGURE_MS_TEAMS.md)

---

Before initialize errbot, you also need to [Configure SDM](configure_accessbot/CONFIGURE_SDM.md).

## Initialize errbot
```bash
$ mv config.py config.py.back
$ pip install errbot[slack]
$ mv config.py.back config.py
```

## Update submodules
```bash
$ git submodule init
$ git submodule update
```

## Run the bot
```bash
$ pytest # run tests
$ errbot # starts bot
```
