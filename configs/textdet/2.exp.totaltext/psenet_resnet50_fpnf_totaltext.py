_base_ = [
    '_base_psenet_resnet50_fpnf.py',
    '../_base_/datasets/totaltext.py',
    '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_adam_exp.py',
]

# optimizer
optim_wrapper = dict(optimizer=dict(lr=1e-4))
param_scheduler = [
    dict(type='MultiStepLR', milestones=[200, 400], end=_base_.train_cfg.max_epochs),
]


train_pipeline = [
    dict(type='LoadImageFromFile', color_type='color_ignore_orientation'),
    dict(
        type='LoadOCRAnnotations',
        with_polygon=True,
        with_bbox=True,
        with_label=True,
    ),
    dict(type='FixInvalidPolygon'),
    dict(
        type='RandomResize',
        scale=(800, 800),
        ratio_range=(0.75, 2.5),
        keep_ratio=True),
    dict(
        type='TextDetRandomCropFlip',
        crop_ratio=0.5,
        iter_num=1,
        min_area_ratio=0.2),
    dict(
        type='RandomApply',
        transforms=[dict(type='RandomCrop', min_side_ratio=0.3)],
        prob=0.8),
    dict(
        type='RandomApply',
        transforms=[
            dict(
                type='RandomRotate',
                max_angle=30,
                pad_with_fixed_color=False,
                use_canvas=True)
        ],
        prob=0.5),
    dict(
        type='RandomChoice',
        transforms=[[
            dict(type='Resize', scale=800, keep_ratio=True),
            dict(type='SourceImagePad', target_scale=800)
        ],
                    dict(type='Resize', scale=800, keep_ratio=False)],
        prob=[0.6, 0.4]),
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    dict(
        type='TorchVisionWrapper',
        op='ColorJitter',
        brightness=32.0 / 255,
        saturation=0.5,
        contrast=0.5),
    dict(
        type='PackTextDetInputs',
        meta_keys=('img_path', 'ori_shape', 'img_shape', 'scale_factor'))
]

test_pipeline = [
    dict(type='LoadImageFromFile', color_type='color_ignore_orientation'),
    dict(type='Resize', scale=(1280, 960), keep_ratio=True),
    # add loading annotation after ``Resize`` because ground truth
    # does not need to do resize data transform
    dict(
        type='LoadOCRAnnotations',
        with_polygon=True,
        with_bbox=True,
        with_label=True),
    dict(type='FixInvalidPolygon'),
    dict(
        type='PackTextDetInputs',
        meta_keys=('img_path', 'ori_shape', 'img_shape', 'scale_factor'))
]


# dataset settings
totaltext_textdet_train = _base_.totaltext_textdet_train
totaltext_textdet_test = _base_.totaltext_textdet_test
totaltext_textdet_train.pipeline = train_pipeline
totaltext_textdet_test.pipeline = test_pipeline

# use quadrilaterals for icdar2015
model = dict(
    backbone=dict(style='pytorch'),
    det_head=dict(postprocessor=dict(text_repr_type='quad')))

train_dataloader = dict(
    batch_size=16,
    num_workers=8,
    persistent_workers=False,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=totaltext_textdet_train)

val_dataloader = dict(
    batch_size=1,
    num_workers=1,
    persistent_workers=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=totaltext_textdet_test)

test_dataloader = val_dataloader

auto_scale_lr = dict(base_batch_size=64 * 4)
