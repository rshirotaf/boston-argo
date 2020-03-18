FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip

RUN mkdir /app
RUN mkdir /data

ADD 3-train-model /app/
ADD data /data/

WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["python3", "train_model.py"]
