"""
【框架自测】— 数据隔离子系统

验证三件事：
  1. 每次运行的 identity 唯一（并发/重复执行不会撞数据）
  2. tag() 只给指定字段加前缀，不误伤其他字段
  3. 清理时按登记的 HTTP 方法发请求（原实现在这里写死了 POST，
     导致 DELETE 类清理接口全部清理失败）
"""
import pytest

# 用模块方式导入：TestIdentity / TestContext 以 Test 开头，
# 直接 import 类名会被 pytest 当成测试类收集并抛 PytestCollectionWarning
from api_automation.framework import isolation


class FakeClient:
    """假客户端：只记录被调用了哪个方法、访问了哪个 URL"""

    def __init__(self):
        self.calls = []

    def __getattr__(self, name):
        if name not in ("get", "post", "put", "delete"):
            raise AttributeError(name)

        def _call(url, **kwargs):
            self.calls.append((name.upper(), url))
            return None
        return _call


class TestIdentity:
    """测试身份标识"""

    def test_identity_is_unique(self):
        """两次运行的 tag 必须不同，否则并发时数据会互相覆盖"""
        a = isolation.TestIdentity.new("test_a")
        b = isolation.TestIdentity.new("test_a")
        assert a.tag != b.tag
        assert a.run_id != b.run_id

    def test_tag_only_touches_given_fields(self):
        """只给显式指定的字段打标"""
        identity = isolation.TestIdentity.new("t")
        data = {"userName": "ry_001", "nickName": "昵称", "remark": "备注"}
        tagged = identity.apply_to(data, ["userName"])

        assert tagged["userName"].startswith(identity.tag + "_")
        assert tagged["nickName"] == "昵称"
        assert tagged["remark"] == "备注"

    def test_original_data_not_mutated(self):
        """打标不能污染调用方传入的原始字典"""
        identity = isolation.TestIdentity.new("t")
        data = {"userName": "ry_001"}
        identity.apply_to(data, ["userName"])
        assert data["userName"] == "ry_001"


class TestLifecycle:
    """数据生命周期与清理"""

    def test_created_registers_task(self):
        client = FakeClient()
        ctx = isolation.TestContext("test_x", client)
        ctx.lifecycle.created("user", 12, endpoint="/system/user/12", method="DELETE")
        assert ctx.lifecycle.task_count == 1

    def test_cleanup_uses_registered_method(self):
        """登记 DELETE 就必须发 DELETE（回归：原实现恒定调 post）"""
        client = FakeClient()
        ctx = isolation.TestContext("test_x", client)
        ctx.lifecycle.created("user", 12, endpoint="/system/user/12", method="DELETE")

        ctx.cleanup()

        assert ("DELETE", "/system/user/12") in client.calls

    def test_cleanup_supports_mixed_methods(self):
        """同一个用例里可以混合不同清理方法"""
        client = FakeClient()
        ctx = isolation.TestContext("test_x", client)
        ctx.lifecycle.created("config", 5, endpoint="/system/config/5", method="DELETE")
        ctx.lifecycle.created("job", 6, endpoint="/monitor/job/6", method="DELETE")

        ctx.cleanup()

        assert ("DELETE", "/system/config/5") in client.calls
        assert ("DELETE", "/monitor/job/6") in client.calls
        assert ctx.lifecycle.task_count == 0

    def test_cleanup_failure_does_not_break_other_tasks(self):
        """单条清理失败不能中断其余清理 —— 否则会留下一堆脏数据"""
        class HalfBrokenClient(FakeClient):
            def delete(self, url, **kwargs):
                self.calls.append(("DELETE", url))
                if url.endswith("/1"):
                    raise RuntimeError("删不掉")

        client = HalfBrokenClient()
        ctx = isolation.TestContext("test_x", client)
        ctx.lifecycle.created("a", 1, endpoint="/x/1", method="DELETE")
        ctx.lifecycle.created("b", 2, endpoint="/x/2", method="DELETE")

        ctx.cleanup()  # 不应抛出

        assert ("DELETE", "/x/2") in client.calls

    def test_cleanup_without_tasks_is_noop(self):
        client = FakeClient()
        ctx = isolation.TestContext("test_x", client)
        ctx.cleanup()
        assert client.calls == []