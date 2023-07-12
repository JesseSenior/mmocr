# Copyright (c) OpenMMLab. All rights reserved.
from .base import BaseTextDetPostProcessor
from .db_postprocessor import DBPostprocessor
from .drrg_postprocessor import DRRGPostprocessor
from .fce_postprocessor import FCEPostprocessor
from .fce_light_postprocessor import FCELightPostprocessor
from .pan_postprocessor import PANPostprocessor
from .pse_postprocessor import PSEPostprocessor
from .textsnake_postprocessor import TextSnakePostprocessor

__all__ = [
    'PSEPostprocessor', 'PANPostprocessor', 'DBPostprocessor',
    'DRRGPostprocessor', 'FCEPostprocessor', 'FCELightPostprocessor', 'TextSnakePostprocessor',
    'BaseTextDetPostProcessor'
]
