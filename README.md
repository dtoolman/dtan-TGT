# dtan-TGT
docker-compose sandbox ~ Python Flask framework with Kompose-created deployment,
and a MongoDB backend

## Install
```
# cd .
# docker-compose up -d --build
# docker-compose up -d --build --force-recreate service_name (optional)
```

## Usage
```
Flask,         http://localhost
Flask,         http://localhost/products/<prodid>
```

## Usage kompose.io
```
Ensure you're in the proper K8s context/namespace,
https://kompose.io/

# curl -L https://github.com/kubernetes/kompose/releases/download/v1.25.0/kompose-linux-amd64 -o kompose
# kompose convert
# kubectl apply -f .
```

## Destroy
```
# docker-compose down -v
```
