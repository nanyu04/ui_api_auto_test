"""
【场景测试】— 权限与越权（安全向）

设计说明：
  普通账号（角色 common）在 .env 里配置后才跑；
  没配置就 skip，而不是伪造一个账号 —— 测试不能因为"造不出环境"就假通过。

  每条越权用例都带"正向对照"：先确认管理员可访问，再确认普通用户被拒绝，
  避免用例因为接口本身不可用而假通过。
"""
import allure
import pytest

from api_automation.apis import user_api
from api_automation.common import AssertionEngine

# 只有管理员角色才有的接口（普通用户角色 common 不含这些权限）
ADMIN_ONLY_GET = [
    ("/system/user/list", {"pageNum": 1, "pageSize": 10}),
    ("/system/role/list", {"pageNum": 1, "pageSize": 10}),
    ("/system/menu/list", None),
    ("/system/dept/list", None),
    ("/system/config/list", {"pageNum": 1, "pageSize": 10}),
    ("/monitor/operlog/list", {"pageNum": 1, "pageSize": 10}),
]


def _denied(resp) -> bool:
    """兼容两种拒绝语义：HTTP 401/403，或 HTTP 200 但业务码 401/403"""
    if resp.status_code in (401, 403):
        return True
    try:
        return resp.json().get("code") in (401, 403)
    except Exception:
        return False


@allure.epic("若依接口自动化")
@allure.feature("权限与越权")
class TestAuthorization:
    """越权访问拦截"""

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("越权访问")
    @allure.title("普通用户访问管理员接口被拒绝，且不返回任何业务数据")
    @pytest.mark.parametrize("url,params", ADMIN_ONLY_GET, ids=[u for u, _ in ADMIN_ONLY_GET])#直接给这个解包了解开成list了
    def test_common_user_cannot_access_admin_api(self, logged_in_admin, common_client, url, params):
        # 正向对照：管理员访问同一接口必须成功，否则说明是接口本身坏了，而不是权限生效
        admin_resp = user_api.client.get(url, params=params)
        assert not _denied(admin_resp), (
            f"正向对照失败：管理员访问 {url} 也被拒绝：HTTP {admin_resp.status_code} {admin_resp.text[:200]}"
        )

        resp = common_client.get(url, params=params)
        body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}

        assert _denied(resp), (
            f"普通用户竟然能访问 {url}：HTTP {resp.status_code} {resp.text[:200]}"
        )
        assert "rows" not in body and "data" not in body, (
            f"被拒绝的响应里仍带回了业务数据：{resp.text[:200]}"
        )

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("越权写入")
    @allure.title("普通用户尝试新增用户被拒绝，且系统未产生新用户")
    def test_common_user_cannot_create_user(self, logged_in_admin, common_client, context):
        payload = context.tag({
            "userName": "ry_forbidden_001",
            "nickName": "越权测试账号",
            "password": "admin123",
            "deptId": 103,
            "email": "",
            "phonenumber": "",
            "sex": "0",
            "status": "0",
            "roleIds": [],
            "postIds": [],
            "remark": "",
        }, ["userName"])

        resp = common_client.post("/system/user", json=payload)
        assert _denied(resp), f"普通用户竟然能新增用户：HTTP {resp.status_code} {resp.text[:200]}"

        # 确认真的没落库
        found = user_api.list({"pageNum": 1, "pageSize": 10, "userName": payload["userName"]}).json()
        assert not (found.get("rows") or []), f"越权请求竟然落库了：{found.get('rows')}"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("越权删除")
    @allure.title("普通用户尝试删除其他用户被拒绝，目标用户仍存在")
    def test_common_user_cannot_delete_others(self, logged_in_admin, common_client, a_new_user):
        resp = common_client.delete(f"/system/user/{a_new_user['id']}")
        assert _denied(resp), f"普通用户竟然能删除用户：HTTP {resp.status_code} {resp.text[:200]}"

        assert user_api.detail(a_new_user["id"]).json().get("code") == 200, (
            "越权删除竟然生效了，目标用户已不存在"
        )

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("权限标识")
    @allure.title("管理员 getInfo 返回的权限集合覆盖用户管理写权限")
    def test_admin_permissions_contain_write_scopes(self, logged_in_admin):
        from api_automation.apis import auth_api

        resp = auth_api.get_info()
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200)

        perms = ae.extract("permissions") or []
        assert "*:*:*" in perms or "system:user:add" in perms, (
            f"admin 权限集合异常：{perms[:10]}"
        )