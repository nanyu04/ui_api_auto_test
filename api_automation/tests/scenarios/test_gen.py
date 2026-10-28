"""
【场景测试】— 代码生成（接口文档 4.4.1 ~ 4.4.13）

只覆盖只读查询接口：导入表结构 / 生成代码 / 下载 zip 都会写磁盘，
不适合放在日常回归里（放进去会让每次执行都在工程目录产出垃圾文件）。
"""
import allure
import pytest

from api_automation.apis import gen_api
from api_automation.common import AssertionEngine
from api_automation.data import factory


@allure.epic("若依接口自动化")
@allure.feature("代码生成")
class TestGen:
    """代码生成只读查询"""

    @pytest.mark.smoke
    @pytest.mark.P1
    @allure.story("代码生成列表")
    @allure.title("代码生成列表返回分页结构")
    def test_gen_list(self, logged_in_admin):
        ae = AssertionEngine(gen_api.list({"pageNum": 1, "pageSize": 10}))
        ae.status_code(200).jsonpath_eq("$.code", 200).has_field("rows").has_field("total")

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("数据库表列表")
    @allure.title("数据库表列表返回分页结构且包含表名字段")
    def test_db_list(self, logged_in_admin):
        resp = gen_api.db_list({"pageNum": 1, "pageSize": 10})
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200).has_field("rows")

        rows = ae.extract("rows") or []
        if rows:
            assert "tableName" in rows[0], f"数据库表列表缺少 tableName：{rows[0]}"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("表详细")
    @allure.title("查询不存在的表详情返回业务错误而不是崩溃")
    def test_gen_detail_not_exists(self, logged_in_admin):
        resp = gen_api.detail(factory.random_id())
        AssertionEngine(resp).status_code(200)
        body = resp.json()
        assert body.get("code") == 500, f"不存在的表应返回业务错误：{resp.text}"