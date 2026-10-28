# 若依（RuoYi-Vue）后台管理系统 · 接口 + UI 全链路自动化测试框架

> **Python 3.13 · pytest 9 · requests · Allure · Selenium 4 · Jenkins**
>
> 被测对象：开源后台管理系统 **RuoYi-Vue（若依）** 定制版（后端 `http://localhost:8081`）
> 接口链路基于自研框架（数据隔离 / 契约中心 / Mock / 自动清理），UI 链路沿用 Selenium PO 模式。

---

## 一、项目概览

| 链路 | 核心目录 | 技术方案 |
| :-- | :-- | :-- |
| 接口自动化 | `api_automation/` 下的 `apis/` `tests/` `common/` `framework/` `models/` `data/` | requests + pytest + Allure，自研测试框架（隔离子系统 + 契约中心 + Mock 子系统） |
| UI 自动化 | `ui_automation/` 下的 `scripts/` `page/` `base/` | Selenium + PO 设计模式 + 单例驱动 + 失败自动截图 |

接口覆盖模块：登录认证、用户、角色、菜单、部门、岗位、字典、参数配置、通知公告、
个人中心、在线用户、定时任务、调度日志、缓存监控、服务监控、登录日志、操作日志、代码生成、通用文件。

> 接口清单与字段约束的权威来源见同目录下的 `RuoYi-Vue接口文档.md`（147 个接口 / 20 张表）。

---

## 二、技术栈

| 分类 | 技术 |
| :-- | :-- |
| 开发语言 | Python 3.13 |
| 测试框架 | pytest 9、`pytest.mark.parametrize` 数据驱动 |
| 接口测试 | requests（Session 会话复用 + Bearer Token 鉴权） |
| 契约校验 | jsonschema（端点级响应结构自动校验）+ Pydantic（请求体建模） |
| Mock | requests_mock（拦截层与真实请求同库，mock/live 无感切换） |
| 数据构造 | Faker + 自研数据工厂 `data/factory.py` |
| 断言 | 自研 `AssertionEngine`（链式断言 + JSONPath + DeepDiff + JSON Schema） |
| 测试报告 | Allure（epic / feature / story / title 四级结构 + step 步骤） |
| 日志 | loguru（控制台 + 文件双输出，支持结构化 JSON） |
| 持续集成 | Jenkins Declarative Pipeline + JUnit XML |

---

## 三、目录结构

