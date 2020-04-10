# choose python image
FROM python:3.8-slim-buster

# install needed pip packages
RUN mkdir /code
WORKDIR /code
COPY s3bench.py /code/
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt

# run script from entry point
ENTRYPOINT [ "python3", "./s3bench.py" ]
