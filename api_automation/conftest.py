"""
conftest — 框架级测试基础设施（RuoYi-Vue 接口自动化）

pytest 启动时做三件事：
  1. 注册 models/ 里的端点契约 → 之后每个响应都会被自动校验结构
  2. 给每条用例一个唯一的 TestContext → 数据隔离 + 自动清理
  3. 按 --mode 启停 MockServer → mock / live 无感切换
"""
import shutil
import subprocess
from pathlib import Path

import pytest

from api_automation.common import HttpClient, logger
from api_automation.config import settings
from api_automation.framework import TestContext, MockServer, MockMode, registry

# tests/fixtures/ 下的模块不会被 pytest 自动加载，必须显式注册为插件
pytest_plugins = ["tests.fixtures.user_fixtures"]


# ==================== 配置阶段（收集用例前执行一次） ====================

def pytest_configure(config):
    """注册契约 + 写出 Allure 环境信息"""
    from api_automation.models import register_ruoyi_contracts

    count = register_ruoyi_contracts()
    logger.info(f"📋 [框架] 契约注册完成: {count} 条端点")

    allure_dir = getattr(config.option, "allure_report_dir", None) or str(settings.ALLURE_RESULTS_DIR)
    if allure_dir:
        env_file = Path(allure_dir) / "environment.properties"
        env_file.parent.mkdir(parents=True, exist_ok=True)
        env_file.write_text(
            f"Environment={settings.ENV}\n"
            f"BaseURL={settings.BASE_URL}\n"
            f"Contracts={count}\n",
            encoding="utf-8",
        )


# ==================== 命令行参数 ====================

def pytest_addoption(parser):
    parser.addoption("--mode", action="store", default="live",
                     choices=["live", "mock", "hybrid"],
                     help="测试模式: live=真实服务, mock=全部Mock, hybrid=混合")
    parser.addoption("--no-cleanup", action="store_true", default=False,
                     help="保留测试数据（调试用，不自动删除本次创建的数据）")
    parser.addoption("--base-url", action="store", default=None,
                     help="临时覆盖被测服务地址，如 http://192.168.1.10:8081")


def pytest_collection_modifyitems(config, items):
    """把 --base-url 覆盖到运行时配置上（在 fixture 建连之前生效）"""
    base_url = config.getoption("--base-url")
    if base_url:
        settings.BASE_URL = base_url.rstrip("/")
        logger.info(f"⚙️  [框架] BASE_URL 已被命令行覆盖: {settings.BASE_URL}")


# ==================== Session 级 ====================

@pytest.fixture(scope="session")
def test_mode(request) -> MockMode:
    return MockMode(request.config.getoption("--mode"))


@pytest.fixture(scope="session", autouse=True)
def session_banner(test_mode):
    """打印环境信息横幅"""
    logger.info("=" * 60)
    logger.info(f"🚀 环境: {settings.ENV}  |  🎯 地址: {settings.BASE_URL}")
    logger.info(f"🎭 模式: {test_mode.value}  |  📋 契约: {registry.count()} 条")
    logger.info("=" * 60)
    yield
    logger.info("🏁 全部测试执行完毕")


@pytest.fixture(scope="session")
def global_client() -> HttpClient:
    """session 级共享客户端：用例间复用连接，退出时统一关闭"""
    client = HttpClient()
    yield client
    client.close()


@pytest.fixture(scope="session", autouse=True)
def bind_api_client(global_client):
    """
    把所有接口模块的 client 绑定到同一个 session 会话上。

    必须这样做：否则登录态只存在于某一个模块自己的会话里，
    而测试结束后的自动清理走的是 global_client，
    发出的删除请求不带鉴权头 → 清理静默失败、脏数据残留。
    """
    from api_automation.apis import ALL_API_SINGLETONS
    for api in ALL_API_SINGLETONS:
        api.client = global_client

    yield


@pytest.fixture(scope="session")
def mock_server(test_mode) -> MockServer:
    ms = MockServer(settings.BASE_URL)
    if test_mode in (MockMode.MOCK, MockMode.HYBRID):
        ms.start(mode=test_mode)
    yield ms
    ms.stop()


@pytest.fixture
def mock_session(mock_server):
    """
    函数级 Mock，用完自动清理，不污染其他用例。

    用法：
        def test_mock_xxx(mock_session):
            profile = MockProfile("demo")
            profile.get("/system/user/list", MockResponse(200, body={"code": 200, "rows": []}))
            mock_session.load(profile)
            ...
    """
    yield mock_server
    mock_server.reset()


# ==================== 测试级：隔离 + 生命周期 ====================

@pytest.fixture
def context(request, global_client) -> TestContext:
    """
    每条用例独享一个上下文：

      - context.identity     本次运行的唯一标识（数据打标用）
      - context.tag(data)    给 payload 的 userName 等字段加唯一前缀
      - context.lifecycle    登记本次创建的数据，用例结束按依赖顺序自动清理
    """
    ctx = TestContext(request.node.name, global_client)
    yield ctx
    if not request.config.getoption("--no-cleanup"):
        ctx.cleanup()


@pytest.fixture
def api_client(global_client) -> HttpClient:
    """原始 HTTP 客户端（不带任何业务封装）"""
    return global_client


# ==================== 收尾：把原始结果编译成 HTML ====================

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """
    pytest 只把结果写成 reports/allure-results 下的 JSON，不会生成 HTML。
    这里补上 allure generate，否则 reports/allure-report 会一直停留在旧版本。
    """
    config = session.config
    if config.option.collectonly:
        return

    results_dir = getattr(config.option, "allure_report_dir", None)
    if not results_dir:
        return

    results = Path(results_dir).resolve()
    if not any(results.glob("*-result.json")):
        return

    report_dir = Path(settings.ALLURE_REPORT_DIR)
    allure_cli = shutil.which("allure")
    if not allure_cli:
        logger.warning("⚠️  [框架] 未找到 allure 命令，跳过 HTML 报告生成")
        return

    try:
        result = subprocess.run(
            [allure_cli, "generate", str(results), "-o", str(report_dir), "--clean"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
    except OSError as exc:
        logger.warning(f"⚠️  [框架] Allure 报告生成失败: {exc}")
        return

    if result.returncode == 0:
        logger.info(f"📊 [框架] Allure 报告已更新: {report_dir / 'index.html'}")
    else:
        detail = (result.stderr or result.stdout or "").strip().splitlines()
        logger.warning(f"⚠️  [框架] Allure 报告生成失败(exit={result.returncode}): {detail[-1] if detail else ''}")
