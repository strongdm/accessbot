FROM continuumio/miniconda3

# Edit the values below for your organization -- leave quotes, omit brackets
ENV SLACK_TOKEN="[SLACK TOKEN HERE]"
ENV SDM_API_ACCESS_KEY="[SDM TOKEN HERE]"
ENV SDM_API_SECRET_KEY="[SDM SECRET HERE]"
ENV SDM_ADMIN="[@SLACK_HANDLE]"
# Below is optional, default is 30 seconds
ENV SDM_ADMIN_TIMEOUT="[TIMEOUT IN SECONDS]"

ENV ERRBOT_DIR=/errbot

RUN mkdir -p $ERRBOT_DIR

WORKDIR $ERRBOT_DIR

VOLUME ["/errbot/data", "/errbot/plugins"]

COPY requirements/common.txt ./requirements.txt

RUN pip install \
      --no-cache-dir \
      --disable-pip-version-check \
      -r requirements.txt

RUN errbot --init
RUN pip install errbot[slack]
COPY config.py .

RUN mkdir -p plugins/sdm
COPY plugins/sdm ./plugins/sdm/

ENTRYPOINT [ "errbot" ]
