"""
【场景测试】— 岗位管理（接口文档 4.2.44 ~ 4.2.50）
"""
import allure
import pytest

from api_automation.apis import post_api
from api_automation.common import AssertionEngine
from api_automation.data import factory
from api_automation.utils import get_project_root, read_yaml

CASES = read_yaml(get_project_root() / "data/test_data/post_cases.yaml")


@allure.epic("若依接口自动化")
@allure.feature("岗位管理")
class TestPost:
    """岗位 CRUD"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("新增岗位")
    @allure.title("新增岗位成功并可在列表中查询到")
    def test_create_post(self, logged_in_admin, context):
        payload = context.tag(factory.sys_post(), ["postCode"])
        AssertionEngine(post_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_post(payload["postCode"])
        assert found, f"新增成功但列表查不到 {payload['postCode']}"
        assert found["postName"] == payload["postName"]
        context.lifecycle.created("post", found["postId"],
                                  endpoint=f"/system/post/{found['postId']}", method="DELETE")

    @pytest.mark.regression
    @pytest.mark.P1
    @pytest.mark.parametrize("case", CASES, ids=[c["title"] for c in CASES])
    @allure.story("岗位参数校验")
    @allure.title("岗位参数校验与边界值（数据驱动）")
    def test_post_validation(self, logged_in_admin, context, case):
        payload = context.tag(factory.sys_post(), ["postCode"])
        payload.update(case["overrides"])

        resp = post_api.create(payload)
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
    @allure.story("岗位生命周期")
    @allure.title("岗位生命周期：创建→改名→删除→确认已删除")
    def test_post_lifecycle(self, logged_in_admin, context):
        payload = context.tag(factory.sys_post(), ["postCode"])
        AssertionEngine(post_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_post(payload["postCode"])
        assert found, "创建后列表查不到"
        post_id = found["postId"]

        updated = dict(found)
        updated["postName"] = f"改名_{payload['postName']}"
        AssertionEngine(post_api.update(updated)).status_code(200).jsonpath_eq("$.code", 200)
        assert post_api.detail(post_id).json()["data"]["postName"] == updated["postName"]

        AssertionEngine(post_api.remove(post_id)).status_code(200).jsonpath_eq("$.code", 200)
        assert post_api.detail(post_id).json().get("code") == 500, "删除后仍能查到该岗位"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("岗位下拉项")
    @allure.title("获取岗位下拉选项返回数据")
    def test_option_select(self, logged_in_admin):
        ae = AssertionEngine(post_api.option_select())
        ae.status_code(200).jsonpath_eq("$.code", 200)
        assert ae.extract("data") is not None, "岗位下拉选项不应为 null"


def _find_post(post_code: str):
    resp = post_api.list({"pageNum": 1, "pageSize": 10, "postCode": post_code})
    try:
        rows = resp.json().get("rows") or []
    except Exception:
        return None
    for row in rows:
        if row.get("postCode") == post_code:
            return row
    return None