# JSONPlaceholder API 自动化测试项目

## 项目简介

基于 [JSONPlaceholder](https://jsonplaceholder.typicode.com/)（在线假 REST API）的接口自动化测试项目。使用 Python + Pytest + Requests 搭建分层测试框架，覆盖 GET / POST / PUT / PATCH / DELETE 五种 HTTP 方法，实现数据驱动、三层断言、HTML 报告生成。

## 技术栈

- **语言**：Python 3.10+
- **测试框架**：Pytest 8.x
- **HTTP 客户端**：requests + requests.Session（连接池复用）
- **报告**：pytest-html
- **并行执行**：pytest-xdist

## 项目结构

```
jsonplaceholder-api-test/
├── config.py              # 集中配置（base_url、阈值）
├── conftest.py            # Pytest fixture（base_url、api_session）
├── pytest.ini             # Pytest 配置（HTML 报告）
├── requirements.txt       # Python 依赖
├── .gitignore
├── tests/
│   ├── test_posts_api.py     # posts 接口用例（15 条）
│   ├── test_users_api.py     # users 接口用例（10 条）
│   ├── test_comments_api.py  # comments 接口用例（8 条）
│   ├── test_albums_api.py    # albums 接口用例（18 条）
│   └── test_photos_api.py    # photos 接口用例（16 条）
├── data/                  # 测试数据目录
└── reports/               # HTML 报告输出目录
```

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/你的用户名/jsonplaceholder-api-test.git
cd jsonplaceholder-api-test

# 2. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行测试
python -m pytest

# 5. 查看报告
# 打开 reports/report.html
```

## 测试覆盖

| 资源 | 接口数 | 用例数 | 覆盖方法 |
|------|--------|--------|---------|
| posts | 7 | 15 | GET/POST/PUT/PATCH/DELETE |
| users | 5 | 10 | GET/POST/PUT/DELETE |
| comments | 2 | 8 | GET/过滤 |
| albums | 6 | 18 | GET/POST/PUT/DELETE + 子资源 |
| photos | 4 | 16 | GET/POST/PUT/DELETE + 过滤 |
| **合计** | **24** | **67** | — |

## 用例设计方法

- **正常路径**：合法输入验证成功响应
- **异常路径**：不存在的 id、非法参数
- **边界值**：id=0、id=最大值、id=-1
- **数据驱动**：`@pytest.mark.parametrize` 参数化多组数据
- **三层断言**：状态码 → 响应结构 → 数据正确性
- **性能验证**：响应时间阈值断言

## 关键设计

### Fixture 复用
`conftest.py` 中定义 `api_session`（session scope），所有用例共用一个 `requests.Session`，复用 TCP 连接池，性能更优。

### 数据驱动
使用 `@pytest.mark.parametrize` 将测试数据与测试逻辑分离，一条用例函数覆盖多组数据。

### 集中配置
`config.py` 集中管理 base_url 和阈值，换环境只改一处。
