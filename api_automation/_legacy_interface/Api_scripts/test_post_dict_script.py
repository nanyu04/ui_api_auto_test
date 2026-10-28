"""
岗位和字典模块API测试用例
覆盖场景：岗位列表/搜索、字典类型/数据查询
"""
import allure
import pytest

from api_automation._legacy_interface.Api.PostApi import PostApi
from api_automation._legacy_interface.Api.DictApi import DictApi


@allure.epic("系统管理接口测试")
@allure.feature("岗位管理模块")
@pytest.mark.usefixtures("login_with_token")
class TestPostManagement:

    @allure.story("岗位查询")
    @allure.title("查询全部岗位列表")
    def test_get_post_list(self, login_with_token):
        token = login_with_token
        api = PostApi()
        api.set_token(token)
        with allure.step("查询岗位列表"):
            resp = api.list_post(params={"pageNum": 1, "pageSize": 10})
            result = resp.json()
        with allure.step("校验返回码200且有rows"):
            assert result["code"] == 200
            assert "rows" in result

    @allure.story("岗位搜索")
    @allure.title("按岗位名称搜索")
    def test_search_post_by_name(self, login_with_token):
        token = login_with_token
        api = PostApi()
        api.set_token(token)
        with allure.step("按postName=董事长搜索"):
            resp = api.list_post(params={"pageNum": 1, "pageSize": 10, "postName": "董事长"})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200

    @allure.story("岗位搜索")
    @allure.title("按岗位编码搜索")
    def test_search_post_by_code(self, login_with_token):
        token = login_with_token
        api = PostApi()
        api.set_token(token)
        with allure.step("按postCode=ceo搜索"):
            resp = api.list_post(params={"pageNum": 1, "pageSize": 10, "postCode": "ceo"})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200


@allure.epic("系统管理接口测试")
@allure.feature("字典管理模块")
@pytest.mark.usefixtures("login_with_token")
class TestDictManagement:

    @allure.story("字典类型查询")
    @allure.title("查询全部字典类型列表")
    def test_get_dict_type_list(self, login_with_token):
        token = login_with_token
        api = DictApi()
        api.set_token(token)
        with allure.step("查询字典类型列表"):
            resp = api.list_dict_type(params={"pageNum": 1, "pageSize": 10})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200
            assert "rows" in result

    @allure.story("字典数据查询")
    @allure.title("查询用户性别字典数据")
    def test_get_dict_data_by_type(self, login_with_token):
        token = login_with_token
        api = DictApi()
        api.set_token(token)
        with allure.step("查询dictType=sys_user_sex的字典数据"):
            resp = api.get_dict_data("sys_user_sex")
            result = resp.json()
        with allure.step("校验返回码200且有数据"):
            assert result["code"] == 200
            assert "data" in result

    @allure.story("字典数据查询")
    @allure.title("查询通知类型字典数据")
    def test_get_dict_data_notice_type(self, login_with_token):
        token = login_with_token
        api = DictApi()
        api.set_token(token)
        with allure.step("查询dictType=sys_notice_type的字典数据"):
            resp = api.get_dict_data("sys_notice_type")
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200