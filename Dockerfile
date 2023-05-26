FROM python:3.11

# Copy files
COPY . ligo

RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive pip install --upgrade pip

# Voila: install ligo
RUN pip3 install ./ligo/
RUN stitchrdl -s human
