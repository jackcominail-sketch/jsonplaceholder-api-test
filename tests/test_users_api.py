# -*- coding: utf-8 -*-
"""
test_users_api.py
JSONPlaceholder /users 接口测试
覆盖 GET / POST / PUT / DELETE
"""
import pytest


def test_get_user_by_id(base_url, api_session):
    """GET /users/1 - 查单个用户"""
    url = f"{base_url}/users/1"
    response = api_session.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "email" in data
    assert "address" in data


@pytest.mark.parametrize("user_id,expected_status", [
    (1, 200), (5, 200), (10, 200), (0, 404), (11, 404),
])
def test_get_user_various_ids(base_url, api_session, user_id, expected_status):
    """参数化测 GET /users/{id}"""
    url = f"{base_url}/users/{user_id}"
    response = api_session.get(url)
    assert response.status_code == expected_status


def test_get_all_users(base_url, api_session):
    """GET /users - 查所有用户"""
    url = f"{base_url}/users"
    response = api_session.get(url)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10


def test_create_user(base_url, api_session):
    """POST /users - 新增用户"""
    url = f"{base_url}/users"
    payload = {
        "name": "测试用户",
        "username": "testuser",
        "email": "test@test.com",
    }
    response = api_session.post(url, json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "测试用户"
    assert "id" in data


def test_update_user(base_url, api_session):
    """PUT /users/1 - 修改用户"""
    url = f"{base_url}/users/1"
    payload = {
        "id": 1,
        "name": "改名了",
        "username": "Bret",
        "email": "new@test.com",
    }
    response = api_session.put(url, json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "改名了"


def test_delete_user(base_url, api_session):
    """DELETE /users/1 - 删除用户"""
    url = f"{base_url}/users/1"
    response = api_session.delete(url)
    assert response.status_code == 200
