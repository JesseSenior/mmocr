_base_ = [
    '_base_dbnet_resnet50_fpnc.py',
    '../_base_/datasets/ctw1500.py',
    '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_sgd_exp.py',
]

load_from = None

# dataset settings
ctw1500_textdet_train = _base_.ctw1500_textdet_train
ctw1500_textdet_test = _base_.ctw1500_textdet_test

test_pipeline_ctw = [
    dict(type='LoadImageFromFile', color_type='color_ignore_orientation'),
    dict(type='Resize', scale=(1024, 1024), keep_ratio=True),
    dict(
        type='LoadOCRAnnotations',
        with_polygon=True,
        with_bbox=True,
        with_label=True),
    dict(
        type='PackTextDetInputs',
        meta_keys=('img_path', 'ori_shape', 'img_shape', 'scale_factor'))
]

# pipeline settings
ctw1500_textdet_train.pipeline = _base_.train_pipeline
ctw1500_textdet_test.pipeline = test_pipeline_ctw

train_dataloader = dict(
    batch_size=16,
    num_workers=24,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=ctw1500_textdet_train)

val_dataloader = dict(
    batch_size=1,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=ctw1500_textdet_test)

test_dataloader = val_dataloader

auto_scale_lr = dict(base_batch_size=16)

_base_.optim_wrapper.optimizer.lr = 0.002

param_scheduler = [
    dict(type='LinearLR', end=100, start_factor=0.001),
    dict(type='PolyLR', power=0.9, eta_min=1e-7, end=_base_.train_cfg.max_epochs),
]
