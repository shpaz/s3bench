## s3bench

This project contains a container-based tool for benchmarking and visualizing various S3 workloads. This tool can be run on-premise, on the cloud etc (as long as storage backend provides native S3 API).

## Getting Started

To start using analyzer, please clone this git repostory: 
```
git clone https://github.com/shonpaz123/s3bench.git
```
### Prerequisites

To use this tool, you should have a running ELK stack and a S3 based service. 

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
                  BUCKET_NAME -o OBJECT_SIZE -u ELASTIC_URL -n NUM_OBJECTS -w
                  WORKLOAD [-l MAX_LATENCY] [-p PREFIX] [-c CLEANUP]
s3bench.py: error: the following arguments are required: -e/--endpoint-url, -a/--access-key, -s/--secret-key, -b/--bucket-name, -o/--object-size, -u/--elastic-url, -n/--num-objects, -w/--workload 
```
Arguments between squrae brackets are optional, the regular ones are required. To enter the man page run the command ``` docker run shonpaz123/s3bench -h ```, for example: 

``` 
usage: s3bench.py [-h] -e ENDPOINT_URL -a ACCESS_KEY -s SECRET_KEY -b
                  BUCKET_NAME -o OBJECT_SIZE -u ELASTIC_URL -n NUM_OBJECTS -w
                  WORKLOAD [-l MAX_LATENCY] [-p PREFIX] [-c CLEANUP]

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT_URL, --endpoint-url ENDPOINT_URL
                        endpoint url for s3 object storage
  -a ACCESS_KEY,   --access-key ACCESS_KEY
                        access key for s3 object storage
  -s SECRET_KEY,   --secret-key SECRET_KEY
                        secret key for s3 object storage
  -b BUCKET_NAME,  --bucket-name BUCKET_NAME
                        s3 bucket name
  -o OBJECT_SIZE,  --object-size OBJECT_SIZE
                        s3 object size
  -u ELASTIC_URL,  --elastic-url ELASTIC_URL
                        elastic cluster url
  -n NUM_OBJECTS,  --num-objects NUM_OBJECTS
                        number of objects to put/get
  -w WORKLOAD,     --workload WORKLOAD
                        workload running on s3 - read/write
  -l MAX_LATENCY,  --max-latency MAX_LATENCY
                        max acceptable latency per object operation in ms
  -p PREFIX,       --prefix PREFIX
                        A prefix (directory) located in the bucket
  -c CLEANUP,      --cleanup CLEANUP
                        should we cleanup all the object that were written
                        yes/no
```

To run this tool with docker-compose you could run ``` docker-compose up --scale s3bench=X -d ``` (where X is number of wanted replicas), docker-compose.yml file contains all needed arguments to be passed in order to commit the wanted workload to s3. 

For example: 
``` 
docker-compose up --scale s3bench=5 -d
Recreating s3bench_s3bench_1 ... done
Creating s3bench_s3bench_2   ... done
Creating s3bench_s3bench_3   ... done
Creating s3bench_s3bench_4   ... done
Creating s3bench_s3bench_5   ... done
```

### Ansible For Multiclient Support 

The `S3bench` role will create an entire infrastructure for you to start benchmarking your S3 service in a multiclient manner. This role creates a podman pod that interacts with your S3 service, creates a workload and documents all results in an ELK stack deployed by this role as well. In addition, There is an automation for throwing in some pre-defined dashboards that will help you analyze the results you get when performing the workload. 

This role divides into three parts: 

* The first part, deploys the ELK stack, and can be initiated by runinng ```ansible-playbook playbooks/s3bench.yml -i hosts --tags start_infra```. This will deploy an ELK stack, that will be available by host networking and can be accessed via port 5601 (Kibana port). 
* The second part, deploys the s3bench service, which is being defined by a workload located in `group_vars/s3bench.yml`. Once you edit this vars file with your configuration (such as endpoint_url, access_key, secret_key, bucket_name, etc) you could pick the hosts you want to run these on by editing the inventory file. After running ```ansible-playbook playbooks/s3bench.yml -i hosts --tags start_s3bench```, the playbook will add the needed containers to the pod and start testing your S3 service. 
* The third part, created the dashboards, running ```ansible-playbook playbooks/s3bench.yml -i hosts --tags create_dashboards``` will send an API request to Kibana wit hthe needed ndjson file. 

For example: 
```bash
$ ansible-playbook playbooks/s3bench.yml -i hosts --tags start_s3bench

TASK [s3bench : Search for any existing s3bench pod] *****************************************************************************************************************************************
changed: [localhost]

TASK [s3bench : Create A S3bench Pod If Not Exists] ******************************************************************************************************************************************
skipping: [localhost]

TASK [s3bench : Search for any existing s3bench instance] ************************************************************************************************************************************
changed: [localhost]

TASK [s3bench : Clean exsiting s3bench] ******************************************************************************************************************************************************
changed: [localhost] => (item=0)
changed: [localhost] => (item=1)
changed: [localhost] => (item=2)
changed: [localhost] => (item=3)
changed: [localhost] => (item=4)
changed: [localhost] => (item=5)
changed: [localhost] => (item=6)

TASK [s3bench : Start s3bench container using Podman] ****************************************************************************************************************************************
changed: [localhost] => (item=0)
changed: [localhost] => (item=1)
changed: [localhost] => (item=2)
changed: [localhost] => (item=3)
changed: [localhost] => (item=4)
changed: [localhost] => (item=5)
changed: [localhost] => (item=6)

PLAY RECAP ***********************************************************************************************************************************************************************************
localhost                  : ok=6    changed=4    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
```


## Results Analysis

This repository provides the ability of importing pre-built kibana dashboard for viewing bechmark data, how-to is provided in the next section. The dashboard will appear on kibana's dashboard section in the name 'Demo'.
You are more than welcome to add one of your own ... ;)

### Dashboard Import

To import the dashboard you could use the two following methods:

(1) Go to kibana Management -> Saved Objects -> Import and upload the json s3_dashboard.ndjson file

(2) Run ```curl -X POST "localhost:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@s3_dashboard.ndjson ``` (from dashbaord folder, where `localhost` is the kibana server).


## Running local ELK stack to visualize metrics

Below example shows how to setup a local environment to benchmark a local Ceph Rados Gateway (using Docker CLI) 

Start Elastic:

```shell
sudo docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:7.5.0

sudo docker ps
CONTAINER ID        IMAGE                                                 COMMAND                  CREATED             STATUS              PORTS                                            NAMES
7ed851e60565        docker.elastic.co/elasticsearch/elasticsearch:7.5   "/usr/local/bin/do..."   29 minutes ago      Up 29 minutes       0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   dreamy_murdock
```

Run the benchmark (note the _CONTAINER ID_ from above):

```shell
sudo docker run --link 7ed851e60565:elasticsearch shonpaz123/s3bench -e http://$(hostname):8000 -a ${ACCESS_KEY} -s ${SECRET_KEY} -b s3bench -o 65536 -n 1000000 -w write -l 10000 -c no -u elasticsearch:9200
```

Run and connect to Kibana:

```shell
sudo docker run --link 7ed851e60565:elasticsearch -p 5601:5601 docker.elastic.co/kibana/kibana:7.5.0

firefox http://127.0.0.1:5601
```

Below example shows how to setup a local environment to benchmark a local Ceph Rados Gateway (using Docker Compose)

Refer to https://github.com/deviantony/docker-elk.git repository and follow the instructions to run ELK stack in version 7.5 via docker-compose tool. 

```shell
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
- Support for Bucket Provisioning supported by OCP>=4.2

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
