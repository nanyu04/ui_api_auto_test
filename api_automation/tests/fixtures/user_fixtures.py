"""
【共享 Fixture】— 登录身份 + "新建即自动清理"的测试数据

设计要点：
  1. 登录成功后把 token 写进共享 Session，之后所有接口模块自动带鉴权；
  2. 若依的新增接口只返回 {code,msg}，不回传主键，
     所以创建后必须回查列表拿到 id，否则清理时无从下手；
  3. 每条数据创建成功就登记到 context.lifecycle，用例结束自动删除。
"""
import pytest

from api_automation.apis import (
    auth_api, user_api, role_api, dept_api, post_api,
    menu_api, dict_type_api, dict_data_api, config_api, notice_api, job_api,
)
from api_automation.common import AssertionEngine, HttpClient, logger
from api_automation.config import settings
from api_automation.data import factory


# ==================== 内部小工具 ====================

def _body(resp) -> dict:
    """安全取 JSON（非 JSON 响应返回空字典，避免用例因解析异常报错）"""
    try:
        return resp.json()
    except Exception:
        return {}


def _first_id(resp, key: str, container: str = "rows"):
    """从列表响应的第一条记录里取主键，取不到返回 None"""
    items = _body(resp).get(container) or []
    return items[0].get(key) if items else None


def _require_login(resp):
    """登录响应必须成功，否则后续用例的失败信息会非常难排查"""
    body = _body(resp)
    assert body.get("code") == 200, (
        f"登录失败：HTTP {resp.status_code}，响应 {resp.text}\n"
        f"请检查被测服务是否已启动、账号密码是否正确、"
        f"以及 sys.account.captchaEnabled 是否为 false。"
    )
    token = body.get("token")
    assert token, f"登录成功但未返回 token：{resp.text}"
    return token


# ==================== 登录身份 ====================

@pytest.fixture
def logged_in_admin():
    """
    用 admin 登录，并把 token 写入共享 Session。

    所有接口模块共用同一个 HttpClient，所以这里设置一次即可全局生效。
    """
    resp = auth_api.login(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)
    token = _require_login(resp)
    auth_api.client.set_token(token)
    logger.info("🔐 admin 登录成功，token 已注入共享会话")
    yield token
    auth_api.client.clear_auth()


@pytest.fixture
def common_client():
    """
    普通用户（角色 common）的独立会话，用于越权用例。

    单独建一个 HttpClient 而不是复用共享会话：
    否则会把 admin 的 token 覆盖掉，导致同一用例里"管理员上下文"失效。
    """
    if not settings.COMMON_USERNAME or not settings.COMMON_PASSWORD:
        raise RuntimeError(
            ".env 中未配置 COMMON_USERNAME / COMMON_PASSWORD，越权用例无法执行"
        )

    client = HttpClient()
    resp = client.post("/login", json={
        "username": settings.COMMON_USERNAME,
        "password": settings.COMMON_PASSWORD,
    })
    body = _body(resp)
    if body.get("code") != 200 or not body.get("token"):
        client.close()
        raise RuntimeError(f"普通账号登录失败，越权用例终止：{resp.text}")
    client.set_token(body["token"])
    logger.info("🔐 普通账号登录成功（独立会话）")
    yield client
    client.close()


# ==================== 新建即清理的数据 ====================

@pytest.fixture
def a_new_user(logged_in_admin, context):
    """创建一个测试用户，用例结束自动删除"""
    payload = context.tag(factory.sys_user(), ["userName"])
    resp = user_api.create(payload)
    AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    user_id = _first_id(user_api.list({"userName": payload["userName"]}), "userId")
    if user_id:
        context.lifecycle.created(
            "user", user_id, endpoint=f"/system/user/{user_id}", method="DELETE")
    return {"id": user_id, "userName": payload["userName"], "payload": payload}


@pytest.fixture
def a_new_role(logged_in_admin, context):
    """创建一个测试角色，用例结束自动删除"""
    payload = context.tag(factory.sys_role(), ["roleName"])
    resp = role_api.create(payload)
    AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    role_id = _first_id(role_api.list({"roleName": payload["roleName"]}), "roleId")
    if role_id:
        context.lifecycle.created(
            "role", role_id, endpoint=f"/system/role/{role_id}", method="DELETE")
    return {"id": role_id, "payload": payload}


