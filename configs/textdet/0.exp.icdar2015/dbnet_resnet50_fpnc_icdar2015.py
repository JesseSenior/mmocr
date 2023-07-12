_base_ = [
    '_base_dbnet_resnet50_fpnc.py',
    '../_base_/datasets/icdar2015.py',
    '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_sgd_exp.py',
]

load_from = None

# dataset settings
icdar2015_textdet_train = _base_.icdar2015_textdet_train
icdar2015_textdet_train.pipeline = _base_.train_pipeline
icdar2015_textdet_test = _base_.icdar2015_textdet_test
icdar2015_textdet_test.pipeline = _base_.test_pipeline

train_dataloader = dict(
    batch_size=16,
    num_workers=24,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=icdar2015_textdet_train)

val_dataloader = dict(
    batch_size=1,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=icdar2015_textdet_test)

test_dataloader = val_dataloader

auto_scale_lr = dict(base_batch_size=16)

_base_.optim_wrapper.optimizer.lr = 0.002

param_scheduler = [
    dict(type='LinearLR', end=100, start_factor=0.001),
    dict(type='PolyLR', power=0.9, eta_min=1e-7, end=_base_.train_cfg.max_epochs),
]
