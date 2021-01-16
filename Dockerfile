FROM ubuntu:18.04
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev
COPY . /app
RUN pip3 install -r /app/requirements.txt
CMD ["/app/get_bitcoin_info.py"]
ENTRYPOINT ["python3"]