"""
【场景测试】— 字典管理（接口文档 4.2.51 ~ 4.2.65）

字典是"类型 + 数据"两张表，这里重点验证两者的联动与正则约束。
"""
import allure
import pytest

from api_automation.apis import dict_data_api, dict_type_api
from api_automation.common import AssertionEngine
from api_automation.data import factory
from api_automation.utils import get_project_root, read_yaml

TYPE_CASES = read_yaml(get_project_root() / "data/test_data/dict_type_cases.yaml")
DATA_CASES = read_yaml(get_project_root() / "data/test_data/dict_data_cases.yaml")


@allure.epic("若依接口自动化")
@allure.feature("字典管理")
class TestDictType:
    """字典类型"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("字典类型")
    @allure.title("新增字典类型成功并可在列表中查询到")
    def test_create_dict_type(self, logged_in_admin, context):
        payload = context.tag(factory.sys_dict_type(), ["dictType"])
        AssertionEngine(dict_type_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_type(payload["dictType"])
        assert found, f"新增成功但列表查不到 {payload['dictType']}"
        context.lifecycle.created("dictType", found["dictId"],
                                  endpoint=f"/system/dict/type/{found['dictId']}", method="DELETE")

    @pytest.mark.regression
    @pytest.mark.P1
    @pytest.mark.parametrize("case", TYPE_CASES, ids=[c["title"] for c in TYPE_CASES])
    @allure.story("字典类型参数校验")
    @allure.title("字典类型参数校验与正则约束（数据驱动）")
    def test_dict_type_validation(self, logged_in_admin, context, case):
        payload = context.tag(factory.sys_dict_type(), ["dictType"])
        payload.update(case["overrides"])

        resp = dict_type_api.create(payload)
        body = resp.json()
        AssertionEngine(resp).status_code(200)
        assert body.get("code") == case["expect_code"], (
            f"[{case['title']}] 期望 code={case['expect_code']}，实际 {body.get('code')}：{resp.text}"
        )
        if case.get("expect_msg"):
            assert case["expect_msg"] in body.get("msg", ""), (
                f"[{case['title']}] 提示不含 '{case['expect_msg']}'：{body.get('msg')}"
            )

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("字典类型")
    @allure.title("字典类型生命周期：创建→查详细→改名→删除→确认已删除")
    def test_dict_type_lifecycle(self, logged_in_admin, context):
        payload = context.tag(factory.sys_dict_type(), ["dictType"])
        AssertionEngine(dict_type_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_type(payload["dictType"])
        assert found, "创建后列表查不到字典类型"
        dict_id = found["dictId"]

        updated = dict(found)
        updated["dictName"] = f"改名_{payload['dictName']}"
        AssertionEngine(dict_type_api.update(updated)).status_code(200).jsonpath_eq("$.code", 200)
        assert dict_type_api.detail(dict_id).json()["data"]["dictName"] == updated["dictName"]

        AssertionEngine(dict_type_api.remove(dict_id)).status_code(200).jsonpath_eq("$.code", 200)
        assert dict_type_api.detail(dict_id).json().get("code") == 500, "删除后仍能查到该类型"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("字典缓存")
    @allure.title("刷新字典缓存返回成功")
    def test_refresh_cache(self, logged_in_admin):
        AssertionEngine(dict_type_api.refresh_cache()).status_code(200).jsonpath_eq("$.code", 200)

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("字典类型下拉项")
    @allure.title("获取字典类型下拉选项返回数据")
    def test_option_select(self, logged_in_admin):
        ae = AssertionEngine(dict_type_api.option_select())
        ae.status_code(200).jsonpath_eq("$.code", 200)
        assert ae.extract("data") is not None, "字典类型下拉选项不应为 null"


@allure.epic("若依接口自动化")
@allure.feature("字典管理")
class TestDictData:
    """字典数据"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("字典数据")
    @allure.title("在新建字典类型下新增字典数据，并可按类型查询到")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_dict_data(self, logged_in_admin, a_new_dict_type, context):
        payload = context.tag(
            factory.sys_dict_data(a_new_dict_type["dictType"]), ["dictLabel"])
        AssertionEngine(dict_data_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        # 按类型查询：这是前端下拉框真正走的接口
        by_type = dict_data_api.by_type(a_new_dict_type["dictType"])
        ae = AssertionEngine(by_type)
        ae.status_code(200).jsonpath_eq("$.code", 200)

        rows = ae.extract("data") or []
        assert rows, f"按类型 {a_new_dict_type['dictType']} 查询不到字典数据"
        assert any(r.get("dictLabel") == payload["dictLabel"] for r in rows), (
            f"新增的字典标签未出现在结果中：{[r.get('dictLabel') for r in rows]}"
        )

        found = _find_data(a_new_dict_type["dictType"], payload["dictLabel"])
        if found:
            context.lifecycle.created("dictData", found["dictCode"],
                                      endpoint=f"/system/dict/data/{found['dictCode']}", method="DELETE")

    @pytest.mark.regression
    @pytest.mark.P1
    @pytest.mark.parametrize("case", DATA_CASES, ids=[c["title"] for c in DATA_CASES])
    @allure.story("字典数据参数校验")
    @allure.title("字典数据参数校验（数据驱动）")
    def test_dict_data_validation(self, logged_in_admin, a_new_dict_type, context, case):
        payload = context.tag(
            factory.sys_dict_data(a_new_dict_type["dictType"]), ["dictLabel"])
        payload.update(case["overrides"])

        resp = dict_data_api.create(payload)
        body = resp.json()
        AssertionEngine(resp).status_code(200)
        assert body.get("code") == case["expect_code"], (
            f"[{case['title']}] 期望 code={case['expect_code']}，实际 {body.get('code')}：{resp.text}"
        )
        if case.get("expect_msg"):
            assert case["expect_msg"] in body.get("msg", ""), (
                f"[{case['title']}] 提示不含 '{case['expect_msg']}'：{body.get('msg')}"
            )

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("字典数据")
    @allure.title("字典数据生命周期：创建→改标签→删除→确认已删除")
    def test_dict_data_lifecycle(self, logged_in_admin, a_new_dict_type, context):
        payload = context.tag(
            factory.sys_dict_data(a_new_dict_type["dictType"]), ["dictLabel"])
        AssertionEngine(dict_data_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_data(a_new_dict_type["dictType"], payload["dictLabel"])
        assert found, "创建后查不到字典数据"
        dict_code = found["dictCode"]

        updated = dict(found)
        updated["dictLabel"] = f"改名_{payload['dictLabel']}"
        AssertionEngine(dict_data_api.update(updated)).status_code(200).jsonpath_eq("$.code", 200)
        assert dict_data_api.detail(dict_code).json()["data"]["dictLabel"] == updated["dictLabel"]

        AssertionEngine(dict_data_api.remove(dict_code)).status_code(200).jsonpath_eq("$.code", 200)
        assert dict_data_api.detail(dict_code).json().get("code") == 500, "删除后仍能查到该数据"


def _find_type(dict_type: str):
    resp = dict_type_api.list({"pageNum": 1, "pageSize": 10, "dictType": dict_type})
    try:
        rows = resp.json().get("rows") or []
    except Exception:
        return None
    for row in rows:
        if row.get("dictType") == dict_type:
            return row
    return None


def _find_data(dict_type: str, dict_label: str):
    resp = dict_data_api.list({"pageNum": 1, "pageSize": 10, "dictType": dict_type})
    try:
        rows = resp.json().get("rows") or []
    except Exception:
        return None
    for row in rows:
        if row.get("dictLabel") == dict_label:
            return row
    return None
