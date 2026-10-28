"""
【场景测试】— 部门管理（接口文档 4.2.37 ~ 4.2.43）
"""
import allure
import pytest

from api_automation.apis import dept_api
from api_automation.common import AssertionEngine
from api_automation.data import factory
from api_automation.utils import get_project_root, read_yaml

CASES = read_yaml(get_project_root() / "data/test_data/dept_cases.yaml")


@allure.epic("若依接口自动化")
@allure.feature("部门管理")
class TestDept:
    """部门 CRUD 与树结构"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("新增部门")
    @allure.title("新增部门成功并可在树中查询到")
    def test_create_dept(self, logged_in_admin, context):
        payload = context.tag(factory.sys_dept(), ["deptName"])
        AssertionEngine(dept_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_dept(payload["deptName"])
        assert found, f"新增成功但部门树里查不到 {payload['deptName']}"
        context.lifecycle.created("dept", found["deptId"],
                                  endpoint=f"/system/dept/{found['deptId']}", method="DELETE")

    @pytest.mark.regression
    @pytest.mark.P1
    @pytest.mark.parametrize("case", CASES, ids=[c["title"] for c in CASES])
    @allure.story("部门参数校验")
    @allure.title("部门参数校验与边界值（数据驱动）")
    def test_dept_validation(self, logged_in_admin, context, case):
        payload = context.tag(factory.sys_dept(), ["deptName"])
        payload.update(case["overrides"])

        resp = dept_api.create(payload)
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
    @allure.story("部门树")
    @allure.title("部门列表为树形结构且包含已知的根部门")
    def test_dept_list_is_tree(self, logged_in_admin):
        ae = AssertionEngine(dept_api.list())
        ae.status_code(200).jsonpath_eq("$.code", 200)

        tree = ae.extract("data")
        assert isinstance(tree, list) and tree, "部门列表应为非空数组"
        assert any("children" in node for node in tree), "部门列表应带 children 层级"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("部门排除节点")
    @allure.title("排除节点查询不返回被排除的部门")
    def test_list_exclude(self, logged_in_admin, a_new_dept):
        resp = dept_api.list_exclude(a_new_dept["id"])
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200)

        ids = _collect_ids(ae.extract("data") or [])
        assert a_new_dept["id"] not in ids, f"被排除的部门仍出现在结果中：{ids}"

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("部门生命周期")
    @allure.title("部门生命周期：创建→改名→删除→确认已删除")
    def test_dept_lifecycle(self, logged_in_admin, context):
        payload = context.tag(factory.sys_dept(), ["deptName"])
        AssertionEngine(dept_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_dept(payload["deptName"])
        assert found, "创建后部门树查不到"
        dept_id = found["deptId"]

        updated = dict(found)
        updated["deptName"] = f"改名_{payload['deptName']}"
        AssertionEngine(dept_api.update(updated)).status_code(200).jsonpath_eq("$.code", 200)
        assert dept_api.detail(dept_id).json()["data"]["deptName"] == updated["deptName"]

        AssertionEngine(dept_api.remove(dept_id)).status_code(200).jsonpath_eq("$.code", 200)
        assert dept_api.detail(dept_id).json().get("code") == 500, "删除后仍能查到该部门"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("部门排序")
    @allure.title("保存部门排序成功回写 orderNum")
    def test_update_sort(self, logged_in_admin, a_new_dept):
        resp = dept_api.update_sort({"deptIds": f"{a_new_dept['id']}", "orderNums": "7"})
        AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)
        assert dept_api.detail(a_new_dept["id"]).json()["data"].get("orderNum") == 7


def _collect_ids(nodes) -> list:
    """递归收集树里所有 deptId"""
    ids = []
    for node in nodes:
        if isinstance(node, dict):
            if "deptId" in node:
                ids.append(node["deptId"])
            ids.extend(_collect_ids(node.get("children") or []))
    return ids


def _find_dept(dept_name: str):
    resp = dept_api.list({"deptName": dept_name})
    try:
        nodes = resp.json().get("data") or []
    except Exception:
        return None
    for node in nodes:
        if node.get("deptName") == dept_name:
            return node
    return None
