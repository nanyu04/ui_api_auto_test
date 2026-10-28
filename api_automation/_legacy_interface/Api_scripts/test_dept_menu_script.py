"""
部门和菜单模块API测试用例
覆盖场景：部门列表/树查询、菜单列表/树查询
"""
import allure
import pytest

from api_automation._legacy_interface.Api.CommonApi import CommonApi
from api_automation._legacy_interface.Api.DeptApi import DeptApi
from api_automation._legacy_interface.Api.MenuApi import MenuApi


@allure.epic("组织架构接口测试")
@allure.feature("部门管理模块")
@pytest.mark.usefixtures("login_with_token")
class TestDeptManagement:

    @allure.story("部门查询")
    @allure.title("查询全部部门列表")
    def test_get_dept_list(self, login_with_token):
        token = login_with_token
        api = DeptApi()
        api.set_token(token)
        with allure.step("调用部门列表接口"):
            resp = api.dept_api()
            result = resp.json()
        with allure.step("校验返回码200且有数据"):
            assert result["code"] == 200
            assert "data" in result
            assert isinstance(result["data"], list)
            assert len(result["data"]) > 0

    @allure.story("部门查询")
    @allure.title("查询部门树下拉结构")
    def test_get_dept_treeselect(self, login_with_token):
        token = login_with_token
        api = CommonApi()
        api.set_token(token)
        with allure.step("调用部门树接口"):
            resp = api.dept_treeselect()
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200
            assert "data" in result


@allure.epic("组织架构接口测试")
@allure.feature("菜单管理模块")
@pytest.mark.usefixtures("login_with_token")
class TestMenuManagement:

    @allure.story("菜单查询")
    @allure.title("查询全部菜单列表")
    def test_get_menu_list(self, login_with_token):
        token = login_with_token
        api = MenuApi()
        api.set_token(token)
        with allure.step("调用菜单列表接口"):
            resp = api.list_menu()
            result = resp.json()
        with allure.step("校验返回码200且有数据"):
            assert result["code"] == 200
            assert "data" in result
            assert isinstance(result["data"], list)

    @allure.story("菜单查询")
    @allure.title("查询菜单树下拉结构")
    def test_get_menu_treeselect(self, login_with_token):
        token = login_with_token
        api = MenuApi()
        api.set_token(token)
        with allure.step("调用菜单树下拉接口"):
            resp = api.treeselect()
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200
            assert "data" in result

    @allure.story("菜单查询")
    @allure.title("根据角色ID查询菜单树")
    def test_get_role_menu_treeselect(self, login_with_token):
        token = login_with_token
        api = MenuApi()
        api.set_token(token)
        with allure.step("查询角色ID=1的菜单树"):
            resp = api.role_menu_treeselect(1)
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200