```text
RuoYi-AutoTest/
├── api_automation/         # 接口自动化
│   ├── apis/               #   接口层：13 个模块的 API 封装，只描述「路径 + 参数」
│   │   ├── auth_api.py     #     登录 / 验证码 / getInfo / getRouters / 登出
│   │   ├── user_api.py     #     用户 CRUD、状态、重置密码、角色分配、部门树
│   │   ├── role_api.py / menu_api.py / dept_api.py / post_api.py
│   │   ├── dict_api.py     #     字典类型 + 字典数据（两个 Controller）
│   │   ├── config_api.py / notice_api.py / profile_api.py
│   │   ├── monitor_api.py  #     在线用户 / 定时任务 / 调度日志 / 缓存 / 服务监控 / 登录日志 / 操作日志
│   │   ├── gen_api.py / common_api.py
│   │   └── __init__.py     #     单例导出 + ALL_API_SINGLETONS（会话绑定用）
│   ├── common/             #   基础层：与业务无关的通用能力
│   │   ├── http_client.py  #     requests 封装：URL 拼接、超时、日志、契约校验挂钩
│   │   ├── base_api.py     #     API 基类：service_path + get/post/put/patch/delete
│   │   ├── assertion.py    #     断言引擎：链式调用 + JSONPath + DeepDiff + Schema
│   │   ├── retry.py        #     重试装饰器（只重试环境类异常，断言失败不重试）
│   │   └── logger.py       #     日志（请求/响应统一打印与脱敏）
│   ├── framework/          #   框架核心：三个子系统
│   │   ├── isolation/      #     数据隔离：TestContext / TestIdentity / DataLifecycle
│   │   ├── contract/       #     契约中心：端点 Schema 注册 + 自动校验
│   │   └── mock/           #     Mock：MockProfile / MockResponse / MockServer / MockMode
│   ├── models/             #   数据模型与契约：Pydantic 请求模型 + 76 条端点响应 Schema
│   ├── data/               #   数据层
│   │   ├── factory.py      #     数据工厂（字段约束与实体注解一一对应）
│   │   └── test_data/*.yaml  #   12 份数据驱动文件（参数校验 / 边界值 / 查询条件）
│   ├── tests/              #   用例层
│   │   ├── fixtures/       #     共享 fixture：登录身份 + 「新建即清理」的数据
│   │   ├── scenarios/      #     业务场景用例（按模块拆分，14 个文件）
│   │   ├── contracts/      #     契约测试（从注册中心自动生成）
│   │   └── framework/      #     框架自测（重试 / 隔离 / 契约 / Mock）
│   ├── config/             #   全局配置中心（pydantic-settings + .env）
│   └── conftest.py         #   会话、隔离、Mock、清理、Allure 环境信息的总装配
│
├── ui_automation/          # UI 自动化
│   ├── scripts/            #   UI 用例层（Selenium）
│   ├── page/               #   页面对象层（PO 模式）
│   └── base/               #   Base 操作封装 / GetDriver 单例 / logs
│
├── reports/                # 测试产物（已 gitignore）
│   ├── allure-results/     #   pytest 产出的 Allure 原始 JSON（可随时删除）
│   └── allure-report/      #   allure generate 产出的 HTML 报告
├── logs/                   # 运行日志（已 gitignore）
├── pytest.ini              # 用例路径、Allure 参数、标记注册
├── Test_runall.py          # 一键执行 + 生成 Allure HTML
├── Jenkinsfile             # Jenkins 流水线
├── requirements.txt        # 依赖清单
└── .env.example            # 环境变量模板（复制为 .env 使用）
```

---

## 四、框架分层设计

| 层级 | 位置 | 职责 |
| :-- | :-- | :-- |
| 用例层 | `api_automation/tests/scenarios/` | Allure 分层注解 + 场景编排 + 断言 |
| 夹具层 | `api_automation/tests/fixtures/` | 登录身份、造数与自动清理，用例只关心业务 |
| 接口层 | `api_automation/apis/` | 一个模块一个类，只负责「路径 + 参数」，不含断言 |
| 基础层 | `api_automation/common/` | HTTP 客户端、断言引擎、重试、日志 |
| 框架层 | `api_automation/framework/` | 数据隔离、契约中心、Mock 三大子系统 |
| 模型层 | `api_automation/models/` | 请求体建模 + 端点响应 Schema 注册 |
| 数据层 | `api_automation/data/` | 数据工厂 + YAML 数据驱动 |
| UI 页面层 | `ui_automation/page/` | 页面对象：定位器 + 页面动作 |
| UI 基础层 | `ui_automation/base/` | 浏览器驱动单例、等待/点击/输入/断言/截图 |

调用关系：`用例层 → 夹具层 → 接口层 → 基础层（HttpClient）→ 契约中心自动校验 → 被测系统`。

---

## 五、核心特性

### 1. 数据隔离与自动清理

每条用例运行都会拿到一个唯一的 `TestContext`：

- `context.tag(payload)` 给 `userName` 等字段加唯一前缀，**并发执行也不会撞数据**；
- `context.lifecycle.created(...)` 登记本次创建的资源；
- 用例结束（含失败）自动按依赖顺序回调删除接口清理，`--no-cleanup` 可保留现场用于排查。

所有接口模块共用同一个 `HttpClient`，登录态只设置一次即全局生效 —— 这样清理请求才带得上鉴权头。

### 2. 契约中心（接口结构变更自动拦截）

`models/__init__.py` 中登记了 76 条端点的响应 JSON Schema，`HttpClient` 每次收到响应都会自动匹配并校验：

