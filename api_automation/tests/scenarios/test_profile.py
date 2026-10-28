"""
【场景测试】— 个人中心（接口文档 4.2.83 ~ 4.2.86）

注意：这里操作的是登录账号自己的资料，用例结束必须还原，
否则会污染 admin 账号，影响后续用例。
"""
import allure
import pytest

from api_automation.apis import profile_api
from api_automation.common import AssertionEngine


@allure.epic("若依接口自动化")
@allure.feature("个人中心")
class TestProfile:
    """个人信息 / 密码 / 头像"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("个人信息")
    @allure.title("查询个人信息返回当前登录用户与角色/岗位分组")
    def test_get_profile(self, logged_in_admin):
        resp = profile_api.profile()
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200)

        assert ae.extract("data.userName") == "admin", f"个人信息用户名不符：{resp.text}"
        assert ae.extract("data.userId"), "个人信息缺少 userId"

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("个人信息")
    @allure.title("修改个人信息后可在查询中回读到新值，用例结束自动还原")
    def test_update_profile_and_restore(self, logged_in_admin):
        original = profile_api.profile().json()["data"]
        original_nick = original.get("nickName")

        new_nick = "自动化临时昵称"
        try:
            resp = profile_api.update_profile({
                "nickName": new_nick,
                "email": original.get("email"),
                "phonenumber": original.get("phonenumber"),
                "sex": original.get("sex"),
            })
            AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

            assert profile_api.profile().json()["data"]["nickName"] == new_nick, "昵称未更新成功"
        finally:
            # 无论断言是否失败都要还原，避免污染共享账号
            profile_api.update_profile({
                "nickName": original_nick,
                "email": original.get("email"),
                "phonenumber": original.get("phonenumber"),
                "sex": original.get("sex"),
            })
            assert profile_api.profile().json()["data"]["nickName"] == original_nick, "昵称未还原"

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("个人密码")
    @allure.title("旧密码错误时修改密码被拒绝")
    def test_update_pwd_wrong_old_password(self, logged_in_admin):
        resp = profile_api.update_pwd("definitely_wrong_old_pwd", "another_pwd_123")
        AssertionEngine(resp).status_code(200)

        body = resp.json()
        assert body.get("code") == 500, f"旧密码错误竟然修改成功：{resp.text}"
        assert "旧密码错误" in body.get("msg", ""), body.get("msg")

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("个人密码")
    @allure.title("新密码与旧密码相同时被拒绝")
    def test_update_pwd_same_as_old(self, logged_in_admin):
        resp = profile_api.update_pwd("admin123", "admin123")
        AssertionEngine(resp).status_code(200)

        body = resp.json()
        assert body.get("code") == 500, f"新旧密码相同竟然通过：{resp.text}"
        assert "新密码不能与旧密码相同" in body.get("msg", ""), body.get("msg")