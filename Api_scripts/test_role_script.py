"""
角色管理模块API测试用例
覆盖场景：角色列表查询、按条件搜索、角色新增/修改/删除
"""
import allure
import pytest

from Api.CommonApi import CommonApi
from Api.RoleApi import RoleApi


@allure.epic("角色管理接口测试")
@allure.feature("角色管理模块")
@pytest.mark.usefixtures("login_with_token")
class TestRoleManagement:

    @allure.story("角色列表查询")
    @allure.title("查询全部角色列表")
    def test_get_role_list(self, login_with_token):
        token = login_with_token
        api = RoleApi()
        api.set_token(token)
        with allure.step("查询角色列表"):
            resp = api.list_role(params={"pageNum": 1, "pageSize": 10})
            result = resp.json()
        with allure.step("校验返回码200且有rows"):
            assert result["code"] == 200
            assert "rows" in result
            assert isinstance(result["rows"], list)

    @allure.story("角色搜索")
    @allure.title("按角色名称搜索-超级管理员")
    def test_search_role_by_name(self, login_with_token):
        token = login_with_token
        api = RoleApi()
        api.set_token(token)
        with allure.step("按roleName=超级管理员搜索"):
            resp = api.list_role(params={"pageNum": 1, "pageSize": 10, "roleName": "超级管理员"})
            result = resp.json()
        with allure.step("校验返回正确"):
            assert result["code"] == 200
            assert len(result["rows"]) > 0

    @allure.story("角色搜索")
    @allure.title("按角色状态搜索")
    def test_search_role_by_status(self, login_with_token):
        token = login_with_token
        api = RoleApi()
        api.set_token(token)
        with allure.step("查询status=0的角色"):
            resp = api.list_role(params={"pageNum": 1, "pageSize": 10, "status": "0"})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200

    @allure.story("角色详情")
    @allure.title("根据角色ID查询角色详情")
    def test_get_role_detail(self, login_with_token):
        token = login_with_token
        api = RoleApi()
        api.set_token(token)
        with allure.step("先获取角色列表取第一个角色ID"):
            list_resp = api.list_role(params={"pageNum": 1, "pageSize": 10})
            rows = list_resp.json().get("rows", [])
            if rows:
                role_id = rows[0]["roleId"]
                with allure.step(f"查询角色ID={role_id}的详情"):
                    resp = api.get_role(role_id)
                    result = resp.json()
                    assert result["code"] == 200
                    assert "data" in result

    @allure.story("角色授权用户查询")
    @allure.title("查询角色已授权用户列表")
    def test_get_allocated_users(self, login_with_token):
        token = login_with_token
        api = RoleApi()
        api.set_token(token)
        with allure.step("查询角色ID=1的已授权用户"):
            resp = api.allocated_list(params={"pageNum": 1, "pageSize": 10, "roleId": 1})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200