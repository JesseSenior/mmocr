# Copyright (c) OpenMMLab. All rights reserved.
from .base import BaseTextDetHead
from .db_head import DBHead
from .drrg_head import DRRGHead
from .fce_head import FCEHead
from .fce_light_head import FCELightHead
from .pan_head import PANHead
from .pse_head import PSEHead
from .textsnake_head import TextSnakeHead

__all__ = [
    'PSEHead', 'PANHead', 'DBHead', 'FCEHead', 'FCELightHead', 'TextSnakeHead', 'DRRGHead',
    'BaseTextDetHead'
]
