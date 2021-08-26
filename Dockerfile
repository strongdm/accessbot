FROM continuumio/miniconda3

ENV ERRBOT_DIR=/errbot
ENV SDM_DOCKERIZED=true

RUN apt update
RUN apt install -y gcc
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

RUN rm -rf plugins/*
RUN mkdir -p plugins/sdm
COPY plugins/sdm ./plugins/sdm/

ENTRYPOINT [ "errbot" ]
