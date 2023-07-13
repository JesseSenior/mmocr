#!/bin/bash

tmux new-session -d \
    "gpustat -i 1" \;\
    new-window "conda activate openmmlab;\
        CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/textdet/0.exp.icdar2015/dbnet_resnet50_fpnc_icdar2015.py --amp;\
        CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/textdet/1.exp.ctw1500/dbnet_resnet50_fpnc_ctw1500.py --amp;\
        CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/textdet/2.exp.totaltext/dbnet_resnet50_fpnc_totaltext.py --amp" \;\
    new-window "conda activate openmmlab;\
        CUDA_VISIBLE_DEVICES=1 python tools/train.py configs/textdet/0.exp.icdar2015/fcenet_resnet50_fpn_icdar2015.py --amp;\
        CUDA_VISIBLE_DEVICES=1 python tools/train.py configs/textdet/1.exp.ctw1500/fcenet_resnet50_fpn_ctw1500.py --amp;\
        CUDA_VISIBLE_DEVICES=1 python tools/train.py configs/textdet/2.exp.totaltext/fcenet_resnet50_fpn_totaltext.py --amp" \;\
    new-window "conda activate openmmlab;\
        CUDA_VISIBLE_DEVICES=2 python tools/train.py configs/textdet/0.exp.icdar2015/psenet_resnet50_fpnf_icdar2015.py --amp;\
        CUDA_VISIBLE_DEVICES=2 python tools/train.py configs/textdet/1.exp.ctw1500/psenet_resnet50_fpnf_ctw1500.py --amp;\
        CUDA_VISIBLE_DEVICES=2 python tools/train.py configs/textdet/2.exp.totaltext/psenet_resnet50_fpnf_totaltext.py --amp" \;\

tmux a -t 0:0