FROM python:3.8.0

COPY . /work
WORKDIR /work
RUN set -eux \
  && pip install -r requirements.txt
RUN pip install autopep8 
