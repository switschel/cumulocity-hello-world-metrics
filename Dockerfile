FROM debian:11-slim

RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY hello-world.py hello-world.py /
CMD ["python3","-u","hello-world.py"]