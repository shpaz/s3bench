#! /bin/bash

kubectl create -f object-user.yaml

AccessKey=`kubectl get secret rook-ceph-object-user-my-store-shon -n rook-ceph -o 'jsonpath={.data.AccessKey}' | base64 --decode`
SecretKey=`kubectl get secret rook-ceph-object-user-my-store-shon -n rook-ceph -o 'jsonpath={.data.SecretKey}' | base64 --decode`
sed -i "s/ACCESS_KEY/${AccessKey}/g" s3bench.yaml
sed -i "s/SECRET_KEY/${SecretKey}/g" s3bench.yaml

kubectl create -f s3bench.yaml
kubectl wait --for=condition=complete --timeout=600s job/s3bench

echo "Done Deal! creating dashboard"

kubectl create -f put-dashboard.yaml
kubectl wait --for=condition=complete --timeout=600s job/put-dashboard