- 后端字段改名、必填字段丢失、类型变化会被立刻发现；
- 静态路径优先于占位符路径（`/system/user/list` 不会被 `/system/user/{id}` 抢走）；
- 契约中心默认不阻断业务流，只告警，避免"结构变化"直接让整轮用例崩掉。

### 3. Mock 子系统

一套用例，`--mode live|mock|hybrid` 三种模式无感切换：

- `live`：全量打真实服务；
- `mock`：未注册的端点直接报错（**宁可炸，也不悄悄走真实网络**）；
- `hybrid`：注册了的走 Mock，没注册的透传。

后端未就绪时，可以先用 Mock 把用例链路和断言跑通。

### 4. 业务码约定（重要）

若依的约定是 **HTTP 状态码恒为 200，业务结果靠 `body.code` 表达**：

| 场景 | HTTP | body.code | 说明 |
| :-- | :-- | :-- | :-- |
| 成功 | 200 | 200 | `msg = 操作成功` |
| 参数校验失败 / 业务异常 | 200 | 500 | 由 `GlobalExceptionHandler` 统一返回 |
| 未认证 | 200 | 401 | 认证失败提示带请求路径 |
| 权限不足 | 200 | 403 | `没有权限，请联系管理员授权` |

用例统一断言 `HTTP 200 + 业务 code`，这正是需要被固化的接口契约。

### 5. 验证码开关

若依默认开启算术验证码（`sys.account.captchaEnabled=true`），接口自动化无法识别图片。
测试库执行 `UPDATE sys_config SET config_value='false' WHERE config_key='sys.account.captchaEnabled'`。
框架用 `.env` 的 `CAPTCHA_ENABLED` 控制：开启时登录类用例 `skip` 而不是假通过。

### 6. 重试策略

只对**环境类异常**（连接失败 / 超时 / 连接中断）重试，断言失败不重试 ——
断言失败说明被测系统行为不符合预期，重试只会掩盖缺陷。

---

## 六、快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 准备被测系统（后端默认 8081）
#    启动 RuoYi-Vue 后端，并确认数据库已初始化

# 3. 配置环境变量
copy .env.example .env      # Windows
# 按实际情况修改 BASE_URL / 测试账号 / CAPTCHA_ENABLED

# 4. 跑用例
pytest                                  # 全量（接口 + UI）
pytest api_automation/tests             # 只跑接口
pytest api_automation/tests/scenarios/test_auth.py -v  # 跑单个模块
pytest -m smoke                         # 只跑冒烟
pytest -m "P0"                          # 只跑核心用例

# 5. 生成并查看 Allure 报告
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
# 只想临时看一眼，不落地 HTML：allure serve reports/allure-results
```

### Allure 报告目录约定

原始结果和 HTML 报告必须是**两个平级目录**，不能把 `allure-results` 放进报告目录里：

```text
reports/
├── allure-results/   # pytest 写出的原始 JSON
└── allure-report/    # allure generate 写出的 HTML
```

原因：`allure generate ... -o reports --clean` 会清空输出目录。如果原始结果也放在
`reports/` 下面，清理输出时会把输入一起删掉，报告就再也生成不出来。

四处配置已经统一：

| 位置 | 作用 |
| :-- | :-- |
| `pytest.ini` 的 `--alluredir=reports/allure-results --clean-alluredir` | 每次运行前清空旧结果，避免多轮结果混在一起 |
| `api_automation/config` 的 `ALLURE_RESULTS_DIR` / `ALLURE_REPORT_DIR` | Python 代码里读取的统一绝对路径 |
| `Test_runall.py` | 跑完 pytest 后生成 `reports/allure-report` |
| `Jenkinsfile` | JUnit 与 Allure 结果都发布自 `reports/` |

### 命令行参数

| 参数 | 说明 |
| :-- | :-- |
| `--mode live\|mock\|hybrid` | 测试模式，默认 `live` |
| `--base-url http://ip:8081` | 临时覆盖被测地址（不改 `.env` 也能切环境） |
| `--no-cleanup` | 保留本次创建的数据，便于排查问题 |

---

## 七、用例组织

