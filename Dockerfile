# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/python:3.10.5-slim-bullseye

LABEL org.opencontainers.image.authors="FNNDSC <rudolph.pienaar@childrens.harvard.edu>" \
      org.opencontainers.image.title="FreeSurfer Simple Reporting" \
      org.opencontainers.image.description="A ChRIS DS plugin that generates a report table (in various formats) off a FreeSurfer annotation/segmentation volume"

WORKDIR /usr/local/src/pl-freesurfer_simplereport

COPY requirements.txt .
COPY FreeSurferColorLUT.txt .

RUN apt update
RUN apt -y install python3-pip libpango-1.0-0 libpangoft2-1.0-0

RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD ["freesurfer_simplereport", "--help"]
