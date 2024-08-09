"""
Description: 基于FastAPI构建API服务器接口
    
-*- Encoding: UTF-8 -*-
@File     ：server.py
@Author   ：King Songtao
@Time     ：2024/8/6 下午9:00
@Contact  ：king.songtao@gmail.com
"""
import json
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from config.log_config import *
from embedding.embedding_local import *

# 创建FastAPI实例
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，在生产环境中应该更具体
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)


# 构建一个数据模型类
class QueryData(BaseModel):
    """
    定义一个数据模型类，进行验证
    """
    text: str


# 构建路由
@app.post("/faq/search")
def search(query_data: QueryData):
    try:
        # 获取用户输入的文本
        logger.info(f"用户输入的文本：{query_data.text}")
        # 计算query的向量表示
        query_vec = get_embedding(query_data.text)
        return {"query_vec": query_vec}

    except Exception as e:
        logger.exception(f"发生异常：{e}")
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8008)

