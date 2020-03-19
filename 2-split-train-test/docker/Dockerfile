FROM python:3.6
#RUN apt-get update
#RUN apt-get install -y python3 python3-pip
RUN apt-get update
RUN apt-get upgrade


RUN mkdir /app
RUN mkdir /data

ADD 2-split-train-test /app/
ADD data /data/

WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["python3", "split_train_test.py"]
