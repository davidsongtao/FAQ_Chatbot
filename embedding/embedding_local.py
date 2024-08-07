"""
Description: 
    
-*- Encoding: UTF-8 -*-
@File     ：embedding_local.py
@Author   ：King Songtao
@Time     ：2024/8/6 下午9:34
@Contact  ：king.songtao@gmail.com
"""
import torch
from config.log_config import *
from config.parameter_config import *
from transformers import AutoTokenizer, AutoModel
import warnings

# 消除警告信息
warnings.filterwarnings("ignore", category=UserWarning, message="TypedStorage is deprecated")

param = ParameterConfig()
tokenizer = AutoTokenizer.from_pretrained(param.embedding_model, trust_remote_code=True)
model = AutoModel.from_pretrained(param.embedding_model, trust_remote_code=True).half().cuda()
model = model.to(param.device)
model.eval()


def compute_embedding(text: str):
    try:
        encoded_input = tokenizer(
            text,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512
        ).to(param.device)

        with torch.no_grad():
            outputs = model(**encoded_input)
            # 从模型推理结果中提取句子embedding,获取输出的最后一层的隐藏状态，选择每个序列的第一个token(通常是[CLS])的嵌入。
            # 能够表征这句话的含义。
            sentence_embedding = outputs[0][:, 0]
            # 对提取的句子embedding进行L2标准化句子embedding
            sentence_embedding = torch.nn.functional.normalize(sentence_embedding, p=2, dim=1)
            sentence_embedding = sentence_embedding.cpu().tolist()
            return sentence_embedding

    except Exception as e:
        logger.error(f"发生错误：{e},请检查代码！", exc_info=True)


def get_embedding(text: str):
    _embedding = compute_embedding(text)
    return _embedding[0]
