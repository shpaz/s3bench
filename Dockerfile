FROM python

ADD objectAnalyzer.py /

RUN pip install boto3
RUN pip install elasticsearch
RUN pip install humanfriendly
RUN pip install argparse

ENTRYPOINT [ "python", "./objectAnalyzer.py" ]
