# 若依后台管理系统 · 全链路自动化测试框架

> **Python 3.13 · pytest 9 · Selenium 4 · Allure · Jenkins**
>
> 以开源后台管理系统 **RuoYi-Vue（若依）** 为被测对象，从 0 到 1 搭建的「接口 + UI」双链路自动化测试框架。
> 接口用例 **44 条**、UI 用例 **10 条**，合计 **54 条**，覆盖 **11 个业务模块**。

---

## 一、项目概览

| 链路 | 核心目录 | 用例数 | 技术方案 |
| :-- | :-- | :--: | :-- |
| 接口自动化 | `Api/` `Api_scripts/` `base_Api/` | 44 | requests + pytest + Allure，Session 会话复用 + JWT 自动鉴权 |
| UI 自动化 | `scripts/` `page/` `base/` | 10 | Selenium + PO 设计模式 + 单例驱动 + 失败自动截图 |

覆盖模块：登录认证、用户管理、角色管理、菜单管理、部门管理、岗位管理、字典管理、参数配置、通知公告、操作日志、系统监控。

---

## 二、技术栈

| 分类 | 技术 |
| :-- | :-- |
| 开发语言 | Python 3.13 |
| 测试框架 | pytest 9、`pytest.mark.parametrize`、parameterized |
| 接口测试 | requests（Session 会话复用 + Bearer Token 鉴权） |
| UI 测试 | Selenium 4、WebDriverWait 显式等待、项目内置 chromedriver |
| 数据驱动 | YAML + PyYAML |
| 测试报告 | Allure（epic / feature / story / title 四级结构 + step 步骤） |
| 日志 | logging（控制台 + 文件双输出） |
| 持续集成 | Jenkins Declarative Pipeline + JUnit XML |

---

## 三、目录结构

```text
RuoYi-AutoTest/
├── Api/                  # 接口层：11 个业务模块 API 类
│   ├── CommonApi.py      #   通用接口（登录、用户、部门）
│   ├── UserApi.py / RoleApi.py / MenuApi.py / DeptApi.py
│   ├── PostApi.py / DictApi.py / ConfigApi.py / NoticeApi.py
│   └── MonitorApi.py / LogApi.py
├── Api_scripts/          # 接口用例层
│   ├── conftest.py       #   class 级 fixture：登录一次，全类复用 token
│   ├── test_*.py         #   8 个模块、共 44 条接口用例
│   └── *.yaml            #   12 份测试数据文件（数据驱动）
├── base_Api/             # 接口基础层
│   ├── base.py           #   Api_common：Session 复用 + 四种请求方法封装
│   └── yaml_untils.py    #   YAML 数据读取工具
├── scripts/              # UI 用例层
│   ├── conftest.py       #   浏览器生命周期 fixture
│   └── test_selenium_scripts.py   # 10 条 UI 用例
├── page/                 # UI 页面对象层（PO 模式）
├── base/                 # UI 基础层：Base 操作封装 / GetDriver 单例 / logs
├── logs/                 # 运行日志
├── screenshot/           # 断言失败自动截图
├── reports/  temps/      # Allure 报告产物 / 原始结果
├── Jenkinsfile           # Jenkins 声明式流水线
├── pytest.ini            # 用例路径、Allure 参数、12 个分类 marker
├── requirements.txt      # 依赖清单
└── Test_runall.py        # 一键执行用例并生成 Allure 报告
```

---

## 四、框架分层设计

| 层级 | 位置 | 职责 |
| :-- | :-- | :-- |
| 数据层 | `Api_scripts/*.yaml`、`base_Api/yaml_untils.py` | 测试数据与代码分离，YAML 读取为字典列表供参数化使用 |
| 基础层 | `base_Api/base.py` | `Api_common` 封装 Session、请求方法、鉴权、调试输出 |
| 接口层 | `Api/` | 一个业务模块一个 API 类，继承 `Api_common`，只负责「路径 + 参数」 |
| 用例层 | `Api_scripts/` | pytest 用例 + Allure 分层注解 + `with allure.step()` 步骤拆分 |
| 页面层 | `page/` | PO 页面对象，继承 `Base`，把元素定位与业务操作分开 |
| UI 基础层 | `base/` | `Base` 操作封装（等待/点击/输入/断言/截图）、`Getdriver` 单例驱动 |

接口链路调用关系：`用例层 → 接口层（Api/）→ 基础层（base_Api）→ 被测系统`。

---

## 五、核心特性

