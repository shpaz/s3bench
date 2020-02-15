#! /bin/bash 

kubectl create -f common.yaml -f operator.yaml
kubectl wait --for=condition=available --timeout=600s deployment/rook-ceph-operator -n rook-ceph
kubectl create -f cluster-test.yaml
while [[ $(kubectl get cephcluster -n rook-ceph -o 'jsonpath={.items[*].status.ceph.health}') != "HEALTH_OK" ]]; do echo "waiting for cluster HEALTH OK" && sleep 1; done
kubectl create -f object.yaml 
sleep 30
kubectl create -f object-user.yaml 
while [[ $(kubectl get cephcluster -n rook-ceph -o 'jsonpath={.items[*].status.ceph.health}') != "HEALTH_OK" ]]; do echo "waiting for cluster HEALTH OK" && sleep 1; done
sleep 5 


kubectl create -f elasticsearch.yaml
kubectl wait --for=condition=ready --timeout=600s pod/esnode-0
kubectl create -f kibana.yaml
kubectl wait --for=condition=available --timeout=600s deployment/kibana
kubectl create configmap s3-dashboard-configmap --from-file=s3_dashboard.ndjson
kubectl port-forward service/kibana 5601
