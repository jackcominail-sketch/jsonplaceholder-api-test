# -*- coding: utf-8 -*-
"""
conftest.py - Pytest 公共 fixture
所有 tests/ 下的用例自动可用这里的 fixture，不需要 import
"""
import pytest
import requests
from config import BASE_URL


@pytest.fixture(scope="session")
def base_url():
    """提供接口基础地址，整个测试会话只创建一次"""
    return BASE_URL


@pytest.fixture(scope="session")
def api_session():
    """提供复用的 requests.Session，连接池复用，性能更好"""
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    yield s
    s.close()
