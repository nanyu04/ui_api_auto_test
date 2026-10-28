"""
【框架自测】— 契约校验子系统

契约子系统是"接口结构变更自动拦截"的抓手，
这里验证它的匹配、校验与优先级三条核心行为。
"""
import copy

import pytest

from api_automation.framework.contract import registry, ContractRegistry, SchemaRegistration


@pytest.fixture
def fresh_registry():
    """用独立的注册中心做测试，不污染全局 registry"""
    r = ContractRegistry()
    r.disable()  # 注册时不要打印一堆日志
    yield r
    r.clear()


_OBJ = {
    "type": "object",
    "required": ["code", "msg"],
    "properties": {"code": {"type": "integer"}, "msg": {"type": "string"}},
}


class TestRegistration:
    """注册与匹配"""

    def test_matches_static_path(self, fresh_registry):
        fresh_registry.register("GET", "/system/user/list", response_schema=_OBJ)
        assert fresh_registry.find("GET", "http://x:8081/system/user/list") is not None

    def test_matches_placeholder_path(self, fresh_registry):
        """{id} 必须能匹配真实的数字 id"""
        fresh_registry.register("DELETE", "/system/user/{ids}", response_schema=_OBJ)
        assert fresh_registry.find("DELETE", "http://x:8081/system/user/1,2,3") is not None

    def test_method_must_match(self, fresh_registry):
        fresh_registry.register("POST", "/system/user", response_schema=_OBJ)
        assert fresh_registry.find("PUT", "http://x:8081/system/user") is None

    def test_query_string_is_ignored(self, fresh_registry):
        """带分页参数的列表请求也要能匹配上"""
        fresh_registry.register("GET", "/system/user/list", response_schema=_OBJ)
        assert fresh_registry.find("GET", "http://x:8081/system/user/list?pageNum=1&pageSize=10") is not None

    def test_static_path_wins_over_placeholder(self, fresh_registry):
        """
        回归点：/system/user/list 会被 /system/user/{id} 命中，
        静态注册必须优先，否则列表响应会被详情的 Schema 误判。
        """
        fresh_registry.register("GET", "/system/user/{id}", response_schema={"type": "object", "required": ["detail"]})
        fresh_registry.register("GET", "/system/user/list", response_schema=_OBJ)

        found = fresh_registry.find("GET", "http://x:8081/system/user/list")
        assert found.pattern == "/system/user/list"


class TestValidation:
    """响应校验"""

    def test_valid_body_passes(self, fresh_registry):
        fresh_registry.register("GET", "/a", response_schema=_OBJ)
        fresh_registry.enable()
        assert fresh_registry.validate_response("GET", "http://x/a", 200, {"code": 200, "msg": "操作成功"}) is None

    def test_missing_required_field_is_violation(self, fresh_registry):
        fresh_registry.register("GET", "/a", response_schema=_OBJ)
        fresh_registry.enable()
        violation = fresh_registry.validate_response("GET", "http://x/a", 200, {"code": 200})
        assert violation is not None
        # 顶层缺字段时 relative_path 为空，违规点体现在 error 描述里
        assert "msg" in violation["error"], violation

    def test_wrong_type_is_violation(self, fresh_registry):
        fresh_registry.register("GET", "/a", response_schema=_OBJ)
        fresh_registry.enable()
        assert fresh_registry.validate_response("GET", "http://x/a", 200, {"code": "200", "msg": "x"}) is not None

    def test_unregistered_endpoint_is_skipped(self, fresh_registry):
        fresh_registry.enable()
        assert fresh_registry.validate_response("GET", "http://x/nothing", 200, {"anything": 1}) is None

    def test_disabled_registry_skips_validation(self, fresh_registry):
        fresh_registry.register("GET", "/a", response_schema=_OBJ)
        fresh_registry.disable()
        assert fresh_registry.validate_response("GET", "http://x/a", 200, {"code": 200}) is None


class TestGlobalRegistry:
    """全局注册中心（由 models.register_ruoyi_contracts 填充）"""

    def test_ruoyi_contracts_are_registered(self):
        """conftest 在 pytest_configure 阶段已经注册过了，这里做覆盖度断言"""
        assert registry.count() >= 75, f"RuoYi 契约注册过少: {registry.count()} 条"

    def test_all_http_methods_covered(self):
        methods = {r.method for r in registry.find_all()}
        for m in ("GET", "POST", "PUT", "DELETE"):
            assert m in methods, f"缺少 {m} 方法的契约注册"