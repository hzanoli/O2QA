FROM rootproject/root:6.22.02-ubuntu20.04

RUN apt update && apt install -y python3-pip

COPY O2SingleTrackQA/requirements.txt .

RUN pip3 install -r requirements.txt

COPY O2SingleTrackQA /O2SingleTrackQA

WORKDIR /O2SingleTrackQA
RUN pip3 install -e .