# -*- coding: utf-8 -*-
"""
test_posts_api.py
JSONPlaceholder /posts 接口测试
覆盖 GET / POST / PUT / PATCH / DELETE
"""
import pytest


# ========== GET 用例 ==========

def test_get_post_by_id(base_url, api_session):
    """GET /posts/1 - 查单个 post，三层断言"""
    url = f"{base_url}/posts/1"
    response = api_session.get(url)

    # 第一层：状态码
    assert response.status_code == 200, f"期望 200，实际 {response.status_code}"

    # 第二层：响应结构
    data = response.json()
    assert "userId" in data, "缺少 userId 字段"
    assert "id" in data, "缺少 id 字段"
    assert "title" in data, "缺少 title 字段"
    assert "body" in data, "缺少 body 字段"

    # 第三层：数据正确性
    assert data["id"] == 1, f"期望 id=1，实际 {data['id']}"


@pytest.mark.parametrize("post_id,expected_status", [
    (1, 200),    # 正常
    (2, 200),    # 正常
    (3, 200),    # 正常
    (100, 200),  # 最大 id
    (0, 404),    # 不存在
    (9999, 404), # 不存在
    (-1, 404),   # 非法
])
def test_get_post_various_ids(base_url, api_session, post_id, expected_status):
    """参数化测 GET /posts/{id}"""
    url = f"{base_url}/posts/{post_id}"
    response = api_session.get(url)
    assert response.status_code == expected_status, \
        f"id={post_id}：期望 {expected_status}，实际 {response.status_code}"


def test_get_all_posts(base_url, api_session):
    """GET /posts - 查所有 posts"""
    url = f"{base_url}/posts"
    response = api_session.get(url)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), "应返回数组"
    assert len(data) == 100, f"期望 100 条，实际 {len(data)} 条"


def test_get_posts_by_userid(base_url, api_session):
    """GET /posts?userId=1 - 按用户过滤"""
    url = f"{base_url}/posts"
    response = api_session.get(url, params={"userId": 1})

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0, "userId=1 应有文章"
    for post in data:
        assert post["userId"] == 1, f"过滤结果含非 userId=1 的文章"


# ========== POST 用例 ==========

def test_create_post(base_url, api_session):
    """POST /posts - 新增文章"""
    url = f"{base_url}/posts"
    payload = {"title": "测试标题", "body": "测试正文", "userId": 1}
    response = api_session.post(url, json=payload)

    assert response.status_code == 201, f"期望 201，实际 {response.status_code}"
    data = response.json()
    assert data["title"] == "测试标题"
    assert data["body"] == "测试正文"
    assert data["userId"] == 1
    assert "id" in data, "返回应含自动生成的 id"


# ========== PUT 用例 ==========

def test_update_post_put(base_url, api_session):
    """PUT /posts/1 - 全量修改"""
    url = f"{base_url}/posts/1"
    payload = {"id": 1, "title": "新标题", "body": "新正文", "userId": 1}
    response = api_session.put(url, json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "新标题"
    assert data["body"] == "新正文"


# ========== PATCH 用例 ==========

def test_partial_update_post(base_url, api_session):
    """PATCH /posts/1 - 部分修改"""
    url = f"{base_url}/posts/1"
    payload = {"title": "只改标题"}
    response = api_session.patch(url, json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "只改标题"
    assert "body" in data, "PATCH 应保留未修改的字段"


# ========== DELETE 用例 ==========

def test_delete_post(base_url, api_session):
    """DELETE /posts/1 - 删除文章"""
    url = f"{base_url}/posts/1"
    response = api_session.delete(url)

    assert response.status_code == 200


# ========== 性能用例 ==========

def test_response_time(base_url, api_session):
    """响应时间应 < 3 秒"""
    url = f"{base_url}/posts/1"
    response = api_session.get(url)
    elapsed = response.elapsed.total_seconds()
    assert elapsed < 3, f"响应时间 {elapsed:.2f}s 超阈值"
