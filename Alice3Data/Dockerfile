FROM rootproject/root:6.22.02-ubuntu20.04

RUN apt update && apt install -y python3-pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY O2QAPlot /O2QAPlot

WORKDIR /O2QAPlot
RUN pip3 install -e .