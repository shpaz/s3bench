"""This module is used in order to create a interactive benchmark tool for S3 operations.
Metrics are written into ELasticsearch and can be visualized using Kibana."""

__author__ = "Shon Paz"
__email__ = "spaz@redhat.com"
__date__ = "10/04/2020"

import datetime
import time
import socket
import argparse
import uuid
import random
import boto3
import humanfriendly
from elasticsearch import Elasticsearch
from botocore.client import ClientError

TO_STRING = 'a'

class ObjectAnalyzer(object): #pylint: disable=too-many-instance-attributes
    """This class creates object analyzer objects, these objects are provided with pre-writen
        attributes and methods relevant for object storage performance analytics
    """
    def __init__(self):
        """creates all needed arguments for the program to run"""
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--endpoint-url', help="endpoint url for s3 object storage",
                            required=True)
        parser.add_argument('-a', '--access-key', help='access key for s3 object storage',
                            required=True)
        parser.add_argument('-s', '--secret-key', help='secret key for s3 object storage',
                            required=True)
        parser.add_argument('-b', '--bucket-name', help='s3 bucket name', required=True)
        parser.add_argument('-o', '--object-size', help='s3 object size', required=True)
        parser.add_argument('-u', '--elastic-url', help='elastic cluster url', required=True)
        parser.add_argument('-n', '--num-objects', help='number of objects to put/get',
                            required=True)
        parser.add_argument('-w', '--workload', help='workload running on s3 - read/write',
                            required=True)
        parser.add_argument('-c', '--cleanup',
                            help='should we cleanup all the object that were written yes/no',
                            required=False)

        # parsing all arguments
        args = parser.parse_args()

        # building instance vars
        self.endpoint_url = args.endpoint_url
        self.access_key = args.access_key
        self.secret_key = args.secret_key
        self.bucket_name = args.bucket_name
        self.elastic_cluster = args.elastic_url
        self.object_size = args.object_size
        self.object_name = ""
        self.num_objects = args.num_objects
        self.workload = args.workload
        self.cleanup = args.cleanup
        self.s3 = boto3.client('s3', endpoint_url=self.endpoint_url, #pylint: disable=invalid-name
                               aws_access_key_id=self.access_key,
                               aws_secret_access_key=self.secret_key)
        self.elastic = Elasticsearch(self.elastic_cluster, verify_certs=False)
        self.cleanup_list = []

    def check_bucket_existence(self):
        """This function checks for bucket existence"""
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError:
            return False

    def create_bucket(self):
        """This function creates bucket according the the user's input"""
        self.s3.create_bucket(Bucket=self.bucket_name)

    @classmethod
    def calcuate_throughput(cls, latency, req_size_in_bytes):
        """This method calculates each request's throughput"""
        # IOPS * BS / TO_MB
        return (1000 / latency) * req_size_in_bytes / 1000 ** 2

    def put_object(self, object_name, bin_data):
        """ This function writes an object to object storage using in-memory generated binary
            data"""
        self.s3.put_object(Key=object_name, Bucket=self.bucket_name, Body=bin_data)
        self.cleanup_list.append(object_name)

    def get_object(self, object_name):
        """This function gets an object from object storage"""
        response = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
        response['Body'].read()

    @classmethod
    def generate_object_name(cls):
        """This function generates randomized object name"""
        return str(uuid.uuid4())

    def create_bin_data(self):
        """This function creates object data according to user's object size input"""
        return humanfriendly.parse_size(self.object_size) * TO_STRING

    def get_objects_num(self):
        """This function return number of iterations"""
        return int(self.num_objects)

    def get_workload(self):
        """This function returns workload"""
        return self.workload

    def get_cleanup(self):
        """This function returns weather the client needs a cleanup"""
        return self.cleanup

    def time_operation(self, method, object_name, bin_data):
        """This function is a generic timer for s3 CRUD operations"""
        if method == 'GET':
            start = datetime.datetime.now()
            self.get_object(object_name)
            end = datetime.datetime.now()
            diff = (end - start).total_seconds() * 1000

        elif method == 'PUT':
            start = datetime.datetime.now()
            self.put_object(object_name, bin_data)
            end = datetime.datetime.now()
            diff = (end - start).total_seconds() * 1000

        return diff

    @classmethod
    def create_timestamp(cls):
        """This method parses time into kibana timestamp"""
        return round(time.time() * 1000)

    def prepare_elastic_index(self):
        """This function prepares elasticsearch index for writing"""
        es_index = 's3-perf-index'
        mapping = '''
           {
               "mappings": {
                 "properties": {
                   "timestamp": {
                    "type": "date"
                    }
                 }
               }
           }'''
        if not self.elastic.indices.exists(es_index):
            self.elastic.indices.create(index=es_index, body=mapping)

    def write_elastic_data(self, **kwargs):
        """This function gets a pre-built json and writes it to elasticsearch"""
        self.elastic.index(index='s3-perf-index', body=kwargs)

    def objects_cleanup(self):
        """This function deletes all objects created within the workload"""
        for object_name in self.cleanup_list:
            self.s3.delete_object(Bucket=self.bucket_name, Key=object_name)

    def list_random_objects(self):
        """This function returns randomized list of object in a bucket according to a given number
        In case number is bigger than 1000, use pagination, else use regular v2"""
        # in case number of objects is smaller then the page size, to save list costs
        if int(self.num_objects) <= 1000:
            objects = self.s3.list_objects(Bucket=self.bucket_name, MaxKeys=int(self.num_objects))
        else:
            keys = []
            # uses pagination to list object number bigger then 1000
            paginator = self.s3.get_paginator('list_objects')
            pages = paginator.paginate(Bucket=self.bucket_name)
            for page in pages:
                for obj in page['Contents']:
                    keys.append({'Key':obj['Key'], 'Size':obj['Size']})
            # shuffles keys list randomly to create different list between clients
            random.shuffle(keys)
            # picks a random object from the list
            random_object_index = keys.index(random.choice(keys))
            # creates a circular list for list index deviation
            circular_keys = keys + keys
            # returns a slice of keys list according to num_objects var
            return circular_keys[random_object_index:random_object_index + int(self.num_objects)]
        # in case there is no need for pagination and there are objects to read in the bucket
        if 'Contents' in objects:
            return objects['Contents']
        else:
            raise Exception("no objects to read in bucket!")

