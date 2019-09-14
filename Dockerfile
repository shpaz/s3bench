# choose python image
FROM python

# install needed pip packages
RUN mkdir /code
WORKDIR /code
ADD s3bench.py /code/
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# run script from entry point
ENTRYPOINT [ "python", "./s3bench.py" ]
