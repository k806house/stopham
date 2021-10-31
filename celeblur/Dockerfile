FROM python:3.7-slim as storage

WORKDIR /workdir

RUN apt-get -y update && \
    apt-get install -y --fix-missing \
    build-essential \
    cmake \
    zip \
    ffmpeg \
    libsm6 \
    libxext6

ADD requirements.txt /tmp/
RUN pip3 install --no-cache-dir -Ur /tmp/requirements.txt

COPY app app

CMD ["python3", "/workdir/app/storage/server.py"]