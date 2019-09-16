# choose python image
FROM python

# install needed pip packages
RUN mkdir /code
WORKDIR /code
COPY s3bench.py /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# run script from entry point
ENTRYPOINT [ "python", "./s3bench.py" ]
