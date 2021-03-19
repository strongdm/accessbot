FROM continuumio/miniconda3

ENV ERRBOT_DIR=/errbot
VOLUME ["/errbot/data", "/errbot/plugins"]

RUN mkdir -p $ERRBOT_DIR
WORKDIR $ERRBOT_DIR

COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install \
      --no-cache-dir \
      --disable-pip-version-check \
      -r requirements.txt

RUN errbot --init
RUN pip3 install errbot[slack]
COPY config.py .

RUN mkdir -p plugins
RUN mkdir -p plugins/sdm
COPY sdm ./plugins/sdm/
