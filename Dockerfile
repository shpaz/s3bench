# choose python image
FROM python

# add script to execution path
ADD objectAnalyzer.py /

# install needed pip packages
RUN pip install boto3
RUN pip install elasticsearch
RUN pip install humanfriendly
RUN pip install argparse

# run script from entry point
ENTRYPOINT [ "python", "./objectAnalyzer.py" ]
