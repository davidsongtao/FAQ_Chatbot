"""
Description: unit test logger

-*- Encoding: UTF-8 -*-
@File     ：test_log_config.py
@Author   ：King Songtao
@Time     ：2024/8/7 下午1:06
@Contact  ：king.songtao@gmail.com
"""
import pytest
from config.log_config import *
import os
import tempfile


# 通过pytest的fixture管理临时文件和目录
@pytest.fixture
def temp_log_file():
    # 创建一个临时文件
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    yield temp_file.name


def test_log_to_file(temp_log_file):
    # 配置loguru添加一个临时文件处理器
    logger.add(temp_log_file, format=log_format, level=log_level)

    # 记录一条日志消息
    logger.info("This is a test log message")

    # 读取临时文件内容
    with open(temp_log_file, 'r', encoding='utf-8') as file:
        log_content = file.read()

    # 验证日志内容是否包含期望的消息
    assert "This is a test log message" in log_content


def test_log_directory_exists():
    # 验证日志目录是否存在
    assert log_directory.exists()
    assert log_directory.is_dir()


def test_log_level():
    # 验证日志级别是否正确
    assert log_level in ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]


def test_log_format():
    # 验证日志格式是否正确
    assert "<green>{time:YYYY-MM-DD HH:mm:ss}</green>" in log_format
    assert "<level>{level: <8}</level>" in log_format
    assert "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>" in log_format


if __name__ == "__main__":
    pytest.main()
