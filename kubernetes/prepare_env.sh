#! /bin/bash 

kubectl create -f common.yaml -f operator.yaml > /dev/null
kubectl wait --for=condition=available --timeout=600s deployment/rook-ceph-operator -n rook-ceph
kubectl create -f cluster-test.yaml > /dev/null
while [[ $(kubectl get cephcluster -n rook-ceph -o 'jsonpath={.items[*].status.ceph.health}') != "HEALTH_OK" ]]; do echo "waiting for cluster HEALTH OK" && sleep 10; done
kubectl create -f object.yaml > /dev/null
while [[ $(kubectl get cephcluster -n rook-ceph -o 'jsonpath={.items[*].status.ceph.health}') != "HEALTH_OK" ]]; do echo "waiting for cluster HEALTH OK" && sleep 10; done
sleep 5 

echo "creating an ELK stack..."
kubectl create -f elasticsearch.yaml > /dev/null
kubectl wait --for=condition=ready --timeout=600s pod/esnode-0
echo "elasticsearch service created!"
kubectl create -f kibana.yaml > /dev/null
kubectl wait --for=condition=available --timeout=600s deployment/kibana
echo "kibana service created!"
