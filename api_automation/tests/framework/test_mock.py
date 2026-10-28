"""
【框架自测】— Mock 子系统

Mock 的价值是"后端没就绪也能跑用例"，这里验证：
  1. Profile 能声明式地拦截指定端点
  2. 未注册的端点在不同模式下行为不同（宁可炸，不悄悄放行）
  3. 函数级 mock 用完即清，不污染其他用例
"""
import pytest

from api_automation.common import HttpClient
from api_automation.config import settings
from api_automation.framework.mock import MockServer, MockProfile, MockResponse, MockMode


class TestMockProfile:
    """Profile 定义能力"""

    def test_register_and_read_routes(self):
        profile = MockProfile("demo")
        profile.get("/system/user/list", MockResponse(200, {"code": 200, "rows": []}))
        profile.post("/system/user", {"status": 200, "body": {"code": 200, "msg": "操作成功"}})

        routes = profile.get_routes()
        assert len(routes) == 2
        assert routes[0].method == "GET"
        assert routes[1].method == "POST"

    def test_dict_response_is_coerced(self):
        """允许直接写字典，内部自动转成 MockResponse"""
        profile = MockProfile("demo")
        profile.delete("/system/user/1", {"status": 200, "body": {"code": 200}})
        assert isinstance(profile.get_routes()[0].response, MockResponse)

    def test_merge_profile(self):
        a = MockProfile("a")
        a.get("/a", {"status": 200})
        b = MockProfile("b")
        b.get("/b", {"status": 200})
        a.merge(b)
        assert len(a.get_routes()) == 2


class TestMockServer:
    """拦截行为"""

    @pytest.fixture
    def server(self):
        ms = MockServer(settings.BASE_URL)
        yield ms
        ms.stop()

    def test_registered_endpoint_is_intercepted(self, server):
        """命中注册路由 → 拿到假数据，不碰真实服务"""
        profile = MockProfile("demo")
        profile.get("/system/user/list",
                    MockResponse(200, {"code": 200, "msg": "mock", "rows": [{"userId": 1}], "total": 1}))
        server.load(profile)
        server.start(mode=MockMode.MOCK)

        client = HttpClient()
        try:
            resp = client.get("/system/user/list")
            assert resp.json()["msg"] == "mock"
            assert resp.json()["rows"][0]["userId"] == 1
        finally:
            client.close()

    def test_placeholder_route_is_intercepted(self, server):
        """/system/user/{id} 这种带占位符的路径也要拦得住"""
        profile = MockProfile("demo")
        profile.get("/system/user/{id}", MockResponse(200, {"code": 200, "msg": "detail"}))
        server.load(profile)
        server.start(mode=MockMode.MOCK)

        client = HttpClient()
        try:
            resp = client.get("/system/user/123")
            assert resp.json()["msg"] == "detail"
        finally:
            client.close()

    def test_unregistered_endpoint_raises_in_mock_mode(self, server):
        """MOCK 模式下未注册的端点直接报错 —— 宁可炸，也不能悄悄走真实网络"""
        server.start(mode=MockMode.MOCK)

        import requests
        client = HttpClient()
        try:
            with pytest.raises(Exception):
                client.get("/not/registered")
        finally:
            client.close()