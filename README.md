# Hugging Face Containers

This repository contains a set of container images for training and serving Hugging Face models for different versions and libraries. 
The containers are structure and scoped base on the following principles:

1. The `buildspec/` directory is the source of truth for every generated container defintion in `containers/`
2. The `buildspec/` directory is strucuted by `{library}/{scope}/buildspec.yaml`. 
3. The `containers/` direcotry contained all the generated container definitions for the container and conda environment.
4. The `containers/` directory is structured by `{library}/{scope}/{tag.split("/")}/Dockerfile`. _tag is defined in the `buildspec.yaml` as key_
5. Never make changes in `containers/` since they will always be overwritten.
6. The `templates/` directory contains the templates for the different `Dockerfiles`, `environment.yaml` and Github `actions.yaml`
7. If you want to add new images check [add new images](#add-new-images).
8. Use `python generator.py` to create the `containers/`.

For the list of available DLC images, see [Available Huggingface Containers Images](available_images.md). You can find more information for each image their respective `Dockerfile` and `environment.yaml` definitions.

## Repository Structure

Below is a tree structure of the repository with comments
```bash
├── .github/workflows
│   └── {library}-{tag}.yaml # action to build, test, scan & push images
├── buildspec/
│   ├── {library}/{scope}
│       └── buildspec.yaml # definitions for all images for the library and scope
├── containers/
│   ├── {library}/{scope}/{tag}/{version}/{device}.../ # contains container artifact
│       ├── Dockerfile # Dockerfile for the container
│       └── environment.yaml # mamba/conda environment definition
└── index.html
```

## Add new images

If you want to add new images you need to follow the steps below:

### 1. Create new Repository in the Hugging Face Dockerhub account. 

If you don't have access to the Dockerhub account ping @philschmid in the PR of your new container.

### 2. Create a new `buildspec` in the `buildspec/` folder

If you want to create a new container image for library:transformers with a scope for distillation. You would create a new `buildspec.yaml` in the `buildspec/transformers/distillation` folder. In there you would all of the images you want to create, e.g. cpu, gpu etc. 
You can find an example for a `buildspec.yaml` [here](buildspec/transformers/training/buildspec.yaml).

### 3. Generate `Dockerfiles`, `environment.yaml` and `action.yaml`

After you added your `buildspec.yaml` you can generate the `Dockerfiles`, `environment.yaml` and `action.yaml` files by running the following command:

```bash
python generator.py
```

This command will re-generate all existing images and create your new image artifacts. Sticking with the distillation example you should new files generated in `containers/transformers/distillation/**`.

### 4. Add Tests _(Work in Progress how to add tests)_

Next step is to add your tests in the `tests/` folder. Therefore you create a new `test_*.py` including the tests for your new images.

### 5. Create PR for new images

The last step is to create a PR into the `main` branch this will trigger you generate CI action, which will try to build, test and scan the new image. After the pipeline is green you can ask for review. 

## Acknowledgements

* [AWS Deep Learning Containers](https://github.com/aws/deep-learning-containers)
* [anibali/docker-pytorch](https://github.com/anibali/docker-pytorch)

## Conda packages

* [pytorch](https://anaconda.org/pytorch/pytorch/files)
* [cudatoolkit](https://anaconda.org/nvidia/cuda-toolkit/files)