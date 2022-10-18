FROM vault.habana.ai/gaudi-docker/1.6.1/ubuntu20.04/habanalabs/pytorch-installer-1.12.0:latest

LABEL maintainer="Hugging Face"

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update \
    && apt-get -y upgrade --only-upgrade systemd openssl cryptsetup \
    && apt-get install -y \
    bzip2 \
    curl \
    git \
    git-lfs \
    tar \
    # audio
    libsndfile1-dev \
    ffmpeg \
    && apt-get clean autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}


RUN python3 -m pip install tensorboard transformers[sklearn,sentencepiece,audio,vision]==4.23.1 datasets==2.6.1 optimum==1.4.0 optimum-habana==1.2.3  --no-cache-dir
