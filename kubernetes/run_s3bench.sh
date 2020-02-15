#! /bin/bash

echo "Creating s3 object user..."
kubectl create -f object-user.yaml
sleep 10 
AccessKey=`kubectl get secret rook-ceph-object-user-my-store-shon -n rook-ceph -o 'jsonpath={.data.AccessKey}' | base64 --decode`
SecretKey=`kubectl get secret rook-ceph-object-user-my-store-shon -n rook-ceph -o 'jsonpath={.data.SecretKey}' | base64 --decode`
sed -i "s/ACCESS_KEY/${AccessKey}/g" s3bench.yaml
sed -i "s/SECRET_KEY/${SecretKey}/g" s3bench.yaml

echo "Running s3 bench workload..."
kubectl create -f s3bench.yaml
kubectl wait --for=condition=complete --timeout=600s job/s3bench

echo "Finished running workload! pushing visualizations to ELK stack"

kubectl create configmap s3-dashboard-configmap --from-file=s3_dashboard.ndjson > /dev/null
kubectl create -f put-dashboard.yaml
kubectl wait --for=condition=complete --timeout=600s job/put-dashboard
echo "Finished running all tests!"
