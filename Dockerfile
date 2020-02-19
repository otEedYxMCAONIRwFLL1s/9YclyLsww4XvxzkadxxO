FROM python:3-alpine

ADD ssh-conf-gen.py ssh-conf-gen.py

RUN pip3 install \
  pyyaml \
  argparse
