from unittest import case

import allure
import parameterized
import pytest

from api_automation._legacy_interface.Api.UserApi import UserApi
from api_automation._legacy_interface.base_Api.base import Api_common
from api_automation._legacy_interface.base_Api.yaml_untils import test_date
from api_automation._legacy_interface.Api.DeptApi import DeptApi


@allure.epic("登录接口测试")
@allure.feature("登录接口")
@allure.story("登录接口类")
@pytest.mark.parametrize("case", test_date)
class TestLogincase:
    @allure.title("正确账号登录")
    def test_login_success(self, case):
        req = case["request"]
        expect = case["validate"]
        username = req["json"]["username"]
        password = req["json"]["password"]
        login_api= UserApi()
        with allure.step("正常调用接口"):
            resp = login_api.login_user(username=username, password=password)
            result = resp.json()
        with allure.step("校验业务返回码200"):
            assert result["code"] == expect["code"]
            assert result["msg"] == expect["msg"]
        with allure.step("校验返回数据中包含JWT令牌token"):
                assert "token" in result
        if result["code"] ==200 :
            with allure.step("提取出token"):
                token=result["token"]
            dept_api = DeptApi()
            with allure.step("将token 传递"):
                dept_api.set_token(token)
            with allure.step("Get请求查询全部部门"):
                dept_resp=dept_api.dept_api()
                dept_res=dept_resp.json()
                print(">>> 部门接口响应:", dept_res)
            with allure.step("验证请求是否正确"):
                assert "data" in dept_res
                assert isinstance(dept_res["data"], list)
                assert len(dept_res["data"]) > 0
                # @allure.title("密码错误，登录失败，返回提示信息")
    # @pytest.mark.parametrize("case2", second_date)
    # def test_login_password_error(self, case2):
    #     login_api = UserApi()
    #
    #     with allure.step("调用登录接口，传入错误密码"):
    #         resp = login_api.login(case2["username"], case2["password"])
    #         result = resp.json()
    #
    #     with allure.step("校验错误码与提示文案"):
    #         assert result["code"] == 500
    #         assert "用户名或密码错误" in result["msg"]