@pytest.fixture
def a_new_dept(logged_in_admin, context):
    """创建一个测试部门，用例结束自动删除"""
    payload = context.tag(factory.sys_dept(), ["deptName"])
    resp = dept_api.create(payload)
    AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    # 部门列表返回的是树形结构（data），不是 rows
    dept_id = _first_id(dept_api.list({"deptName": payload["deptName"]}), "deptId", container="data")
    if dept_id:
        context.lifecycle.created(
            "dept", dept_id, endpoint=f"/system/dept/{dept_id}", method="DELETE")
    return {"id": dept_id, "payload": payload}


@pytest.fixture
def a_new_post(logged_in_admin, context):
    """创建一个测试岗位，用例结束自动删除"""
    payload = context.tag(factory.sys_post(), ["postCode"])
    resp = post_api.create(payload)
    AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    post_id = _first_id(post_api.list({"postCode": payload["postCode"]}), "postId")
    if post_id:
        context.lifecycle.created(
            "post", post_id, endpoint=f"/system/post/{post_id}", method="DELETE")
    return {"id": post_id, "payload": payload}


@pytest.fixture
def a_new_menu(logged_in_admin, context):
    """创建一个测试菜单（顶级目录），用例结束自动删除"""
    payload = context.tag(factory.sys_menu(), ["menuName"])
    resp = menu_api.create(payload)
    AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    # 菜单列表同样是树形结构（data）
    menu_id = _first_id(menu_api.list({"menuName": payload["menuName"]}), "menuId", container="data")
    if menu_id:
        context.lifecycle.created(
            "menu", menu_id, endpoint=f"/system/menu/{menu_id}", method="DELETE")
    return {"id": menu_id, "payload": payload}


@pytest.fixture
def a_new_dict_type(logged_in_admin, context):
    """创建一个测试字典类型，用例结束自动删除"""
    payload = context.tag(factory.sys_dict_type(), ["dictType"])
    resp = dict_type_api.create(payload)
    AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    dict_id = _first_id(dict_type_api.list({"dictType": payload["dictType"]}), "dictId")
    if dict_id:
        context.lifecycle.created(
            "dictType", dict_id, endpoint=f"/system/dict/type/{dict_id}", method="DELETE")
    return {"id": dict_id, "dictType": payload["dictType"], "payload": payload}


@pytest.fixture
def a_new_dict_data(a_new_dict_type, context):
    """在新建的字典类型下挂一条字典数据，用例结束自动删除"""
    payload = context.tag(
        factory.sys_dict_data(a_new_dict_type["dictType"]), ["dictLabel"])
    resp = dict_data_api.create(payload)
    AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    dict_code = _first_id(dict_data_api.list({"dictType": payload["dictType"]}), "dictCode")
    if dict_code:
        context.lifecycle.created(
            "dictData", dict_code, endpoint=f"/system/dict/data/{dict_code}", method="DELETE")
    return {"id": dict_code, "dictType": payload["dictType"], "payload": payload}


@pytest.fixture
def a_new_config(logged_in_admin, context):
    """创建一个测试参数，用例结束自动删除"""
    payload = context.tag(factory.sys_config(), ["configKey"])
    resp = config_api.create(payload)
    AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    config_id = _first_id(config_api.list({"configKey": payload["configKey"]}), "configId")
    if config_id:
        context.lifecycle.created(
            "config", config_id, endpoint=f"/system/config/{config_id}", method="DELETE")
    return {"id": config_id, "configKey": payload["configKey"], "payload": payload}


@pytest.fixture
def a_new_notice(logged_in_admin, context):
    """创建一条测试公告，用例结束自动删除"""
    payload = context.tag(factory.sys_notice(), ["noticeTitle"])
    resp = notice_api.create(payload)
    AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    notice_id = _first_id(notice_api.list({"noticeTitle": payload["noticeTitle"]}), "noticeId")
    if notice_id:
        context.lifecycle.created(
            "notice", notice_id, endpoint=f"/system/notice/{notice_id}", method="DELETE")
    return {"id": notice_id, "payload": payload}


@pytest.fixture
def a_new_job(logged_in_admin, context):
    """创建一个测试定时任务，用例结束自动删除（先停用再删，避免调度器持有）"""
    payload = context.tag(factory.sys_job(), ["jobName"])
    resp = job_api.create(payload)
    AssertionEngine(resp).status_code(200).jsonpath_eq("$.code", 200)

    job_id = _first_id(job_api.list({"jobName": payload["jobName"]}), "jobId")
    if job_id:
        context.lifecycle.created(
            "job", job_id, endpoint=f"/monitor/job/{job_id}", method="DELETE")
    return {"id": job_id, "payload": payload}
