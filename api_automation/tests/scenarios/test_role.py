"""
【场景测试】— 角色管理（接口文档 4.2.14 ~ 4.2.28）
"""
import allure
import pytest

from api_automation.apis import role_api
from api_automation.common import AssertionEngine
from api_automation.data import factory
from api_automation.utils import get_project_root, read_yaml

CASES = read_yaml(get_project_root() / "data/test_data/role_cases.yaml")


@allure.epic("若依接口自动化")
@allure.feature("角色管理")
class TestRole:
    """角色 CRUD 与授权"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("新增角色")
    @allure.title("新增角色成功并可在列表中查询到")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_role(self, logged_in_admin, context):
        payload = context.tag(factory.sys_role(), ["roleName"])
        AssertionEngine(role_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_role(payload["roleName"])
        assert found, f"新增成功但列表查不到 {payload['roleName']}"
        assert found["roleKey"] == payload["roleKey"]
        context.lifecycle.created("role", found["roleId"],
                                  endpoint=f"/system/role/{found['roleId']}", method="DELETE")

    @pytest.mark.regression
    @pytest.mark.P1
    @pytest.mark.parametrize("case", CASES, ids=[c["title"] for c in CASES])
    @allure.story("角色参数校验")
    @allure.title("角色参数校验与边界值（数据驱动）")
    def test_role_validation(self, logged_in_admin, context, case):
        payload = context.tag(factory.sys_role(), ["roleName"])
        payload.update(case["overrides"])

        resp = role_api.create(payload)
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
    @allure.story("角色生命周期")
    @allure.title("角色生命周期：创建→修改→查询确认→删除→确认已删除")
    def test_role_lifecycle(self, logged_in_admin, context):
        payload = context.tag(factory.sys_role(), ["roleName"])
        AssertionEngine(role_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_role(payload["roleName"])
        assert found, "创建后角色列表查不到"
        role_id = found["roleId"]

        new_name = f"改名_{payload['roleName']}"
        updated = factory.sys_role(role_name=new_name, role_key=payload["roleKey"])
        updated.update({"roleId": role_id, "menuIds": []})
        AssertionEngine(role_api.update(updated)).status_code(200).jsonpath_eq("$.code", 200)

        assert role_api.detail(role_id).json()["data"]["roleName"] == new_name

        AssertionEngine(role_api.remove(role_id)).status_code(200).jsonpath_eq("$.code", 200)
        assert role_api.detail(role_id).json().get("code") == 500, "删除后仍能查到该角色"

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("角色状态")
    @allure.title("修改角色状态：停用后状态位变为 1，可再启用")
    def test_change_status(self, logged_in_admin, a_new_role):
        AssertionEngine(role_api.change_status({"roleId": a_new_role["id"], "status": "1"})) \
            .status_code(200).jsonpath_eq("$.code", 200)
        assert role_api.detail(a_new_role["id"]).json()["data"]["status"] == "1"

        AssertionEngine(role_api.change_status({"roleId": a_new_role["id"], "status": "0"})) \
            .status_code(200).jsonpath_eq("$.code", 200)
        assert role_api.detail(a_new_role["id"]).json()["data"]["status"] == "0"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("角色数据权限")
    @allure.title("修改角色数据权限为自定义并校验数据范围回写")
    def test_data_scope(self, logged_in_admin, a_new_role):
        payload = {
            "roleId": a_new_role["id"],
            "dataScope": "2",
            "deptIds": [100, 101],
        }
        AssertionEngine(role_api.data_scope(payload)).status_code(200).jsonpath_eq("$.code", 200)

        detail = role_api.detail(a_new_role["id"]).json()["data"]
        assert detail.get("dataScope") == "2", f"数据权限未更新：{detail.get('dataScope')}"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("角色下拉项")
    @allure.title("获取角色下拉选项返回 code=200 与数据")
    def test_option_select(self, logged_in_admin):
        ae = AssertionEngine(role_api.option_select())
        ae.status_code(200).jsonpath_eq("$.code", 200)
        assert ae.extract("data") is not None, "角色下拉选项不应为 null"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("角色授权用户")
    @allure.title("已分配/未分配用户列表可正常分页查询")
    def test_allocated_unallocated_lists(self, logged_in_admin, a_new_role):
        allocated = AssertionEngine(role_api.allocated_list({"roleId": a_new_role["id"], "pageNum": 1, "pageSize": 10}))
        allocated.status_code(200).jsonpath_eq("$.code", 200)
        allocated.has_field("rows").has_field("total")

        unallocated = AssertionEngine(role_api.unallocated_list({"roleId": a_new_role["id"], "pageNum": 1, "pageSize": 10}))
        unallocated.status_code(200).jsonpath_eq("$.code", 200)


def _find_role(role_name: str):
    resp = role_api.list({"pageNum": 1, "pageSize": 10, "roleName": role_name})
    try:
        rows = resp.json().get("rows") or []
    except Exception:
        return None
    for row in rows:
        if row.get("roleName") == role_name:
            return row
    return None