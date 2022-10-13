FROM python:3.9

ENV ERRBOT_DIR=/errbot
ENV SDM_DOCKERIZED=true

RUN mkdir -p $ERRBOT_DIR
WORKDIR $ERRBOT_DIR

COPY requirements/common.txt ./requirements.txt
RUN pip install \
      --no-cache-dir \
      --disable-pip-version-check \
      -r requirements.txt
RUN pip install errbot[slack]

COPY config.py .
COPY errbot-slack-bolt-backend ./errbot-slack-bolt-backend
COPY errbot-backend-botframework ./errbot-backend-botframework

RUN mkdir ./data
RUN mkdir -p plugins/sdm
COPY plugins/sdm ./plugins/sdm/

ENTRYPOINT [ "errbot" ]

EXPOSE 3141
