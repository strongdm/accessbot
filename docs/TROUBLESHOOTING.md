# Troubleshooting

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