14 个场景文件 + 4 个框架自测文件，共 **198 条用例**：

| 文件 | 覆盖内容 |
| :-- | :-- |
| `test_auth.py` | 登录成功/失败参数化、验证码、登录态、认证与鉴权语义 |
| `test_user.py` | 新增参数校验与边界值、列表查询、完整生命周期、状态、重置密码、角色分配 |
| `test_role.py` | 角色 CRUD、参数校验、状态、数据权限、授权用户列表 |
| `test_menu.py` | 菜单 CRUD、树结构、下拉树、排序 |
| `test_dept.py` | 部门 CRUD、树结构、排除节点、排序 |
| `test_post.py` | 岗位 CRUD、参数校验 |
| `test_dict.py` | 字典类型（含 `^[a-z][a-z0-9_]*$` 正则约束）+ 字典数据联动 |
| `test_config.py` | 参数 CRUD、按键名取值、缓存刷新 |
| `test_notice.py` | 公告 CRUD、XSS 拦截、顶部通知、已读标记（含幂等） |
| `test_profile.py` | 个人信息读取/修改（**自动还原**）、密码修改负向用例 |
| `test_monitor.py` | 在线用户、缓存、服务监控、登录/操作/调度日志、定时任务生命周期 |
| `test_gen.py` | 代码生成只读查询（不写入磁盘，避免污染工程目录） |
| `test_common_upload.py` | 文件上传（内存字节流，不依赖磁盘样本）、非法扩展名拦截 |
| `test_authorization.py` | 越权访问/写入/删除（带正向对照，避免假通过） |
| `test_idempotency.py` | 重复删除、重复提交、状态变更幂等、读操作稳定性 |
| `tests/framework/*` | 重试生效性、隔离与清理、契约匹配优先级、Mock 拦截 |
| `tests/contracts/*` | 注册 Schema 合法性、required 定义完整性、重复注册检测、覆盖率 |

### 标记（marker）

`smoke` `regression` `P0` `P1` `P2` `slow` `auth` `contract` `lifecycle`
以及模块标记 `login` `user` `role` `menu` `dept` `post` `dict` `config` `notice` `monitor` `selenium`。

---

## 八、UI 自动化（沿用原有实现）

```bash
pytest ui_automation/scripts -m selenium
```

`page/` 采用 PO 模式，`base/GetDriver.py` 为单例驱动，`base/base.py` 封装等待/点击/输入/断言/失败截图。

---

## 九、本次改造说明

- **接口链路整体替换**：原 `Api/` `Api_scripts/` `base_Api/` 三个目录已归档到 `api_automation/_legacy_interface/`（保留备查，不再参与执行）；接口用例全部迁移到 `api_automation/tests/`，由自研框架承载。
- **UI 链路保持不变**：`ui_automation/scripts/` `ui_automation/page/` `ui_automation/base/` 只调整了目录归属，仍在 `pytest.ini` 的 `testpaths` 中。
- **修复了两个框架缺陷**（已补充回归用例，见 `tests/framework/`）：
  1. `common/retry.py` 把 `stop_after_attempt(...)` 误传给 `retry=` 参数，导致**重试完全不生效**；已改为 `stop=` + `retry=retry_if_exception_type(...)`。
  2. `framework/isolation` 的清理逻辑硬编码 `client.post(...)`，导致 DELETE 类清理接口**全部静默失败、脏数据残留**；已改为按登记的方法动态派发。
- **补充契约匹配优先级**：静态路径优先于占位符路径，避免列表响应被详情 Schema 误判产生假告警。

---

## 十、后续可扩展方向

- **数据落库校验**：`config` 中已预留 `DB_ENABLED / DB_HOST ...`，可接 PyMySQL 做"接口 + 数据库"双层断言。
- **性能基线**：在关键接口上做响应时间基线断言，识别性能回退。
- **契约覆盖率门禁**：用 `tests/contracts` 的覆盖率断言卡住新增接口未登记 Schema 的情况。
- **CI 门禁分级**：`-m smoke` 作为提交门禁，`-m regression` 作为每日全量。
