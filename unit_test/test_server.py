"""
Description: server单元测试
    
-*- Encoding: UTF-8 -*-
@File     ：test_server.py
@Author   ：King Songtao
@Time     ：2024/8/7 上午11:36
@Contact  ：king.songtao@gmail.com
"""
import pytest
from fastapi.testclient import TestClient
from server import *


@pytest.fixture
def client():
    return TestClient(app)


def test_search_endpoint(client):
    response = client.post("/faq/search", json={"text": "测试查询"})
    assert response.status_code == 200
    assert "query_vec" in response.json()
    assert isinstance(response.json()["query_vec"], str)


def test_search_endpoint_invalid_input(client):
    response = client.post("/faq/search", json={})
    assert response.status_code == 422


def test_search_endpoint_server_error(client, monkeypatch):
    def mock_get_embedding(*args, **kwargs):
        raise Exception("模拟服务器错误")

    monkeypatch.setattr("server.get_embedding", mock_get_embedding)
    response = client.post("/faq/search", json={"text": "测试查询"})
    assert response.status_code == 500
