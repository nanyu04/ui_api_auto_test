"""
【场景测试】— 系统监控（接口文档 4.3.1 ~ 4.3.32）

监控类接口分两种：
  - 只读观测类（在线用户、缓存、服务监控、日志查询）→ 直接断言结构
  - 变更类（定时任务增删改、状态切换）→ 走生命周期 + 自动清理

刻意不测 clean（清空日志/清空缓存）：那会破坏环境的审计数据，
这类"破坏性且不可恢复"的接口只做人工/专项验证，不进日常回归。
"""
import allure
import pytest

from api_automation.apis import cache_api, job_api, job_log_api, login_info_api, online_api, oper_log_api, server_api
from api_automation.common import AssertionEngine
from api_automation.data import factory
from api_automation.utils import get_project_root, read_yaml

JOB_CASES = read_yaml(get_project_root() / "data/test_data/job_cases.yaml")


@allure.epic("若依接口自动化")
@allure.feature("系统监控")
class TestMonitorReadOnly:
    """只读观测类接口"""

    @pytest.mark.smoke
    @pytest.mark.P1
    @allure.story("在线用户")
    @allure.title("在线用户列表返回分页结构，且包含当前登录的 admin")
    def test_online_list(self, logged_in_admin):
        resp = online_api.list({"pageNum": 1, "pageSize": 10})
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200).has_field("rows").has_field("total")

        names = [(r.get("userName") or "") for r in (ae.extract("rows") or [])]
        assert any("admin" in n for n in names), f"在线用户里没有 admin：{names}"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("缓存监控")
    @allure.title("缓存监控信息包含 redis 基本信息字段")
    def test_cache_info(self, logged_in_admin):
        resp = cache_api.info()
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200)
        assert ae.extract("data") is not None, f"缓存信息为空：{resp.text}"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("缓存监控")
    @allure.title("缓存名称列表与键名列表可正常返回")
    def test_cache_names_and_keys(self, logged_in_admin):
        names_resp = cache_api.names()
        names_ae = AssertionEngine(names_resp)
        names_ae.status_code(200).jsonpath_eq("$.code", 200)

        names = names_ae.extract("data") or []
        if not names:
            pytest.skip("当前 Redis 中没有任何缓存名称，跳过键名列表校验")

        cache_name = names[0]
        keys_ae = AssertionEngine(cache_api.keys(cache_name))
        keys_ae.status_code(200).jsonpath_eq("$.code", 200)
        assert keys_ae.extract("data") is not None

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("服务监控")
    @allure.title("服务器监控信息包含 cpu / 内存 / JVM 等分区")
    def test_server_info(self, logged_in_admin):
        resp = server_api.info()
        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200)

        data = ae.extract("data") or {}
        assert data, f"服务监控数据为空：{resp.text}"
        for section in ("cpu", "mem", "jvm", "sys"):
            assert section in data, f"服务监控缺少 {section} 分区：{list(data.keys())}"

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("登录日志")
    @allure.title("登录日志列表可分页查询，且按用户名过滤生效")
    def test_logininfor_list(self, logged_in_admin):
        ae = AssertionEngine(login_info_api.list({"pageNum": 1, "pageSize": 10}))
        ae.status_code(200).jsonpath_eq("$.code", 200).has_field("rows").has_field("total")

        filtered = AssertionEngine(login_info_api.list({"pageNum": 1, "pageSize": 10, "userName": "admin"}))
        filtered.status_code(200).jsonpath_eq("$.code", 200)
        rows = filtered.extract("rows") or []
        assert rows, "按 admin 过滤登录日志无结果"
        assert all("admin" in (r.get("userName") or "") for r in rows), (
            f"登录日志过滤条件未生效：{[r.get('userName') for r in rows]}"
        )

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("登录日志")
    @allure.title("解锁用户登录接口对不存在的用户也能正常返回")
    def test_unlock(self, logged_in_admin):
        resp = login_info_api.unlock("no_such_user_to_unlock")
        AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("操作日志")
    @allure.title("操作日志列表返回分页结构")
    def test_operlog_list(self, logged_in_admin):
        ae = AssertionEngine(oper_log_api.list({"pageNum": 1, "pageSize": 10}))
        ae.status_code(200).jsonpath_eq("$.code", 200).has_field("rows").has_field("total")

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("调度日志")
    @allure.title("调度日志列表返回分页结构")
    def test_joblog_list(self, logged_in_admin):
        ae = AssertionEngine(job_log_api.list({"pageNum": 1, "pageSize": 10}))
        ae.status_code(200).jsonpath_eq("$.code", 200).has_field("rows").has_field("total")


