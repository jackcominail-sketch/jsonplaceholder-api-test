# -*- coding: utf-8 -*-
"""
test_albums_api.py
JSONPlaceholder /albums 接口测试
覆盖 GET / POST / PUT / DELETE + 子资源 photos
"""
import pytest


# ========== GET 用例 ==========

def test_get_album_by_id(base_url, api_session):
    """GET /albums/1 - 查单个专辑"""
    url = f"{base_url}/albums/1"
    response = api_session.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "userId" in data
    assert "title" in data


@pytest.mark.parametrize("album_id,expected_status", [
    (1, 200), (10, 200), (50, 200), (100, 200),
    (0, 404), (101, 404), (-1, 404), (9999, 404),
])
def test_get_album_various_ids(base_url, api_session, album_id, expected_status):
    """参数化测 GET /albums/{id}"""
    url = f"{base_url}/albums/{album_id}"
    response = api_session.get(url)
    assert response.status_code == expected_status


def test_get_all_albums(base_url, api_session):
    """GET /albums - 查所有专辑"""
    url = f"{base_url}/albums"
    response = api_session.get(url)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100


def test_get_albums_by_userid(base_url, api_session):
    """GET /albums?userId=1 - 按用户过滤"""
    url = f"{base_url}/albums"
    response = api_session.get(url, params={"userId": 1})

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for album in data:
        assert album["userId"] == 1


def test_get_album_photos(base_url, api_session):
    """GET /albums/1/photos - 查专辑下的照片"""
    url = f"{base_url}/albums/1/photos"
    response = api_session.get(url)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for photo in data:
        assert photo["albumId"] == 1


# ========== POST 用例 ==========

def test_create_album(base_url, api_session):
    """POST /albums - 新增专辑"""
    url = f"{base_url}/albums"
    payload = {"title": "测试专辑", "userId": 1}
    response = api_session.post(url, json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "测试专辑"
    assert data["userId"] == 1
    assert "id" in data


def test_create_album_missing_title(base_url, api_session):
    """POST /albums - 缺 title 字段"""
    url = f"{base_url}/albums"
    payload = {"userId": 1}
    response = api_session.post(url, json=payload)
    assert response.status_code == 201  # JSONPlaceholder 不严格校验


def test_create_album_empty_body(base_url, api_session):
    """POST /albums - 空请求体"""
    url = f"{base_url}/albums"
    response = api_session.post(url, json={})
    assert response.status_code == 201


# ========== PUT 用例 ==========

def test_update_album(base_url, api_session):
    """PUT /albums/1 - 全量修改"""
    url = f"{base_url}/albums/1"
    payload = {"id": 1, "title": "新专辑名", "userId": 2}
    response = api_session.put(url, json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "新专辑名"
    assert data["userId"] == 2


# ========== DELETE 用例 ==========

def test_delete_album(base_url, api_session):
    """DELETE /albums/1 - 删除专辑"""
    url = f"{base_url}/albums/1"
    response = api_session.delete(url)
    assert response.status_code == 200


# ========== 性能用例 ==========

def test_album_response_time(base_url, api_session):
    """响应时间应 < 3 秒"""
    url = f"{base_url}/albums/1"
    response = api_session.get(url)
    assert response.elapsed.total_seconds() < 3
