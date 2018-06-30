# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
_detail_formatting = '[%(asctime)s] %(module)s.%(funcName)s %(levelname)s -> %(message)s'

logging.basicConfig(
    level=logging.DEBUG,
    format=_detail_formatting, # 出力のformatも変えられる
    filename="./pokeshiri.log", # logファイルのありか
)

