"""
【场景测试】— 幂等性与重复提交

这类用例的价值在于暴露"重复点击/网络重试"引发的脏数据问题，
是接口测试里最容易被漏掉、又最容易在生产上出问题的一类。
"""
import allure
import pytest

from api_automation.apis import user_api
from api_automation.common import AssertionEngine
from api_automation.data import factory


@allure.epic("若依接口自动化")
@allure.feature("幂等性与重复提交")
class TestIdempotency:
    """重复提交与重复删除"""

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("重复删除")
    @allure.title("同一用户删除两次：第二次应返回业务错误，而不是静默成功")
    def test_delete_twice(self, logged_in_admin, context):
        payload = context.tag(factory.sys_user(), ["userName"])
        AssertionEngine(user_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = user_api.list({"pageNum": 1, "pageSize": 10, "userName": payload["userName"]}).json()
        assert found.get("rows"), "创建后查不到用户"
        user_id = found["rows"][0]["userId"]

        first = user_api.remove(user_id)
        AssertionEngine(first).status_code(200).jsonpath_eq("$.code", 200)

        second = user_api.remove(user_id)
        AssertionEngine(second).status_code(200)
        assert second.json().get("code") == 500, (
            f"重复删除竟然返回成功，调用方无法判断是否真的删除了：{second.text}"
        )

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("重复提交")
    @allure.title("完全相同的两次新增请求：只应有一条数据落库")
    @allure.severity(allure.severity_level.NORMAL)
    def test_duplicate_create_creates_single_record(self, logged_in_admin, context):
        payload = context.tag(factory.sys_user(), ["userName"])

        first = user_api.create(payload)
        AssertionEngine(first).status_code(200).jsonpath_eq("$.code", 200)

        second = user_api.create(payload)
        AssertionEngine(second).status_code(200)

        listed = user_api.list({"pageNum": 1, "pageSize": 10, "userName": payload["userName"]}).json()
        rows = [r for r in (listed.get("rows") or []) if r.get("userName") == payload["userName"]]

        assert len(rows) == 1, f"重复提交产生了 {len(rows)} 条同名用户，存在脏数据风险"
        assert second.json().get("code") == 500, (
            "重复提交返回了成功，前端无法提示用户'账号已存在'"
        )
        context.lifecycle.created("user", rows[0]["userId"],
                                  endpoint=f"/system/user/{rows[0]['userId']}", method="DELETE")

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("状态变更幂等")
    @allure.title("连续两次把用户置为停用：两次都应成功（状态变更本身是幂等的）")
    def test_change_status_is_idempotent(self, logged_in_admin, a_new_user):
        for _ in range(2):
            resp = user_api.change_status({"userId": a_new_user["id"], "status": "1"})
            AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

        assert user_api.detail(a_new_user["id"]).json()["data"]["status"] == "1"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("读操作稳定性")
    @allure.title("同一查询连续执行两次，结果保持一致")
    def test_repeated_read_is_stable(self, logged_in_admin, a_new_user):
        params = {"pageNum": 1, "pageSize": 10, "userName": a_new_user["userName"]}
        first = user_api.list(params).json()
        second = user_api.list(params).json()

        assert first.get("total") == second.get("total"), (
            f"两次查询 total 不一致：{first.get('total')} vs {second.get('total')}"
        )
        assert [r.get("userId") for r in first.get("rows", [])] == \
               [r.get("userId") for r in second.get("rows", [])], "两次查询返回的记录不一致"