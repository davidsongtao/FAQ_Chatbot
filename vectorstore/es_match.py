"""
Description: 基于ElasticSearch在本地知识库搜索预设好的答案。
    
-*- Encoding: UTF-8 -*-
@File     ：es_match.py
@Author   ：King Songtao
@Time     ：2024/8/7 下午4:01
@Contact  ：king.songtao@gmail.com
"""
from config.log_config import logger
from elasticsearch import Elasticsearch
from config.parameter_config import *

param = ParameterConfig()
es = Elasticsearch([param.es_url])
