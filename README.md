## s3bench

This project contains a container-based tool for benchmarking and visualizing various S3 workloads. This tool can be run on-premise, on the cloud etc (as long as storage backend provides native S3 API).

## Getting Started

To start using analyzer, please clone this git repostory: 
```
git clone https://github.com/shonpaz123/s3bench.git
```
### Prerequisites

To use this tool, you should have a running ELK cluster and a S3 based service. 

### Installing

To install this tool, you could choose between building the image on your on, or pulling the pre-built docker image. 
To build the image:

```
git clone https://github.com/shonpaz123/s3bench.git && cd s3bench
docker build -t s3bench .
```

To pull the existing docker image: 

```
docker pull shonpaz123/s3bench
```

## Running tests

To run this tool, you could run ``` docker run shonpaz123/s3bench ``` command to view which arguments should be passed, for example:

```
docker run shonpaz123/s3bench
usage: s3bench.py [-h] -e ENDPOINT_URL -a ACCESS_KEY -s SECRET_KEY -b
                         BUCKET_NAME -o OBJECT_SIZE -u ELASTIC_URL -n
                         NUM_OBJECTS -w WORKLOAD [-c CLEANUP]
s3bench: error: the following arguments are required: -e/--endpoint-url, -a/--access-key, -s/--secret-key, -b/--bucket-name, -o/--object-size, -u/--elastic-url, -n/--num-objects, -w/--workload
```
Arguments between squrae brackets are optional, the regular ones are required. To enter the man page run the command ``` docker run shonpaz123/s3bench -h ```, for example: 

``` 
optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT_URL, --endpoint-url ENDPOINT_URL
                        endpoint url for s3 object storage
  -a ACCESS_KEY, --access-key ACCESS_KEY
                        access key for s3 object storage
  -s SECRET_KEY, --secret-key SECRET_KEY
                        secret key for s3 object storage
  -b BUCKET_NAME, --bucket-name BUCKET_NAME
                        s3 bucket name
  -o OBJECT_SIZE, --object-size OBJECT_SIZE
                        s3 object size
  -u ELASTIC_URL, --elastic-url ELASTIC_URL
                        elastic cluster url
  -n NUM_OBJECTS, --num-objects NUM_OBJECTS
                        number of objects to put/get
  -w WORKLOAD, --workload WORKLOAD
                        workload running on s3 - read/write
  -c CLEANUP, --cleanup CLEANUP
                        should we cleanup all the object that were written
                        yes/no
```
## Results Analysis

This repository provides the ability of importing pre-built kibana dashboard for viewing bechmark data. The dashboard contains: 

* Latency Histogram: 

<p align="left">
    <img src="../master/dashboard/Latency.png" alt="Image" width="400" height="300" />
</p>

* Throughput Histogram: 

<p align="left">
    <img src="../master/dashboard/Throughput.png" alt="Image" width="400" height="300" />
</p>

* Percentile Histogram: 

<p align="left">
    <img src="../master/dashboard/Percentiles.png" alt="Image" width="800" height="300" />
</p>

* Max Object Latency Histogram: 

<p align="left">
    <img src="../master/dashboard/MaxLatencyObject.png" alt="Image" width="400" height="300" />
</p>

You are more than welcome to add one of your own ... ;)

### Dashboard Import

To import the dashboard you could use the two following methods:

(1) Go to kibana Management -> Saved Objects -> Import and upload the json s3_dashboard.ndjson file

(2) Run ```curl -X POST "localhost:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@s3_dashboard.ndjson ``` (from dashbaord folder, whrn `localhost` is the kibana server).


## Tutorial

Below example shows how to setup a local environment to benchmark a local Ceph Rados Gateway

Start Elastic:

```shell
sudo docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:6.5.4

sudo docker ps
CONTAINER ID        IMAGE                                                 COMMAND                  CREATED             STATUS              PORTS                                            NAMES
7ed851e60565        docker.elastic.co/elasticsearch/elasticsearch:6.5.4   "/usr/local/bin/do..."   29 minutes ago      Up 29 minutes       0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   dreamy_murdock
```

Run the benchmark (note the _CONTAINER ID_ from above):

```shell
sudo docker run --link 7ed851e60565:elasticsearch shonpaz123/s3bench -e http://$(hostname):8000 -a ${ACCESS_KEY} -s ${SECRET_KEY} -b s3bench -o 65536 -n 1000000 -w write -c no -u elasticsearch:9200
```

Run and connect to Kibana:

```shell
sudo docker run --link 7ed851e60565:elasticsearch -p 5601:5601 docker.elastic.co/kibana/kibana:6.5.4

firefox http://127.0.0.1:5601
```

## Built With

* [Docker Cloud](https://cloud.docker.com/) - used for automated build out of web-hooked source code. 

## Versioning

Build versions are handled through docker cloud. 

Supported versions for infrastructure components are: 
- ELK stack == 7.5

## Authors

* **Shon Paz** - *Initial work* - [shonpaz123](https://github.com/shonpaz123)

## Future Plans 
- Support for K8S and docker-compose 

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