- **Session 复用 + JWT 自动鉴权**：`Api_common` 内部维护一个 `requests.Session`，通过 `set_token()` 注入 `Authorization: Bearer <token>`，后续所有请求自动携带；`conftest.py` 中的 `login_with_token` 为 class 级 fixture，**一个测试类只登录一次**，避免每个用例重复登录。
- **统一请求方法封装**：`send_get / send_post / send_put / send_delete` 统一拼接 base_url、合并请求头，并在控制台打印请求 URL、方法、请求头、状态码与响应体前 500 字符，接口排查无需额外加断点。
- **绕过代理干扰**：构造 Session 时设置 `trust_env = False`，不受系统代理和环境变量影响，保证 CI 与本地结果一致。
- **YAML 数据驱动**：`base_Api/yaml_untils.py` 将 YAML 解析为用例数据列表，配合 `@pytest.mark.parametrize` 实现「新增用例只改数据文件、不改代码」。
- **Allure 四级报告**：`@allure.epic` 项目 → `@allure.feature` 模块 → `@allure.story` 场景 → `@allure.title` 用例，关键校验用 `allure.step()` 拆成可视步骤，报告可直接作为测试记录交付。
- **失败自动留证**：UI 断言失败时自动截图，截图以时间戳命名归档到 `screenshot/`，同时把断言信息与截图路径写入日志，复现问题有据可查。
- **marker 分组执行**：`pytest.ini` 定义 `smoke / login / user / role / menu / dept / dict / config / notice / monitor / log / selenium` 共 12 个 marker，支持只跑冒烟或某个业务模块。
- **浏览器驱动单例**：`Getdriver.Get_driver()` 为类级单例，由 class 级 fixture 负责启动与退出，避免每条用例重启浏览器；启动参数关闭自动化特征（`excludeSwitches: enable-automation`、`disable-blink-features=AutomationControlled`）与显式等待兜底。
- **Jenkins 流水线**：`Prepare`（清理旧环境 → 建虚拟环境 → 安装依赖）→ `Test`（清理历史报告 → pytest 输出 JUnit XML 与 Allure 结果），构建后归档测试结果并清理 `__pycache__`、`.pytest_cache`，配置 30 分钟超时、保留 20 次构建记录、禁止并发构建。

---

## 六、快速开始

### 1. 环境要求

- Python 3.10+
- 被测系统已启动：RuoYi-Vue 后端 `http://127.0.0.1:8081`，前端 `http://localhost:80`
- Chrome 浏览器（UI 用例需要），项目根目录已内置 `chromedriver.exe`

### 2. 安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 按需修改

- 接口地址：`base_Api/base.py` 中的 `self.base_url`
- 前端地址：`base/GetDriver.py` 中的 `driver.get(...)`
- 登录账号：`Api_scripts/conftest.py` 的 `login_with_token` fixture（默认使用若依演示账号）

---

## 七、运行方式

```bash
# 全量用例（接口 + UI）
pytest

# 只跑接口自动化
pytest Api_scripts -v

# 只跑 UI 自动化
pytest scripts -v

# 按 marker 跑子集
pytest -m smoke
pytest -m "user or role"

# 一键执行并生成 Allure 报告
python Test_runall.py
```

---

## 八、报告与产物

```bash
allure serve temps                              # 本地起服务直接查看
allure generate ./temps -o ./reports --clean    # 生成静态 HTML 报告
```

| 产物 | 路径 |
| :-- | :-- |
| 运行日志 | `logs/` |
| 失败截图 | `screenshot/` |
| Allure 原始结果 | `temps/` |
| Allure 报告 | `reports/` |
| JUnit XML（Jenkins 归档） | `reports/junit.xml` |

---

## 九、测试覆盖

### 接口自动化（44 条）

| 模块 | 用例数 | 覆盖场景 |
| :-- | :--: | :-- |
| 登录认证 | 5 | 正常登录返回 token、密码错误、用户名为空、密码为空、不存在用户 |
| 用户管理 | 7 | 用户列表、按用户名搜索、按手机号搜索、按状态筛选（正常/停用）、当前用户信息、路由菜单 |
| 角色管理 | 5 | 角色列表、按角色名称搜索、按状态搜索、角色详情、已授权用户列表 |
| 菜单管理 | 5 | 部门/菜单列表、部门树与菜单树下拉结构、按角色 ID 查询菜单树 |
| 岗位与字典 | 6 | 岗位列表、按岗位名称/编码搜索、字典类型列表、性别字典、通知类型字典 |
| 参数与公告 | 7 | 参数配置列表、按名称/键名搜索、刷新缓存、公告列表、按标题/类型搜索 |
| 监控与日志 | 8 | 服务器信息、在线用户、定时任务、Redis 缓存信息、缓存名称、登录日志、操作日志、按模块搜日志 |
| 数据驱动登录链路 | 1 | YAML 参数化登录 → 提取 token → 串联查询部门接口（接口链路串联） |

### UI 自动化（10 条）

| 用例 | 场景 |
| :-- | :-- |
| TC01 | 正确账号密码登录成功 |
| TC02 | 进入用户管理页面并显示用户列表 |
| TC03 | 进入角色管理页面并显示角色列表 |
| TC04 | 进入菜单管理页面并展开菜单树 |
| TC05 | 进入部门管理页面并显示部门树 |
| TC06 | 进入通知公告页面并显示公告列表 |
| TC07 | 进入在线用户页面查看在线用户 |
| TC08 | 进入服务监控页面查看服务器信息 |
| TC09 | 进入缓存监控页面查看缓存信息 |
| TC10 | 打开新增用户弹窗并取消操作 |

---

## 十、后续规划

- 补充接口「增删改」链路的用例，并加入数据自动清理，保证用例可重复执行
- 将各模块 YAML 数据文件全部接入 `parametrize`，实现全量数据驱动
- 引入接口依赖与前置数据构造，减少用例之间的耦合
- 在 Jenkins 中接入 Allure 插件，实现构建后直接查看趋势报告
- 补充接口响应字段的 JSON Schema 校验，从「字段存在」升级到「结构正确」

---

> 本项目为个人自动化测试实践项目，被测对象为开源 RuoYi-Vue 后台管理系统。