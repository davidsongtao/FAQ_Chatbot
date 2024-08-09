"""
Description: 逐步解析es_index文件
    
-*- Encoding: UTF-8 -*-
@File     ：es_index.py
@Author   ：King Songtao
@Time     ：2024/8/8 下午7:35
@Contact  ：king.songtao@gmail.com
"""
import json

import elasticsearch
from elasticsearch import Elasticsearch, helpers
from config.parameter_config import *
from config.log_config import *
import click
from embedding.embedding_local import *

# 实例化全局配置文件和es数据库对象
param = ParameterConfig()
es = Elasticsearch(param.es_url)


# TODO 在ES数据库中创建索引
def create_index():
    # ES 语句 -> 创建ES索引
    index_body = {
        "mappings": {
            "properties": {
                "question": {
                    "type": "text"
                },
                "similar_question": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_max_word"
                },
                "similar_question_vector": {
                    "type": "dense_vector",
                    "dims": 1024
                },
                "answer": {
                    "type": "text"
                }
            }
        }
    }

    # 如果索引已存在，做相应处理
    if es.indices.exists(index=param.es_index_name):
        if click.confirm(f"索引{param.es_index_name}已存在，确定要删除该索引么？", default=None):
            try:
                response = es.indices.delete(index=param.es_index_name)
                if response["acknowledged"]:
                    logger.info(f"索引{param.es_index_name}已删除！")
                else:
                    logger.error(f"索引删除失败。发生未知错误！")
            except Exception as e:
                logger.error(f"删除索引时发生错误：{e}")
                raise e
        else:
            logger.info(f"用户已取消索引 {param.es_index_name} 的删除操作。")
            return

    # 若索引不存在，创建索引。
    try:
        response = es.indices.create(index=param.es_index_name, body=index_body)
        if response["acknowledged"]:
            logger.info(f"索引{param.es_index_name}创建成功！")
    except Exception as e:
        logger.error(f"创建失败，该索引已存在！错误信息：{e}")
        raise e


# TODO 读取本地数据文件
def read_json_file(file_path):
    batch = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            # 处理空行
            if not line.strip():
                continue
            try:
                data = json.loads(line.strip())
                # 构建必要的数据
                for similar_question in data["similar_question"]:
                    similar_question_vector = get_embedding(similar_question)
                    # 构建es数据库的action,以便后续使用helpers.bulk()函数批量操作这些数据
                    action = {
                        "_index": param.es_index_name,
                        "_source": {
                            "question": data["question"],
                            "similar_question": similar_question,
                            "similar_question_vector": similar_question_vector,
                            "answer": data["answer"]
                        }
                    }

                    batch.append(action)
                    if len(batch) == param.es_index_batch_size:
                        yield batch
                        batch = []

            except Exception as e:
                logger.error(f"发生错误：{e}")

        if batch:
            yield batch


# TODO 批量插入数据
def batch_insert(file_path):
    try:
        for batch in read_json_file(file_path):
            response = helpers.bulk(es, batch)
            logger.info(f"数据批量插入成功！", response)
    except Exception as e:
        logger.error(f"发生位置错误。错误信息：{e}")


if __name__ == '__main__':
    create_index()
    batch_insert(param.data_file_path)
