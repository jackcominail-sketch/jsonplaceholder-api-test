# -*- coding: utf-8 -*-
"""测试数据集中管理"""

# posts 接口测试数据
POST_IDS_VALID = [1, 2, 3, 100]
POST_IDS_INVALID = [0, 9999, -1]
POST_PAYLOAD_CREATE = {"title": "测试标题", "body": "测试正文", "userId": 1}
POST_PAYLOAD_UPDATE = {"id": 1, "title": "新标题", "body": "新正文", "userId": 1}

# users 接口测试数据
USER_IDS_VALID = [1, 5, 10]
USER_IDS_INVALID = [0, 11]
USER_PAYLOAD_CREATE = {
    "name": "测试用户",
    "username": "testuser",
    "email": "test@test.com",
}

# comments 接口测试数据
COMMENT_IDS_VALID = [1, 50, 100]
COMMENT_IDS_INVALID = [0, 501]
