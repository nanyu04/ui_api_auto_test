"""
【契约测试】— 从注册中心自动生成

不需要为每个接口手写结构断言：
框架遍历 ContractRegistry 里注册的端点，
统一验证 Schema 自身合法性 + required 字段有定义 + 覆盖度达标。
"""
import jsonschema
import pytest

from api_automation.framework.contract import registry


class TestContractSchema:
    """契约注册项自身的合法性"""

    @pytest.mark.smoke
    @pytest.mark.contract
    @pytest.mark.P0
    def test_all_registered_schemas_are_valid(self):
        """每个注册的 Schema 都必须是合法的 JSON Schema"""
        registrations = registry.find_all()
        assert len(registrations) > 0, "没有注册任何 Schema"

        for reg in registrations:
            if reg.response_schema:
                try:
                    jsonschema.Draft7Validator.check_schema(reg.response_schema)
                except Exception as e:
                    pytest.fail(f"Schema 不合法: {reg.description}\n  {e}")

    @pytest.mark.contract
    @pytest.mark.P1
    def test_required_fields_have_definitions(self):
        """required 字段必须在 properties 中定义，否则 Schema 是残缺的"""
        for reg in registry.find_all():
            schema = reg.response_schema
            if not schema:
                continue
            for field in schema.get("required", []):
                assert field in schema.get("properties", {}), (
                    f"{reg.description}: required 字段 '{field}' 在 properties 中未定义"
                )

    @pytest.mark.contract
    @pytest.mark.P1
    def test_no_duplicate_registrations(self):
        """同一个 method + pattern 不应重复注册（重复会掩盖覆盖缺口）"""
        seen = {}
        for reg in registry.find_all():
            key = (reg.method, reg.pattern)
            seen.setdefault(key, []).append(reg.description)
        duplicates = {k: v for k, v in seen.items() if len(v) > 1}
        assert not duplicates, f"存在重复注册: {duplicates}"

    @pytest.mark.contract
    @pytest.mark.P2
    def test_coverage_summary(self):
        """打印契约覆盖情况，便于人工核对接口文档覆盖率"""
        regs = registry.find_all()
        by_method = {}
        for r in regs:
            by_method.setdefault(r.method, 0)
            by_method[r.method] += 1

        print(f"\n  已注册 {len(regs)} 个端点:")
        for r in sorted(regs, key=lambda x: (x.pattern, x.method)):
            print(f"    {r.method:6s} {r.pattern:45s} {r.description}")
        print(f"  方法分布: {by_method}")

        assert len(regs) >= 75, (
            f"注册端点过少 ({len(regs)})，接口文档共 147 个接口，覆盖率明显不足"
        )