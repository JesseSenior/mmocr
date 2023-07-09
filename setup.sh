#!/bin/bash

# cd "${0%/*}/.."

apt install ffmpeg libsm6 libxext6 gcc -y

conda create --name openmmlab python=3.8 -y
conda activate openmmlab
conda install pytorch torchvision pytorch-cuda=11.8 -c pytorch -c nvidia -y
pip install pqi; pqi use tuna

pip install -U openmim
mim install mmengine mmcv mmdet
pip install -v -e .