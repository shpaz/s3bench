## s3bench Kubernetes Demo 

This demo contains a full ecosystem deployment for running s3bench performance benchmark on rook as object storage backend and elasticsearch as a document based database for visualizations. 

## Getting Started

To start using s3bench, please clone this git repostory and move to the kubernetes directory: 
```
git clone https://github.com/shonpaz123/s3bench.git
cd kubernetes
```
### Prerequisites

To use this tool, you should have a running ELK stack and a S3 based service. In this demo, we have deployment for those services also (test scale only). 

### Use Cases

This tool integrates with every native S3 API, collects metrics and sends them to pre-built ELK stack. This tool cand be used for benchmarking all S3 based platforms (in and out of kuberenetes/openshift) such as rook-ceph-rgw, ceph-rgw, minio, aws S3 etc. 
To build the image:

## Running tests

To run this tool, first lets prepare the environment needed for us to run the benchmarks. To do this automatically, please run `prepare_env.sh` script which deployes S3 service based on rook-ceph and an ELK stack. This script is synchronous and waits for all services to be available before it exists. To ensure all services are up and running you could port-forward Kibana and rook S3 to localhost: 
```
kubectl port-forward service/kibana 5601
kubectl port-forward service/my-store-rgw 80  

```
Now access both of the ports using your web browser. http://127.0.0.1, http://127.0.0.1:5601

After both services are fully available, we can continue running our S3 workload tests. s3bench performas as Kubernetes job and number of clients is handled by `parallelism` field in s3bench.yaml file. to change the number of clients credentials, bucket name, object size, number of objects etc please access s3bench.yaml file. 

To run the test automatically, run `run_s3bench.sh` script which will fetch the needed credentials, push the needed dashboard and visualizations to the ELK stack and run the tests wanted. 

## Results Analysis

To see the results, an index will be created automatically, please create index pattern for `s3-perf-index` index and open `Demo` dashboard to see the results.

### Dashboard Import

Import is handled automatically by put-dashboard kubernetes job. 

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