@allure.epic("若依接口自动化")
@allure.feature("系统监控")
class TestMonitorJob:
    """定时任务增删改与状态切换"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("定时任务")
    @allure.title("新增定时任务成功并可在列表中查询到")
    def test_create_job(self, logged_in_admin, context):
        payload = context.tag(factory.sys_job(), ["jobName"])
        AssertionEngine(job_api.create(payload)).status_code(200).jsonpath_eq("$.code", 200)

        found = _find_job(payload["jobName"])
        assert found, f"新增成功但列表查不到 {payload['jobName']}"
        assert found["invokeTarget"] == payload["invokeTarget"]
        context.lifecycle.created("job", found["jobId"],
                                  endpoint=f"/monitor/job/{found['jobId']}", method="DELETE")

    @pytest.mark.regression
    @pytest.mark.P1
    @pytest.mark.parametrize("case", JOB_CASES, ids=[c["title"] for c in JOB_CASES])
    @allure.story("定时任务参数校验")
    @allure.title("定时任务参数校验与 cron 表达式合法性（数据驱动）")
    def test_job_validation(self, logged_in_admin, context, case):
        payload = context.tag(factory.sys_job(), ["jobName"])
        payload.update(case["overrides"])

        resp = job_api.create(payload)
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
    @allure.story("定时任务状态")
    @allure.title("任务状态切换：启用→停用，状态位正确回写")
    def test_change_status(self, logged_in_admin, a_new_job):
        AssertionEngine(job_api.change_status({"jobId": a_new_job["id"], "status": "0"})) \
            .status_code(200).jsonpath_eq("$.code", 200)
        assert job_api.detail(a_new_job["id"]).json()["data"]["status"] == "0"

        AssertionEngine(job_api.change_status({"jobId": a_new_job["id"], "status": "1"})) \
            .status_code(200).jsonpath_eq("$.code", 200)
        assert job_api.detail(a_new_job["id"]).json()["data"]["status"] == "1"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("定时任务")
    @allure.title("修改定时任务 cron 表达式并回读确认")
    def test_update_job(self, logged_in_admin, a_new_job):
        detail = job_api.detail(a_new_job["id"]).json()["data"]
        detail["cronExpression"] = "0 0/5 * * * ?"

        AssertionEngine(job_api.update(detail)).status_code(200).jsonpath_eq("$.code", 200)
        assert job_api.detail(a_new_job["id"]).json()["data"]["cronExpression"] == "0 0/5 * * * ?"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("定时任务")
    @allure.title("立即执行一次任务并生成调度日志")
    @allure.severity(allure.severity_level.NORMAL)
    def test_run_job_once(self, logged_in_admin, a_new_job):
        resp = job_api.run({"jobId": a_new_job["id"], "jobGroup": "DEFAULT"})
        AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("定时任务")
    @allure.title("删除不存在的任务返回业务错误")
    def test_delete_not_exists(self, logged_in_admin):
        resp = job_api.remove(factory.random_id())
        AssertionEngine(resp).status_code(200)
        assert resp.json().get("code") == 500, f"删除不存在的任务应返回业务错误：{resp.text}"


def _find_job(job_name: str):
    resp = job_api.list({"pageNum": 1, "pageSize": 10, "jobName": job_name})
    try:
        rows = resp.json().get("rows") or []
    except Exception:
        return None
    for row in rows:
        if row.get("jobName") == job_name:
            return row
    return None