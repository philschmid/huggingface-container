# Hugging Face Containers

This repository contains a set of Docker images for training and serving Hugging Face models for different versions and libraries. 
The containers are structure and layered base on the following principles:
1. accelerator (CPU,GPU,HPU) + user + mamba + labels + maintainer
2. framework (PyTorch, Tensorflow)
3. use case (training, inference)
4. libraries (transformers, optimum, deepspeed)
5. custom (products, hf endpoints etc.)

## Accelerator

CPU includes
* mamba

GPU inculdes
* cuda 
* mamba
* openmpi (training)


## Command

```bash
docker compose --env-file .env build
```

### Jupyter

https://carpentries-incubator.github.io/introduction-to-conda-for-data-scientists/04-sharing-environments/index.html

## Build example

### buildx

```bash
docker buildx build \
    --platform=linux/amd64 \
    --output ./build \
    --file base/Dockerfile.cpu \
    .
```

### build

```bash
docker build -t test -f base/Dockerfile.cpu .
```


# TODO 

* Copy logic from https://github.com/anibali/docker-pytorch with giving him credits
* create templates 
* create manager.py 
* folders for transformers, optimum, custom 