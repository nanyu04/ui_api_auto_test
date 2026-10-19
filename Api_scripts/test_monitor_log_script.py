"""
监控管理和日志模块API测试用例
覆盖场景：服务器信息、在线用户、定时任务、缓存、登录日志、操作日志
"""
import allure
import pytest

from Api.MonitorApi import MonitorApi
from Api.LogApi import LogApi


@allure.epic("监控管理接口测试")
@allure.feature("监控模块")
@pytest.mark.usefixtures("login_with_token")
class TestMonitorManagement:

    @allure.story("服务器监控")
    @allure.title("查询服务器运行信息")
    def test_get_server_info(self, login_with_token):
        token = login_with_token
        api = MonitorApi()
        api.set_token(token)
        with allure.step("调用服务器信息接口"):
            resp = api.server_info()
            result = resp.json()
        with allure.step("校验返回系统信息"):
            assert result["code"] == 200
            assert "data" in result

    @allure.story("在线用户")
    @allure.title("查询在线用户列表")
    def test_get_online_users(self, login_with_token):
        token = login_with_token
        api = MonitorApi()
        api.set_token(token)
        with allure.step("查询在线用户列表"):
            resp = api.online_user_list(params={"pageNum": 1, "pageSize": 10})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200
            assert "rows" in result

    @allure.story("定时任务")
    @allure.title("查询定时任务列表")
    def test_get_job_list(self, login_with_token):
        token = login_with_token
        api = MonitorApi()
        api.set_token(token)
        with allure.step("查询定时任务列表"):
            resp = api.job_list(params={"pageNum": 1, "pageSize": 10})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200
            assert "rows" in result

    @allure.story("缓存监控")
    @allure.title("查询Redis缓存信息")
    def test_get_cache_info(self, login_with_token):
        token = login_with_token
        api = MonitorApi()
        api.set_token(token)
        with allure.step("查询缓存信息"):
            resp = api.cache_info()
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200

    @allure.story("缓存监控")
    @allure.title("查询缓存名称列表")
    def test_get_cache_names(self, login_with_token):
        token = login_with_token
        api = MonitorApi()
        api.set_token(token)
        with allure.step("查询缓存名称"):
            resp = api.cache_names()
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200


@allure.epic("日志管理接口测试")
@allure.feature("日志模块")
@pytest.mark.usefixtures("login_with_token")
class TestLogManagement:

    @allure.story("登录日志")
    @allure.title("查询登录日志列表")
    def test_get_login_log_list(self, login_with_token):
        token = login_with_token
        api = LogApi()
        api.set_token(token)
        with allure.step("查询登录日志"):
            resp = api.login_log_list(params={"pageNum": 1, "pageSize": 10})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200
            assert "rows" in result

    @allure.story("操作日志")
    @allure.title("查询操作日志列表")
    def test_get_oper_log_list(self, login_with_token):
        token = login_with_token
        api = LogApi()
        api.set_token(token)
        with allure.step("查询操作日志"):
            resp = api.oper_log_list(params={"pageNum": 1, "pageSize": 10})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200
            assert "rows" in result

    @allure.story("操作日志")
    @allure.title("按模块名称搜操作日志")
    def test_search_oper_log_by_title(self, login_with_token):
        token = login_with_token
        api = LogApi()
        api.set_token(token)
        with allure.step("按title搜索操作日志"):
            resp = api.oper_log_list(params={"pageNum": 1, "pageSize": 10, "title": "用户管理"})
            result = resp.json()
        with allure.step("校验返回码200"):
            assert result["code"] == 200