if __name__ == '__main__':

    # creates an object analyzer instance from class
    object_analyzer = ObjectAnalyzer() #pylint: disable=invalid-name

    # prepares elasticsearch index for writing
    object_analyzer.prepare_elastic_index()

    # checks for bucket existence, creates if doesn't exist
    if not object_analyzer.check_bucket_existence() and object_analyzer.get_workload() == "write":
        object_analyzer.create_bucket()

    # creates binary data
    DATA = object_analyzer.create_bin_data()

    # verifies that user indeed wants to write
    if object_analyzer.get_workload() == "write":

        # writes wanted number of objects to the bucket
        for index in range(object_analyzer.get_objects_num()):

            # generates new object's name
            object_name_given = object_analyzer.generate_object_name()

            # times put operation
            duration = object_analyzer.time_operation('PUT', object_name=object_name_given,
                                                      bin_data=DATA)

            # gets object size in bytes
            size_in_bytes = humanfriendly.parse_size(object_analyzer.object_size)

            # calculates throughput per request
            throughput = object_analyzer.calcuate_throughput(duration, size_in_bytes)

            # writes data to elasticsearch
            object_analyzer.write_elastic_data(latency=duration,
                                               timestamp=object_analyzer.create_timestamp(),
                                               workload=object_analyzer.get_workload(),
                                               size=object_analyzer.object_size,
                                               size_in_bytes=size_in_bytes,
                                               throughput=throughput,
                                               object_name=object_name_given,
                                               source=socket.gethostname())

    # in case the user chosen read operation
    elif object_analyzer.get_workload() == "read":

        # gathers a list of the wanted objects
        OBJECTS_LIST = object_analyzer.list_random_objects()

        # reads wanted number of objects to the bucket
        for entity in OBJECTS_LIST:
            # sets relevant variables
            object_name_given = entity['Key']
            object_size = entity['Size']

            # gathers latency from get operation
            duration = object_analyzer.time_operation('GET', object_name_given, "")

            # gets the object size parsed
            size = humanfriendly.format_size(object_size)

            # gets the size of bytes
            size_in_bytes = object_size

            # calculates throughput
            throughput = object_analyzer.calcuate_throughput(duration, size_in_bytes)

            # writes data to elasticsearch
            object_analyzer.write_elastic_data(latency=duration,
                                               timestamp=object_analyzer.create_timestamp(),
                                               workload=object_analyzer.get_workload(),
                                               size_in_bytes=size_in_bytes,
                                               size=size,
                                               object_name=object_name_given,
                                               throughput=throughput,
                                               source=socket.gethostname())
    # in case cleanup is chosen
    if object_analyzer.get_cleanup() == "yes":
        object_analyzer.objects_cleanup()
