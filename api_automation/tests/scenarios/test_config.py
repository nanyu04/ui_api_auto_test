"""
【场景测试】— 参数配置（接口文档 4.2.66 ~ 4.2.73）
"""
import allure
import pytest

from api_automation.apis import config_api
from api_automation.common import AssertionEngine
from api_automation.data import factory
from api_automation.utils import get_project_root, read_yaml

CASES = read_yaml(get_project_root() / "data/test_data/config_cases.yaml")


@allure.epic("若依接口自动化")
@allure.feature("参数配置")
class TestConfig:
    """参数 CRUD 与缓存"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("新增参数")
    @allure.title("新增参数成功并可按键名查询到参数值")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_config(self, logged_in_admin, context):
        payload = context.tag(factory.sys_config(), ["configKey"])
        AssertionEngine(config_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        by_key = config_api.by_key(payload["configKey"])
        ae = AssertionEngine(by_key)
        ae.status_code(200).jsonpath_eq("$.code", 200)
        # 若依该接口的 success(String) 重载会把参数值放进 msg，而不是 data
        assert ae.extract("msg") == payload["configValue"], (
            f"按键名查询应返回参数值 {payload['configValue']}：{by_key.text}"
        )

        found = _find_config(payload["configKey"])
        assert found, "新增成功但列表查不到"
        context.lifecycle.created("config", found["configId"],
                                  endpoint=f"/system/config/{found['configId']}", method="DELETE")

    @pytest.mark.regression
    @pytest.mark.P1
    @pytest.mark.parametrize("case", CASES, ids=[c["title"] for c in CASES])
    @allure.story("参数校验")
    @allure.title("参数校验与边界值（数据驱动）")
    def test_config_validation(self, logged_in_admin, context, case):
        payload = context.tag(factory.sys_config(), ["configKey"])
        payload.update(case["overrides"])

        resp = config_api.create(payload)
        body = resp.json()
        AssertionEngine(resp).status_code(200)
        assert body.get("code") == case["expect_code"], (
            f"[{case['title']}] 期望 code={case['expect_code']}，实际 {body.get('code')}：{resp.text}"
        )
        if case.get("expect_msg"):
            assert case["expect_msg"] in body.get("msg", ""), (
                f"[{case['title']}] 提示不含 '{case['expect_msg']}'：{body.get('msg')}"
            )

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("参数生命周期")
    @allure.title("参数生命周期：创建→改值→按键查询确认→删除→确认已删除")
    def test_config_lifecycle(self, logged_in_admin, context):
        payload = context.tag(factory.sys_config(), ["configKey"])
        AssertionEngine(config_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_config(payload["configKey"])
        assert found, "创建后列表查不到"
        config_id = found["configId"]

        updated = dict(found)
        updated["configValue"] = "999"
        AssertionEngine(config_api.update(updated)).status_code(200).jsonpath_eq("$.code", 200)
        assert config_api.by_key(payload["configKey"]).json()["msg"] == "999"

        AssertionEngine(config_api.remove(config_id)).status_code(200).jsonpath_eq("$.code", 200)
        assert config_api.detail(config_id).json().get("code") == 500, "删除后仍能查到该参数"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("参数缓存")
    @allure.title("刷新参数缓存返回成功")
    def test_refresh_cache(self, logged_in_admin):
        AssertionEngine(config_api.refresh_cache()).status_code(200).jsonpath_eq("$.code", 200)

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("参数查询")
    @allure.title("查询参数列表按键名过滤")
    def test_list_filter(self, logged_in_admin, a_new_config):
        resp = config_api.list({"pageNum": 1, "pageSize": 10, "configKey": a_new_config["configKey"]})
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200)

        rows = ae.extract("rows") or []
        assert rows, "按键名过滤无结果"
        assert all(a_new_config["configKey"] in (r.get("configKey") or "") for r in rows), (
            f"过滤条件未生效：{[r.get('configKey') for r in rows]}"
        )


def _find_config(config_key: str):
    resp = config_api.list({"pageNum": 1, "pageSize": 10, "configKey": config_key})
    try:
        rows = resp.json().get("rows") or []
    except Exception:
        return None
    for row in rows:
        if row.get("configKey") == config_key:
            return row
    return None
