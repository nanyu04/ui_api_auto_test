"""
【场景测试】— 通知公告（接口文档 4.2.74 ~ 4.2.82）

表单中"公告标题"带 @Xss 校验，这里顺带覆盖脚本注入拦截。
"""
import allure
import pytest

from api_automation.apis import notice_api
from api_automation.common import AssertionEngine
from api_automation.data import factory
from api_automation.utils import get_project_root, read_yaml

CASES = read_yaml(get_project_root() / "data/test_data/notice_cases.yaml")


@allure.epic("若依接口自动化")
@allure.feature("通知公告")
class TestNotice:
    """公告 CRUD 与已读标记"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("新增公告")
    @allure.title("新增公告成功并可在列表中查询到")
    def test_create_notice(self, logged_in_admin, context):
        payload = context.tag(factory.sys_notice(), ["noticeTitle"])
        AssertionEngine(notice_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_notice(payload["noticeTitle"])
        assert found, f"新增成功但列表查不到 {payload['noticeTitle']}"
        context.lifecycle.created("notice", found["noticeId"],
                                  endpoint=f"/system/notice/{found['noticeId']}", method="DELETE")

    @pytest.mark.regression
    @pytest.mark.P1
    @pytest.mark.parametrize("case", CASES, ids=[c["title"] for c in CASES])
    @allure.story("公告参数校验")
    @allure.title("公告参数校验与 XSS 拦截（数据驱动）")
    def test_notice_validation(self, logged_in_admin, context, case):
        payload = context.tag(factory.sys_notice(), ["noticeTitle"])
        payload.update(case["overrides"])

        resp = notice_api.create(payload)
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
    @allure.story("公告生命周期")
    @allure.title("公告生命周期：创建→改标题→删除→确认已删除")
    def test_notice_lifecycle(self, logged_in_admin, context):
        payload = context.tag(factory.sys_notice(), ["noticeTitle"])
        AssertionEngine(notice_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_notice(payload["noticeTitle"])
        assert found, "创建后列表查不到公告"
        notice_id = found["noticeId"]

        updated = dict(found)
        updated["noticeTitle"] = f"改名_{payload['noticeTitle']}"
        AssertionEngine(notice_api.update(updated)).status_code(200).jsonpath_eq("$.code", 200)
        assert notice_api.detail(notice_id).json()["data"]["noticeTitle"] == updated["noticeTitle"]

        AssertionEngine(notice_api.remove(notice_id)).status_code(200).jsonpath_eq("$.code", 200)
        assert notice_api.detail(notice_id).json().get("code") == 500, "删除后仍能查到该公告"

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("顶部通知")
    @allure.title("最新公告接口返回列表并带未读数，条数不超过 5")
    def test_list_top(self, logged_in_admin):
        resp = notice_api.list_top()
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200).has_field("unreadCount")

        rows = ae.extract("data") or []
        assert len(rows) <= 5, f"顶部公告最多返回 5 条，实际 {len(rows)}"

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("公告已读")
    @allure.title("标记单条公告已读后，未读数应减少或保持不变（不新增）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_mark_read(self, logged_in_admin, a_new_notice):
        before = notice_api.list_top().json().get("unreadCount", 0)
        AssertionEngine(notice_api.mark_read(a_new_notice["id"])) \
            .status_code(200).jsonpath_eq("$.code", 200)
        after = notice_api.list_top().json().get("unreadCount", 0)

        assert after <= before, f"标记已读后未读数反而增加了：{before} → {after}"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("公告已读")
    @allure.title("批量标记已读返回成功（接口容错：重复标记不报错）")
    def test_mark_read_all(self, logged_in_admin, a_new_notice):
        resp = notice_api.mark_read_all(f"{a_new_notice['id']}")
        AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

        # 幂等：再标一次不应报错
        again = notice_api.mark_read_all(f"{a_new_notice['id']}")
        AssertionEngine(again).status_code(200).jsonpath_eq("$.code", 200)

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("公告已读用户")
    @allure.title("查询公告已读用户列表分页结构正确")
    def test_read_users(self, logged_in_admin, a_new_notice):
        resp = notice_api.read_users({"noticeId": a_new_notice["id"], "pageNum": 1, "pageSize": 10})
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200).has_field("rows").has_field("total")


def _find_notice(notice_title: str):
    resp = notice_api.list({"pageNum": 1, "pageSize": 10, "noticeTitle": notice_title})
    try:
        rows = resp.json().get("rows") or []
    except Exception:
        return None
    for row in rows:
        if row.get("noticeTitle") == notice_title:
            return row
    return None