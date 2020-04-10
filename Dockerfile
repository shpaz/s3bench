# Phase I - Builder source
FROM python:latest as builder

WORKDIR /usr/src/app

COPY s3bench.py ./
COPY requirements.txt ./
COPY pylint.cfg ./

WORKDIR /wheels

RUN cp /usr/src/app/requirements.txt ./
RUN pip wheel -r ./requirements.txt 

# Phase II - Lints Code 
FROM eeacms/pylint:latest as linting
WORKDIR /code
COPY --from=builder /usr/src/app/pylint.cfg /etc/pylint.cfg
COPY --from=builder /usr/src/app/s3bench.py ./
RUN ["/docker-entrypoint.sh", "pylint"]

# Phase III - Final Image 
FROM python:3.8-slim as serve
WORKDIR /usr/src/app
# Copy all packages instead of rerunning pip install
COPY --from=builder /wheels /wheels
RUN     pip install -r /wheels/requirements.txt \
                      -f /wheels \
       && rm -rf /wheels \
       && rm -rf /root/.cache/pip/* 

COPY --from=builder /usr/src/app/*.py ./
ENTRYPOINT ["python3", "./s3bench.py"]
