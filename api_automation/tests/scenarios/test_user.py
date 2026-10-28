"""
【场景测试】— 用户管理（接口文档 4.2.1 ~ 4.2.13）

覆盖：新增参数校验与边界值、列表查询、生命周期闭环、
状态变更、重置密码、角色分配、部门树。
"""
import allure
import pytest

from api_automation.apis import user_api
from api_automation.common import AssertionEngine, logger
from api_automation.data import factory
from api_automation.utils import get_project_root, read_yaml

CREATE_CASES = read_yaml(get_project_root() / "data/test_data/user_create_cases.yaml")
QUERY_CASES = read_yaml(get_project_root() / "data/test_data/user_query_cases.yaml")


@allure.epic("若依接口自动化")
@allure.feature("用户管理")
class TestUserCreate:
    """新增用户"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("新增用户")
    @allure.title("新增用户成功并可在列表中查询到")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_success(self, logged_in_admin, context):
        payload = context.tag(factory.sys_user(), ["userName"])
        resp = user_api.create(payload)

        AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200).jsonpath_eq("$.msg", "操作成功")

        found = _find_user(payload["userName"])
        assert found is not None, f"新增成功但列表查不到 {payload['userName']}：{resp.text}"
        assert found["nickName"] == payload["nickName"]

        # 登记清理，用例结束自动删除，避免污染环境
        context.lifecycle.created("user", found["userId"],
                                  endpoint=f"/system/user/{found['userId']}", method="DELETE")

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("新增用户")
    @allure.title("用户名重复时拒绝新增")
    def test_create_duplicate_user_name_rejected(self, logged_in_admin, a_new_user, context):
        payload = context.tag(factory.sys_user(), ["userName"])
        # 故意改成已存在的账号（打标之后覆盖，否则又变成新账号了）
        payload["userName"] = a_new_user["userName"]
        resp = user_api.create(payload)

        AssertionEngine(resp).status_code(200)
        body = resp.json()
        assert body.get("code") == 500, f"重复用户名竟然创建成功：{resp.text}"
        assert "失败" in body.get("msg", "") or "已存在" in body.get("msg", ""), body.get("msg")

    @pytest.mark.regression
    @pytest.mark.P1
    @pytest.mark.parametrize("case", CREATE_CASES, ids=[c["title"] for c in CREATE_CASES])
    @allure.story("新增用户-参数校验")
    @allure.title("新增用户参数校验与边界值（数据驱动）")
    def test_create_user_validation(self, logged_in_admin, context, case):
        # 先生成合法数据并打唯一标记，再用非法值覆盖目标字段：
        # 顺序不能反，否则空字符串会被打标逻辑加前缀，用例就测不到"为空"了
        payload = context.tag(factory.sys_user(), ["userName"])
        payload.update(case["overrides"])

        resp = user_api.create(payload)
        body = resp.json()

        AssertionEngine(resp).status_code(200)
        assert body.get("code") == case["expect_code"], (
            f"[{case['title']}] 期望 code={case['expect_code']}，实际 {body.get('code')}：{resp.text}"
        )
        if case.get("expect_msg"):
            assert case["expect_msg"] in body.get("msg", ""), (
                f"[{case['title']}] 提示不含 '{case['expect_msg']}'：{body.get('msg')}"
            )

        # 正常创建的分支要顺手清理掉
        if case["expect_code"] == 200:
            found = _find_user(payload["userName"])
            if found:
                context.lifecycle.created("user", found["userId"],
                                          endpoint=f"/system/user/{found['userId']}", method="DELETE")


@allure.epic("若依接口自动化")
@allure.feature("用户管理")
class TestUserQuery:
    """用户列表查询"""

    @pytest.mark.regression
    @pytest.mark.P1
    @pytest.mark.parametrize("case", QUERY_CASES, ids=[c["title"] for c in QUERY_CASES])
    @allure.story("用户列表查询")
    @allure.title("用户列表分页与查询条件边界（数据驱动）")
    def test_user_list_query(self, logged_in_admin, case):
        resp = user_api.list(case["params"])
        body = resp.json()

        AssertionEngine(resp).status_code(200)
        assert body.get("code") == case["expect_code"], (
            f"[{case['title']}] 期望 code={case['expect_code']}，实际 {body.get('code')}：{resp.text}"
        )
        if case["expect_code"] == 200:
            assert "rows" in body and "total" in body, f"列表响应缺少分页字段：{body}"

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("用户列表查询")
    @allure.title("按用户名过滤只返回匹配记录")
    def test_user_list_filter_by_name(self, logged_in_admin, a_new_user):
        resp = user_api.list({"pageNum": 1, "pageSize": 10, "userName": a_new_user["userName"]})
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200)

        rows = ae.extract("rows") or []
        assert rows, f"按 {a_new_user['userName']} 查询无结果"
        assert all(a_new_user["userName"] in (r.get("userName") or "") for r in rows), (
            f"过滤条件未生效，返回了无关记录：{[r.get('userName') for r in rows]}"
        )

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("用户详细")
    @allure.title("查询用户详细返回与创建时一致的字段")
    def test_user_detail(self, logged_in_admin, a_new_user):
        resp = user_api.detail(a_new_user["id"])
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200)

        assert ae.extract("data.userId") == a_new_user["id"]
        assert ae.extract("data.userName") == a_new_user["userName"]

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("用户详细")
    @allure.title("查询不存在的用户：返回业务错误而不是 500 崩溃")
    def test_user_detail_not_exists(self, logged_in_admin):
        resp = user_api.detail(factory.random_id())
        AssertionEngine(resp).status_code(200)
        assert resp.json().get("code") == 500, f"不存在的用户应返回业务错误：{resp.text}"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("部门树")
    @allure.title("获取部门树用于新增用户的下拉选择")
    def test_user_dept_tree(self, logged_in_admin):
        ae = AssertionEngine(user_api.dept_tree())
        ae.status_code(200).jsonpath_eq("$.code", 200)
        assert ae.extract("data"), "部门树不应为空"


@allure.epic("若依接口自动化")
@allure.feature("用户管理")
class TestUserLifecycle:
    """用户生命周期：创建 → 查询 → 修改 → 状态变更 → 重置密码 → 删除"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("用户生命周期")
    @allure.title("完整生命周期：创建→修改→查询确认→删除→确认已删除")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_lifecycle(self, logged_in_admin, context):
        payload = context.tag(factory.sys_user(), ["userName"])
        AssertionEngine(user_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_user(payload["userName"])
        assert found, f"创建后查不到用户 {payload['userName']}"
        user_id = found["userId"]

        # 修改昵称
        new_nick = f"改名_{payload['nickName']}"
        updated = factory.sys_user(user_name=payload["userName"], userId=user_id,
                                   nickName=new_nick, deptId=payload["deptId"],
                                   email=payload["email"],
                                   phonenumber=payload["phonenumber"])
        updated["roleIds"] = []
        updated["postIds"] = []
        AssertionEngine(user_api.update(updated)).status_code(200).jsonpath_eq("$.code", 200)

        detail = user_api.detail(user_id).json()
        assert detail.get("data", {}).get("nickName") == new_nick, (
            f"昵称未更新成功：{detail.get('data', {}).get('nickName')}"
        )

        # 删除
        AssertionEngine(user_api.remove(user_id)).status_code(200).jsonpath_eq("$.code", 200)
        gone = user_api.detail(user_id).json()
        assert gone.get("code") == 500, f"删除后仍能查到该用户：{gone}"

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("用户状态")
    @allure.title("修改用户状态：停用后状态位变为 1，可再启用")
    def test_change_status(self, logged_in_admin, a_new_user):
        stop = {"userId": a_new_user["id"], "status": "1"}
        AssertionEngine(user_api.change_status(stop)).status_code(200).jsonpath_eq("$.code", 200)
        assert user_api.detail(a_new_user["id"]).json()["data"]["status"] == "1"

        start = {"userId": a_new_user["id"], "status": "0"}
        AssertionEngine(user_api.change_status(start)).status_code(200).jsonpath_eq("$.code", 200)
        assert user_api.detail(a_new_user["id"]).json()["data"]["status"] == "0"

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("用户密码")
    @allure.title("重置用户密码成功；重置不存在的用户返回业务错误")
    def test_reset_password(self, logged_in_admin, a_new_user):
        resp = user_api.reset_pwd({"userId": a_new_user["id"], "password": "newPwd_123456"})
        AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

        bad = user_api.reset_pwd({"userId": factory.random_id(), "password": "newPwd_123456"})
        assert bad.json().get("code") == 500, f"重置不存在用户的密码应失败：{bad.text}"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("用户密码")
    @allure.title("密码为空时重置被拒绝（@NotBlank）")
    def test_reset_password_blank(self, logged_in_admin, a_new_user):
        resp = user_api.reset_pwd({"userId": a_new_user["id"], "password": ""})
        AssertionEngine(resp).status_code(200)
        body = resp.json()
        assert body.get("code") == 500, f"空密码竟然重置成功：{resp.text}"
        assert "密码" in body.get("msg", ""), body.get("msg")

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("用户角色")
    @allure.title("查询已分配角色 → 分配角色 → 再次查询结果一致")
    def test_assign_role(self, logged_in_admin, a_new_user, a_new_role):
        before = AssertionEngine(user_api.auth_role(a_new_user["id"]))
        before.status_code(200).jsonpath_eq("$.code", 200)

        assign = user_api.insert_auth_role({
            "userId": a_new_user["id"],
            "roleIds": f"{a_new_role['id']}",
        })
        AssertionEngine(assign).status_code(200).jsonpath_eq("$.code", 200)

        after = AssertionEngine(user_api.auth_role(a_new_user["id"]))
        after.status_code(200).jsonpath_eq("$.code", 200)
        role_ids = [r.get("roleId") for r in (after.extract("roles") or [])]
        assert a_new_role["id"] in role_ids, f"分配后角色列表未包含新角色：{role_ids}"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("用户删除")
    @allure.title("删除不存在的用户返回业务错误，不产生 500 崩溃")
    def test_delete_not_exists(self, logged_in_admin):
        resp = user_api.remove(factory.random_id())
        AssertionEngine(resp).status_code(200)
        assert resp.json().get("code") == 500, f"删除不存在用户应返回业务错误：{resp.text}"


def _find_user(user_name: str):
    """按用户名回查列表拿完整记录（若依新增接口不回传 id）"""
    resp = user_api.list({"pageNum": 1, "pageSize": 10, "userName": user_name})
    try:
        rows = resp.json().get("rows") or []
    except Exception:
        return None
    for row in rows:
        if row.get("userName") == user_name:
            return row
    return None