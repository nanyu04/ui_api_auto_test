"""
参数配置和通知公告模块API测试用例
覆盖场景：配置列表/搜索、通知公告列表/搜索
"""
import allure
import pytest

from Api.ConfigApi import ConfigApi
from Api.NoticeApi import NoticeApi


@allure.epic("系统管理接口测试")
@allure.feature("参数配置模块")
@pytest.mark.usefixtures("login_with_token")
class TestConfigManagement:

    @allure.story("参数配置查询")
    @allure.title("查询全部参数配置列表")
    def test_get_config_list(self, login_with_token):
        token = login_with_token
        api = ConfigApi()
        api.set_token(token)
        with allure.step("查询参数配置列表"):
            resp = api.list_config(params={"pageNum": 1, "pageSize": 10})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200
            assert "rows" in result

    @allure.story("参数配置搜索")
    @allure.title("按配置名称搜索")
    def test_search_config_by_name(self, login_with_token):
        token = login_with_token
        api = ConfigApi()
        api.set_token(token)
        with allure.step("按configName=用户管理搜索"):
            resp = api.list_config(params={"pageNum": 1, "pageSize": 10, "configName": "用户管理"})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200

    @allure.story("参数配置搜索")
    @allure.title("按配置键名搜索")
    def test_search_config_by_key(self, login_with_token):
        token = login_with_token
        api = ConfigApi()
        api.set_token(token)
        with allure.step("按configKey搜索"):
            resp = api.list_config(params={"pageNum": 1, "pageSize": 10, "configKey": "sys.user.initPassword"})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200

    @allure.story("参数配置缓存")
    @allure.title("刷新参数缓存")
    def test_refresh_config_cache(self, login_with_token):
        token = login_with_token
        api = ConfigApi()
        api.set_token(token)
        with allure.step("调用刷新缓存接口"):
            resp = api.refresh_cache()
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200


@allure.epic("系统管理接口测试")
@allure.feature("通知公告模块")
@pytest.mark.usefixtures("login_with_token")
class TestNoticeManagement:

    @allure.story("通知公告查询")
    @allure.title("查询全部通知公告列表")
    def test_get_notice_list(self, login_with_token):
        token = login_with_token
        api = NoticeApi()
        api.set_token(token)
        with allure.step("查询通知公告列表"):
            resp = api.list_notice(params={"pageNum": 1, "pageSize": 10})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200
            assert "rows" in result

    @allure.story("通知公告搜索")
    @allure.title("按公告标题搜索")
    def test_search_notice_by_title(self, login_with_token):
        token = login_with_token
        api = NoticeApi()
        api.set_token(token)
        with allure.step("按noticeTitle搜索"):
            resp = api.list_notice(params={"pageNum": 1, "pageSize": 10, "noticeTitle": "温馨"})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200

    @allure.story("通知公告搜索")
    @allure.title("按公告类型搜索")
    def test_search_notice_by_type(self, login_with_token):
        token = login_with_token
        api = NoticeApi()
        api.set_token(token)
        with allure.step("按noticeType=1搜索"):
            resp = api.list_notice(params={"pageNum": 1, "pageSize": 10, "noticeType": "1"})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200