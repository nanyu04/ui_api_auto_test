"""
登录模块API测试用例
覆盖场景：正常登录、密码错误、用户名为空、密码为空、不存在的用户
"""
import allure
import pytest

from Api.UserApi import UserApi


@allure.epic("登录接口测试")
@allure.feature("登录模块")
@pytest.mark.usefixtures("base_api")
class TestLogin:

    @allure.story("正确账号登录")
    @allure.title("正确账号密码登录-返回token")
    def test_login_success(self, base_api):
        login_api = UserApi()
        with allure.step("使用admin/admin123调用登录接口"):
            resp = login_api.login_user(username="admin", password="admin123")
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200
            assert result["msg"] == "操作成功"
        with allure.step("校验返回token"):
            assert "token" in result
            assert len(result["token"]) > 0

    @allure.story("密码错误登录")
    @allure.title("错误密码登录-返回500")
    def test_login_wrong_password(self, base_api):
        login_api = UserApi()
        with allure.step("使用错误密码调用登录接口"):
            resp = login_api.login_user(username="admin", password="wrongpassword")
            result = resp.json()
        with allure.step("校验返回码500"):
            assert result["code"] == 500
            assert "用户不存在/密码错误" in result["msg"]

    @allure.story("用户名为空登录")
    @allure.title("用户名为空登录-返回500")
    def test_login_empty_username(self, base_api):
        login_api = UserApi()
        with allure.step("用户名为空调用登录"):
            resp = login_api.login_user(username="", password="admin123")
            result = resp.json()
        with allure.step("校验返回错误码"):
            assert result["code"] == 500

    @allure.story("密码为空登录")
    @allure.title("密码为空登录-返回500")
    def test_login_empty_password(self, base_api):
        login_api = UserApi()
        with allure.step("密码为空调用登录"):
            resp = login_api.login_user(username="admin", password="")
            result = resp.json()
        with allure.step("校验返回错误码"):
            assert result["code"] == 500

    @allure.story("不存在的用户登录")
    @allure.title("不存在用户登录-返回500")
    def test_login_nonexist_user(self, base_api):
        login_api = UserApi()
        with allure.step("使用不存在的用户登录"):
            resp = login_api.login_user(username="nonexist_user", password="admin123")
            result = resp.json()
        with allure.step("校验返回错误码和提示"):
            assert result["code"] == 500
            assert "用户不存在/密码错误" in result["msg"]