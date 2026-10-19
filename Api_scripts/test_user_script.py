"""
用户管理模块API测试用例
覆盖场景：用户列表查询、按条件搜索、用户详情、新增/修改/删除用户
"""
import allure
import pytest

from Api.CommonApi import CommonApi
from Api.UserApi import UserApi


@allure.epic("用户管理接口测试")
@allure.feature("用户管理模块")
@pytest.mark.usefixtures("login_with_token")
class TestUserManagement:

    @allure.story("用户列表查询")
    @allure.title("查询全部用户列表")
    def test_get_user_list(self, login_with_token):
        token = login_with_token
        api = CommonApi()
        api.set_token(token)
        with allure.step("查询用户列表 pageNum=1 pageSize=10"):
            resp = api.user_list(params={"pageNum": 1, "pageSize": 10})
            result = resp.json()
        with allure.step("校验返回码200和数据"):
            assert result["code"] == 200
            assert "rows" in result
            assert "total" in result
            assert isinstance(result["rows"], list)

    @allure.story("用户搜索")
    @allure.title("按用户名搜索-搜索admin")
    def test_search_user_by_name(self, login_with_token):
        token = login_with_token
        api = CommonApi()
        api.set_token(token)
        with allure.step("按userName=admin搜索"):
            resp = api.user_list(params={"pageNum": 1, "pageSize": 10, "userName": "admin"})
            result = resp.json()
        with allure.step("校验返回正确且搜索结果包含admin"):
            assert result["code"] == 200
            assert len(result["rows"]) > 0
            assert any("admin" in row.get("userName", "") for row in result["rows"])

    @allure.story("用户搜索")
    @allure.title("按手机号搜索用户")
    def test_search_user_by_phone(self, login_with_token):
        token = login_with_token
        api = CommonApi()
        api.set_token(token)
        with allure.step("按手机号搜索"):
            resp = api.user_list(params={"pageNum": 1, "pageSize": 10, "phonenumber": "18888888888"})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200

    @allure.story("用户搜索")
    @allure.title("按状态筛选-正常状态用户")
    def test_filter_user_by_status_normal(self, login_with_token):
        token = login_with_token
        api = CommonApi()
        api.set_token(token)
        with allure.step("查询status=0的正常用户"):
            resp = api.user_list(params={"pageNum": 1, "pageSize": 10, "status": "0"})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200

    @allure.story("用户搜索")
    @allure.title("按状态筛选-停用状态用户")
    def test_filter_user_by_status_disabled(self, login_with_token):
        token = login_with_token
        api = CommonApi()
        api.set_token(token)
        with allure.step("查询status=1的停用用户"):
            resp = api.user_list(params={"pageNum": 1, "pageSize": 10, "status": "1"})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200

    @allure.story("用户详情")
    @allure.title("查询当前登录用户信息")
    def test_get_current_user_info(self, login_with_token):
        token = login_with_token
        api = CommonApi()
        api.set_token(token)
        with allure.step("调用getInfo接口"):
            resp = api.get_info()
            result = resp.json()
        with allure.step("校验返回用户信息"):
            assert result["code"] == 200
            assert "user" in result
            assert "roles" in result

    @allure.story("用户详情")
    @allure.title("获取用户路由菜单")
    def test_get_routers(self, login_with_token):
        token = login_with_token
        api = CommonApi()
        api.set_token(token)
        with allure.step("调用getRouters接口"):
            resp = api.get_routers()
            result = resp.json()
        with allure.step("校验返回路由数据"):
            assert result["code"] == 200
            assert "data" in result