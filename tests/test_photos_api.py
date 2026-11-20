# -*- coding: utf-8 -*-
"""
test_photos_api.py
JSONPlaceholder /photos 接口测试
覆盖 GET / POST / PUT / DELETE + 过滤
"""
import pytest


# ========== GET 用例 ==========

def test_get_photo_by_id(base_url, api_session):
    """GET /photos/1 - 查单个照片"""
    url = f"{base_url}/photos/1"
    response = api_session.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "albumId" in data
    assert "title" in data
    assert "url" in data
    assert "thumbnailUrl" in data


@pytest.mark.parametrize("photo_id,expected_status", [
    (1, 200), (100, 200), (1000, 200), (5000, 200),
    (0, 404), (5001, 404), (-1, 404), (99999, 404),
])
def test_get_photo_various_ids(base_url, api_session, photo_id, expected_status):
    """参数化测 GET /photos/{id}"""
    url = f"{base_url}/photos/{photo_id}"
    response = api_session.get(url)
    assert response.status_code == expected_status


def test_get_all_photos(base_url, api_session):
    """GET /photos - 查所有照片"""
    url = f"{base_url}/photos"
    response = api_session.get(url)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5000


def test_get_photos_by_albumid(base_url, api_session):
    """GET /photos?albumId=1 - 按专辑过滤"""
    url = f"{base_url}/photos"
    response = api_session.get(url, params={"albumId": 1})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 50, "albumId=1 应有 50 张照片"
    for photo in data:
        assert photo["albumId"] == 1


# ========== POST 用例 ==========

def test_create_photo(base_url, api_session):
    """POST /photos - 新增照片"""
    url = f"{base_url}/photos"
    payload = {
        "title": "测试照片",
        "url": "https://example.com/photo.jpg",
        "thumbnailUrl": "https://example.com/thumb.jpg",
        "albumId": 1,
    }
    response = api_session.post(url, json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "测试照片"
    assert "id" in data


def test_create_photo_missing_url(base_url, api_session):
    """POST /photos - 缺 url 字段"""
    url = f"{base_url}/photos"
    payload = {"title": "无URL照片", "albumId": 1}
    response = api_session.post(url, json=payload)
    assert response.status_code == 201


# ========== PUT 用例 ==========

def test_update_photo(base_url, api_session):
    """PUT /photos/1 - 全量修改"""
    url = f"{base_url}/photos/1"
    payload = {
        "id": 1,
        "albumId": 1,
        "title": "新标题",
        "url": "https://new.com/photo.jpg",
        "thumbnailUrl": "https://new.com/thumb.jpg",
    }
    response = api_session.put(url, json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "新标题"


# ========== DELETE 用例 ==========

def test_delete_photo(base_url, api_session):
    """DELETE /photos/1 - 删除照片"""
    url = f"{base_url}/photos/1"
    response = api_session.delete(url)
    assert response.status_code == 200


# ========== 性能用例 ==========

def test_photo_response_time(base_url, api_session):
    """响应时间应 < 3 秒"""
    url = f"{base_url}/photos/1"
    response = api_session.get(url)
    assert response.elapsed.total_seconds() < 3
