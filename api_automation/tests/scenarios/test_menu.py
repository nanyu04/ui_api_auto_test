"""
【场景测试】— 菜单管理（接口文档 4.2.29 ~ 4.2.36）
"""
import allure
import pytest

from api_automation.apis import menu_api
from api_automation.common import AssertionEngine
from api_automation.data import factory
from api_automation.utils import get_project_root, read_yaml

CASES = read_yaml(get_project_root() / "data/test_data/menu_cases.yaml")


@allure.epic("若依接口自动化")
@allure.feature("菜单管理")
class TestMenu:
    """菜单 CRUD 与树结构"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("新增菜单")
    @allure.title("新增菜单成功并可在树中查询到")
    def test_create_menu(self, logged_in_admin, context):
        payload = context.tag(factory.sys_menu(), ["menuName"])
        AssertionEngine(menu_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_menu(payload["menuName"])
        assert found, f"新增成功但菜单树里查不到 {payload['menuName']}"
        context.lifecycle.created("menu", found["menuId"],
                                  endpoint=f"/system/menu/{found['menuId']}", method="DELETE")

    @pytest.mark.regression
    @pytest.mark.P1
    @pytest.mark.parametrize("case", CASES, ids=[c["title"] for c in CASES])
    @allure.story("菜单参数校验")
    @allure.title("菜单参数校验与边界值（数据驱动）")
    def test_menu_validation(self, logged_in_admin, context, case):
        payload = context.tag(factory.sys_menu(), ["menuName"])
        payload.update(case["overrides"])

        resp = menu_api.create(payload)
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
    @allure.story("菜单树")
    @allure.title("菜单列表返回树形结构（含 children 层级）")
    def test_menu_list_is_tree(self, logged_in_admin):
        ae = AssertionEngine(menu_api.list())
        ae.status_code(200).jsonpath_eq("$.code", 200)

        tree = ae.extract("data")
        assert isinstance(tree, list) and tree, "菜单列表应为非空数组"
        assert any("children" in node for node in tree), (
            "菜单列表应带 children 层级；若缺少说明返回的不是树结构"
        )

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("菜单生命周期")
    @allure.title("菜单生命周期：创建→改名→删除→确认已删除")
    def test_menu_lifecycle(self, logged_in_admin, context):
        payload = context.tag(factory.sys_menu(), ["menuName"])
        AssertionEngine(menu_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_menu(payload["menuName"])
        assert found, "创建后菜单树查不到"
        menu_id = found["menuId"]

        updated = dict(found)
        updated["menuName"] = f"改名_{payload['menuName']}"
        AssertionEngine(menu_api.update(updated)).status_code(200).jsonpath_eq("$.code", 200)
        assert menu_api.detail(menu_id).json()["data"]["menuName"] == updated["menuName"]

        AssertionEngine(menu_api.remove(menu_id)).status_code(200).jsonpath_eq("$.code", 200)
        assert menu_api.detail(menu_id).json().get("code") == 500, "删除后仍能查到该菜单"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("菜单下拉树")
    @allure.title("菜单下拉树与角色菜单树均可正常返回")
    def test_treeselect(self, logged_in_admin, a_new_role):
        treeselect = AssertionEngine(menu_api.treeselect())
        treeselect.status_code(200).jsonpath_eq("$.code", 200)
        assert treeselect.extract("data"), "菜单下拉树不应为空"

        role_tree = AssertionEngine(menu_api.role_menu_treeselect(a_new_role["id"]))
        role_tree.status_code(200).jsonpath_eq("$.code", 200).has_field("checkedKeys")

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("菜单排序")
    @allure.title("保存菜单排序成功回写 orderNum")
    def test_update_sort(self, logged_in_admin, a_new_menu):
        resp = menu_api.update_sort({"menuIds": f"{a_new_menu['id']}", "orderNums": "9"})
        AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

        detail = menu_api.detail(a_new_menu["id"]).json()["data"]
        assert detail.get("orderNum") == 9, f"排序未更新：{detail.get('orderNum')}"


def _find_menu(menu_name: str):
    resp = menu_api.list({"menuName": menu_name})
    try:
        nodes = resp.json().get("data") or []
    except Exception:
        return None
    for node in nodes:
        if node.get("menuName") == menu_name:
            return node
    return None
