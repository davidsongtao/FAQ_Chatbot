"""
Description: 基于loguru实现整个项目的日志管理系统。
    
-*- Encoding: UTF-8 -*-
@File     ：log_config.py
@Author   ：King Songtao
@Time     ：2024/8/6 下午9:07
@Contact  ：king.songtao@gmail.com
"""
from loguru import logger
import os
import sys
from pathlib import Path
from config.parameter_config import *

# 实例化全局配置参数
param = ParameterConfig()
log_directory = Path(param.log_directory)
# 检查日志目录是否存在
if not log_directory.exists():
    log_directory.mkdir(parents=True, exist_ok=True)
# 通过环境变量LOG_LEVEL获取日志级别，默认为INFO
log_level = os.getenv("LOG_LEVEL", "INFO")
# 配置日志的格式（时间，级别，来源）以及日志消息的显示格式
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# 配置一个日志处理器，用于将日志输出到一个文件中。
logger.add(
    log_directory / "faq_chatbot_{time:YYYY-MM-DD_HH-MM}.log",
    rotation="2 hours",  # 每2小时轮转一次日志文件
    retention="10 days",  # 保留最近10天的日志文件
    compression="zip",  # 表示压缩旧的日志文件为zip格式
    level=log_level,
    format=log_format,
    enqueue=True,  # 启用异步记录
)

# 配置一个日志处理器，用于将日志输出到标准错误流sys.stderr
logger.add(
    sys.stderr,
    format=log_format,
    level=log_level
)