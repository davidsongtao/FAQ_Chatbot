"""
Description: 单元测试重构的es_index
    
-*- Encoding: UTF-8 -*-
@File     ：test_es_index.py
@Author   ：King Songtao
@Time     ：2024/8/9 下午4:54
@Contact  ：king.songtao@gmail.com
"""
import pytest
import json
from unittest.mock import Mock, patch, call
from elasticsearch import *
from vectorstore.es_index import *
from config.log_config import *


@pytest.fixture
def mock_es():
    return Mock(spec=Elasticsearch)


@pytest.fixture
def mock_param():
    param = Mock(spec=ParameterConfig)
    param.es_index_name = "test_index"
    param.es_index_batch_size = 2
    param.data_file_path = "test_data.json"
    return param


@pytest.fixture
def sample_data():
    return [
        {
            "question": "test question 1",
            "similar_question": ["similar 1", "similar 2"],
            "answer": "test answer 1"
        },
        {
            "question": "test question 2",
            "similar_question": ["similar 3", "similar 4"],
            "answer": "test answer 2"
        }
    ]


def test_create_index(mock_es, mock_param):
    with patch('vectorstore.es_index.es', mock_es), \
            patch('vectorstore.es_index.param', mock_param), \
            patch('vectorstore.es_index.click.confirm', return_value=True):
        mock_es.indices = Mock()
        mock_es.indices.exists.return_value = False
        mock_es.indices.create.return_value = {"acknowledged": True}

        create_index()

        mock_es.indices.create.assert_called_once()
        assert mock_es.indices.create.call_args[1]['index'] == "test_index"


def test_read_json_file(mock_param, sample_data, tmp_path):
    test_file = tmp_path / "test_data.json"
    with open(test_file, 'w') as f:
        for item in sample_data:
            f.write(json.dumps(item) + '\n')

    with patch('vectorstore.es_index.param', mock_param), \
            patch('vectorstore.es_index.get_embedding', return_value=[0.1] * 1024):

        batches = list(read_json_file(str(test_file)))

        assert len(batches) == 2  # 因为我们有4条数据，每批2条
        assert len(batches[0]) == 2
        assert len(batches[1]) == 2

        # 检查返回的数据结构是否正确
        for batch in batches:
            for item in batch:
                assert '_index' in item
                assert '_source' in item
                assert 'question' in item['_source']
                assert 'similar_question' in item['_source']
                assert 'similar_question_vector' in item['_source']
                assert 'answer' in item['_source']


def test_batch_insert(mock_es, mock_param, sample_data, tmp_path):
    test_file = tmp_path / "test_data.json"
    with open(test_file, 'w') as f:
        for item in sample_data:
            f.write(json.dumps(item) + '\n')

    # 模拟 helpers.bulk 函数
    mock_bulk = Mock(return_value=(2, []))  # 假设每次插入2条数据

    # 模拟 logger
    mock_logger = Mock()

    with patch('vectorstore.es_index.es', mock_es), \
            patch('vectorstore.es_index.param', mock_param), \
            patch('vectorstore.es_index.get_embedding', return_value=[0.1] * 1024), \
            patch('elasticsearch.helpers.bulk', mock_bulk), \
            patch('vectorstore.es_index.logger', mock_logger):  # 添加这行来模拟 logger

        batch_insert(str(test_file))

        # 检查 bulk 函数被调用的次数
        assert mock_bulk.call_count == 2  # 因为我们有4条数据，每批2条，所以应该调用2次

        # 检查 logger.info 被正确调用
        mock_logger.info.assert_has_calls([
            call("数据批量插入成功！", (2, [])),
            call("数据批量插入成功！", (2, []))
        ])

        # 确保没有错误被记录
        mock_logger.error.assert_not_called()


if __name__ == '__main__':
    pytest.main()
