FROM python:3.9-slim

ENV ERRBOT_DIR=/errbot

RUN mkdir -p $ERRBOT_DIR

WORKDIR $ERRBOT_DIR

VOLUME ["/errbot/data", "/errbot/plugins"]

COPY requirements.txt ./requirements.txt

RUN pip install \
      --no-cache-dir \
      --disable-pip-version-check \
      -r requirements.txt

RUN errbot --init
RUN pip install errbot[slack]
COPY config.py .

RUN mkdir -p plugins
RUN mkdir -p plugins/sdm
COPY sdm ./plugins/sdm/
