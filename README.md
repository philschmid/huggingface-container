# Hugging Face Containers

This repository contains a set of Docker images for training and serving Hugging Face models for different versions and libraries. 
The containers are structure and layered base on the following principles:

```bash
{framework}_{type}_images.yaml
```
example
```bash
transformers_training_images.yaml
```

Each yaml contains X images definition for transformers.

For the list of available DLC images, see [Available Huggingface Containers Images](). You can find more information on the images in the their respective `dockefile` and `environment.yaml` definitions.


## Generate image definitions

1. install dependencies

```bash
pip install -r requirements.txt
```

2. generate images

```bash
python generator.py
```

## Add new images

If you want to add new images you need to create a new `yaml` file similar to `transformers_training_images.yaml` and add the new images to it. You also need to create a new repository for the new images.

# Conda packages

* [pytorch](https://anaconda.org/pytorch/pytorch/files)