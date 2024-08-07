"""
Description: 项目全局配置文件，配置所有参数
    
-*- Encoding: UTF-8 -*-
@File     ：parameter_config.py
@Author   ：King Songtao
@Time     ：2024/8/6 下午9:08
@Contact  ：king.songtao@gmail.com
"""
import torch.cuda


class ParameterConfig:
    def __init__(self):
        self.log_directory = r"D:\Projects\FAQ_Chatbot\logs"
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.embedding_model = r"D:\Projects\FAQ_Chatbot\models\bge-large-zh-v1.5"
        self.top_n: int = 3
        self.es_url = "http://172.18.0.2:9200"
