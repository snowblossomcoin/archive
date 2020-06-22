FROM python:3.7-slim
ADD . /archive
RUN /bin/bash pip install .
