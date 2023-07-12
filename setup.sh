#!/bin/bash

cd "${0%/*}"

apt install ffmpeg libsm6 libxext6 gcc -y

conda create --name openmmlab python=3.8 -y
conda activate openmmlab
conda install pytorch torchvision pytorch-cuda=11.8 -c pytorch -c nvidia -y
pip install pqi; pqi use tuna

pip install -U openmim
mim install mmengine mmcv mmdet
pip install -v -e .

wget https://download.openmmlab.com/mmocr/data/icdar2015/mini_icdar2015.tar.gz
mkdir -p data/
tar xzvf mini_icdar2015.tar.gz -C data/
rm mini_icdar2015.tar.gz

python tools/dataset_converters/prepare_dataset.py icdar2015 --task textdet
python tools/dataset_converters/prepare_dataset.py ctw1500 --task textdet
python tools/dataset_converters/prepare_dataset.py totaltext --task textdet