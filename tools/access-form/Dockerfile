FROM continuumio/miniconda3

WORKDIR /server

ENV NODE_VERSION=16.13.0
ENV NVM_DIR=/root/.nvm
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"

COPY app.py app.py
COPY modal.py modal.py
COPY requirements.txt requirements.txt
COPY start-access-form.sh start-access-form.sh

RUN apt update -y
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}

RUN npm install -g localtunnel
RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["./start-access-form.sh"]
