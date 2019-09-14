## s3bench

This project contains a container-based tool for benchmarking and visualizing various S3 workloads. This tool can be run on-premise, on the cloud etc (as long as storage backend provides native S3 API).

## Getting Started

To start using analyzer, please clone this git repostory: 
```
git clone https://github.com/shonpaz123/s3bencher.git
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
## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Docker Cloud](https://cloud.docker.com/) - used for automated build out of web-hooked source code. 

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

Supported versions for infrastructure components are: 
- ELK stack < 7.0

## Authors

* **Shon Paz** - *Initial work* - [shonpaz123](https://github.com/shonpaz123)

## Future Plans 
- Support for K8S and docker-compose 

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
