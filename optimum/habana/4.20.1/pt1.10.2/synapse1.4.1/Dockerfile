FROM public.ecr.aws/habanalabs/pytorch-installer:1.10.2-ubuntu18.04-1.4.1-latest

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


RUN python3 -m pip install tensorboard transformers[sklearn,sentencepiece,audio,vision]==4.20.1 optimum[habana]  --no-cache-dir
