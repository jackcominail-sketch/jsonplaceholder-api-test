# -*- coding: utf-8 -*-
"""
test_comments_api.py
JSONPlaceholder /comments 接口测试
覆盖 GET 查询和过滤
"""
import pytest


def test_get_comment_by_id(base_url, api_session):
    """GET /comments/1 - 查单个评论"""
    url = f"{base_url}/comments/1"
    response = api_session.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "email" in data
    assert "body" in data


@pytest.mark.parametrize("comment_id,expected_status", [
    (1, 200), (50, 200), (100, 200), (0, 404), (501, 404),
])
def test_get_comment_various_ids(base_url, api_session, comment_id, expected_status):
    """参数化测 GET /comments/{id}"""
    url = f"{base_url}/comments/{comment_id}"
    response = api_session.get(url)
    assert response.status_code == expected_status


def test_get_all_comments(base_url, api_session):
    """GET /comments - 查所有评论"""
    url = f"{base_url}/comments"
    response = api_session.get(url)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 500


def test_get_comments_by_postid(base_url, api_session):
    """GET /comments?postId=1 - 按文章过滤评论"""
    url = f"{base_url}/comments"
    response = api_session.get(url, params={"postId": 1})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5, "postId=1 应有 5 条评论"
    for comment in data:
        assert comment["postId"] == 1
