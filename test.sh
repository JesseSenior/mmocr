#!/bin/bash

tmux new-session -d \
    "conda activate openmmlab;\
        CUDA_VISIBLE_DEVICES=0 python tools/test.py configs/textdet/0.exp.icdar2015/dbnet_resnet50_fpnc_icdar2015.py work_dirs/dbnet_resnet50_fpnc_icdar2015/epoch_100.pth --show-dir imgs/dbnet_resnet50_fpnc_icdar2015/ --amp;\
        CUDA_VISIBLE_DEVICES=0 python tools/test.py configs/textdet/1.exp.ctw1500/dbnet_resnet50_fpnc_ctw1500.py     work_dirs/dbnet_resnet50_fpnc_ctw1500/epoch_100.pth   --show-dir imgs/dbnet_resnet50_fpnc_ctw1500/   --amp;\
        CUDA_VISIBLE_DEVICES=0 python tools/test.py configs/textdet/2.exp.totaltext/dbnet_resnet50_fpnc_totaltext.py work_dirs/dbnet_resnet50_fpnc_totaltext/epoch_100.pth --show-dir imgs/dbnet_resnet50_fpnc_totaltext/ --amp"\;\
    new-window "conda activate openmmlab;\
        CUDA_VISIBLE_DEVICES=1 python tools/test.py configs/textdet/0.exp.icdar2015/fcenet_resnet50_fpn_icdar2015.py work_dirs/fcenet_resnet50_fpn_icdar2015/epoch_100.pth --show-dir imgs/fcenet_resnet50_fpn_icdar2015/ --amp;\
        CUDA_VISIBLE_DEVICES=1 python tools/test.py configs/textdet/1.exp.ctw1500/fcenet_resnet50_fpn_ctw1500.py     work_dirs/fcenet_resnet50_fpn_ctw1500/epoch_100.pth   --show-dir imgs/fcenet_resnet50_fpn_ctw1500/   --amp;\
        CUDA_VISIBLE_DEVICES=1 python tools/test.py configs/textdet/2.exp.totaltext/fcenet_resnet50_fpn_totaltext.py work_dirs/fcenet_resnet50_fpn_totaltext/epoch_100.pth --show-dir imgs/fcenet_resnet50_fpn_totaltext/ --amp"\;\
    new-window "conda activate openmmlab;\
        CUDA_VISIBLE_DEVICES=2 python tools/test.py configs/textdet/0.exp.icdar2015/psenet_resnet50_fpnf_icdar2015.py work_dirs/psenet_resnet50_fpnf_icdar2015/epoch_100.pth --show-dir imgs/psenet_resnet50_fpnf_icdar2015/ --amp;\
        CUDA_VISIBLE_DEVICES=2 python tools/test.py configs/textdet/1.exp.ctw1500/psenet_resnet50_fpnf_ctw1500.py     work_dirs/psenet_resnet50_fpnf_ctw1500/epoch_100.pth   --show-dir imgs/psenet_resnet50_fpnf_ctw1500/   --amp;\
        CUDA_VISIBLE_DEVICES=2 python tools/test.py configs/textdet/2.exp.totaltext/psenet_resnet50_fpnf_totaltext.py work_dirs/psenet_resnet50_fpnf_totaltext/epoch_100.pth --show-dir imgs/psenet_resnet50_fpnf_totaltext/ --amp"\;\

tmux a -t 0:0
