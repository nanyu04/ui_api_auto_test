"""
【数据模型 / 契约】 — RuoYi-Vue 接口契约定义与注册

这里做两件事：
  1. 用 Pydantic 定义常用请求体 —— 构造参数时就能拿到类型与长度约束校验
  2. 向框架的契约注册中心注册各端点的响应 JSON Schema
     注册之后，所有经过 HttpClient 的响应都会自动做结构校验

字段与约束来源：RuoYi-Vue 源码实体类的 getter 注解（@NotBlank/@Size/@Email/@Xss）
"""
from typing import Any, List, Optional

from pydantic import BaseModel, Field

# =============================================================
#  一、请求模型（Pydantic）
# =============================================================


class LoginRequest(BaseModel):
    """登录请求体（/login）"""

    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    code: str = ""
    uuid: str = ""


class UserCreateRequest(BaseModel):
    """新增用户（POST /system/user）—— 约束与 SysUser 实体一致"""

    userName: str = Field(..., min_length=1, max_length=30)
    nickName: str = Field(..., min_length=1, max_length=30)
    password: str = Field(default="admin123")
    deptId: Optional[int] = None
    email: str = Field(default="", max_length=50)
    phonenumber: str = Field(default="", max_length=11)
    sex: str = "0"
    status: str = "0"
    roleIds: List[int] = Field(default_factory=list)
    postIds: List[int] = Field(default_factory=list)
    remark: str = ""


class RoleCreateRequest(BaseModel):
    """新增角色（POST /system/role）"""

    roleName: str = Field(..., min_length=1, max_length=30)
    roleKey: str = Field(..., min_length=1, max_length=100)
    roleSort: int = Field(..., ge=0)
    status: str = "0"
    remark: str = ""
    menuIds: List[int] = Field(default_factory=list)


class DeptCreateRequest(BaseModel):
    """新增部门（POST /system/dept）"""

    deptName: str = Field(..., min_length=1, max_length=30)
    parentId: int = Field(..., ge=0)
    orderNum: int = Field(..., ge=0)
    leader: str = ""
    phone: str = Field(default="", max_length=11)
    email: str = Field(default="", max_length=50)
    status: str = "0"


class PostCreateRequest(BaseModel):
    """新增岗位（POST /system/post）"""

    postCode: str = Field(..., min_length=1, max_length=64)
    postName: str = Field(..., min_length=1, max_length=50)
    postSort: int = Field(..., ge=0)
    status: str = "0"
    remark: str = ""


class DictTypeCreateRequest(BaseModel):
    """新增字典类型（POST /system/dict/type）"""

    dictName: str = Field(..., min_length=1, max_length=100)
    dictType: str = Field(..., min_length=1, max_length=100)
    status: str = "0"
    remark: str = ""


class DictDataCreateRequest(BaseModel):
    """新增字典数据（POST /system/dict/data）"""

    dictLabel: str = Field(..., min_length=1, max_length=100)
    dictValue: str = Field(..., min_length=1, max_length=100)
    dictType: str = Field(..., min_length=1, max_length=100)
    dictSort: int = Field(default=0, ge=0)
    cssClass: str = ""
    listClass: str = "default"
    isDefault: str = "N"
    status: str = "0"
    remark: str = ""


class ConfigCreateRequest(BaseModel):
    """新增参数（POST /system/config）"""

    configName: str = Field(..., min_length=1, max_length=100)
    configKey: str = Field(..., min_length=1, max_length=100)
    configValue: str = Field(..., min_length=1, max_length=500)
    configType: str = "N"
    remark: str = ""


class NoticeCreateRequest(BaseModel):
    """新增公告（POST /system/notice）"""

    noticeTitle: str = Field(..., min_length=1, max_length=50)
    noticeType: str = "1"
    noticeContent: str = ""
    status: str = "0"


class JobCreateRequest(BaseModel):
    """新增定时任务（POST /monitor/job）"""

    jobName: str = Field(..., min_length=1, max_length=64)
    jobGroup: str = "DEFAULT"
    invokeTarget: str = Field(..., min_length=1, max_length=500)
    cronExpression: str = Field(..., min_length=1, max_length=255)
    misfirePolicy: str = "1"
    concurrent: str = "1"
    status: str = "1"


# =============================================================
#  二、响应 JSON Schema
# =============================================================
_DRAFT = "http://json-schema.org/draft-07/schema#"


def _obj(required, properties):
    return {"$schema": _DRAFT, "type": "object", "required": required, "properties": properties}


INT = {"type": "integer"}
STR = {"type": "string"}

# ---------- 通用结构 ----------
AJAX_SCHEMA = _obj(["code", "msg"], {"code": INT, "msg": STR, "data": {}})

TABLE_SCHEMA = _obj(
    ["total", "rows", "code", "msg"],
    {"total": {"type": "integer", "minimum": 0}, "rows": {"type": "array"}, "code": INT, "msg": STR},
)

LOGIN_SCHEMA = _obj(["code", "msg"], {"code": INT, "msg": STR, "token": STR})

GETINFO_SCHEMA = _obj(
    ["code", "msg", "user", "roles", "permissions"],
    {"code": INT, "msg": STR, "user": {"type": "object"}, "roles": {"type": "array"},
     "permissions": {"type": "array"}},
)

TREE_SCHEMA = _obj(["code", "msg", "data"], {"code": INT, "msg": STR, "data": {"type": "array"}})

# ---------- 各模块列表行 ----------
USER_ROW = _obj(["userId", "userName", "nickName", "status"],
                {"userId": INT, "userName": STR, "nickName": STR, "status": STR, "deptId": {"type": ["integer", "null"]}})
ROLE_ROW = _obj(["roleId", "roleName", "roleKey", "roleSort", "status"],
                {"roleId": INT, "roleName": STR, "roleKey": STR, "roleSort": INT, "status": STR})
MENU_ROW = _obj(["menuId", "menuName", "parentId", "orderNum", "menuType", "visible", "status"],
                {"menuId": INT, "menuName": STR, "parentId": INT, "orderNum": INT,
                 "menuType": STR, "visible": STR, "status": STR, "path": {"type": ["string", "null"]}})
DEPT_ROW = _obj(["deptId", "parentId", "deptName", "orderNum", "status"],
                {"deptId": INT, "parentId": INT, "deptName": STR, "orderNum": INT, "status": STR})
POST_ROW = _obj(["postId", "postCode", "postName", "postSort", "status"],
                {"postId": INT, "postCode": STR, "postName": STR, "postSort": INT, "status": STR})
DICT_TYPE_ROW = _obj(["dictId", "dictName", "dictType", "status"],
                     {"dictId": INT, "dictName": STR, "dictType": STR, "status": STR})
DICT_DATA_ROW = _obj(["dictCode", "dictLabel", "dictValue", "dictSort", "dictType", "status"],
                     {"dictCode": INT, "dictLabel": STR, "dictValue": STR, "dictSort": INT,
                      "dictType": STR, "status": STR})
CONFIG_ROW = _obj(["configId", "configName", "configKey", "configValue"],
                  {"configId": INT, "configName": STR, "configKey": STR, "configValue": STR})
NOTICE_ROW = _obj(["noticeId", "noticeTitle", "noticeType", "status"],
                  {"noticeId": INT, "noticeTitle": STR, "noticeType": STR, "status": STR})
JOB_ROW = _obj(["jobId", "jobName", "jobGroup", "invokeTarget", "cronExpression", "status"],
               {"jobId": INT, "jobName": STR, "jobGroup": STR, "invokeTarget": STR,
                "cronExpression": STR, "status": STR})
JOBLOG_ROW = _obj(["jobLogId", "jobName", "jobGroup", "jobMessage", "status"],
                  {"jobLogId": INT, "jobName": STR, "jobGroup": STR, "jobMessage": STR, "status": STR})
LOGININFOR_ROW = _obj(["infoId", "userName", "ipaddr", "status"],
                      {"infoId": INT, "userName": STR, "ipaddr": STR, "status": STR})
OPERLOG_ROW = _obj(["operId", "title", "businessType", "operName", "status"],
                   {"operId": INT, "title": STR, "businessType": INT, "operName": STR, "status": INT})
ONLINE_ROW = _obj(["tokenId", "userName", "ipaddr", "browser", "os"],
                  {"tokenId": STR, "userName": STR, "ipaddr": STR, "browser": STR, "os": STR})
GEN_TABLE_ROW = _obj(["tableId", "tableName", "className"],
                     {"tableId": INT, "tableName": STR, "tableComment": {"type": ["string", "null"]},
                      "className": STR, "tplCategory": {"type": ["string", "null"]}})
UPLOAD_SCHEMA = _obj(["code", "msg", "fileName", "url"],
                     {"code": INT, "msg": STR, "fileName": STR, "url": STR,
                      "newFileName": STR, "originalFilename": STR})
SERVER_SCHEMA = _obj(["code", "msg", "data"], {"code": INT, "msg": STR, "data": {"type": "object"}})
CACHE_SCHEMA = _obj(["code", "msg", "data"], {"code": INT, "msg": STR, "data": {}})


def _table(row_schema):
    """由行结构生成列表返回结构"""
    return _obj(["total", "rows", "code", "msg"],
                {"total": {"type": "integer", "minimum": 0}, "rows": {"type": "array", "items": row_schema},
                 "code": INT, "msg": STR})


# =============================================================
#  三、端点注册表
#     (HTTP 方法, 路径模板, 响应 Schema, 说明)
# =============================================================
REGISTRATIONS = [
    # ---------- 登录认证 ----------
    ("GET", "/captchaImage", AJAX_SCHEMA, "获取验证码"),
    ("POST", "/login", LOGIN_SCHEMA, "用户登录"),
    ("GET", "/getInfo", GETINFO_SCHEMA, "获取当前用户信息"),
    ("GET", "/getRouters", TREE_SCHEMA, "获取路由菜单"),
    ("POST", "/register", AJAX_SCHEMA, "用户注册"),
    ("POST", "/unlockscreen", AJAX_SCHEMA, "解锁屏幕"),
    # ---------- 用户 ----------
    ("GET", "/system/user/list", _table(USER_ROW), "用户列表"),
    ("GET", "/system/user/{id}", AJAX_SCHEMA, "用户详情"),
    ("POST", "/system/user", AJAX_SCHEMA, "新增用户"),
    ("PUT", "/system/user", AJAX_SCHEMA, "修改用户"),
    ("DELETE", "/system/user/{ids}", AJAX_SCHEMA, "删除用户"),
    ("PUT", "/system/user/resetPwd", AJAX_SCHEMA, "重置密码"),
    ("PUT", "/system/user/changeStatus", AJAX_SCHEMA, "修改用户状态"),
    ("GET", "/system/user/authRole/{id}", AJAX_SCHEMA, "查询用户已分配角色"),
    ("GET", "/system/user/deptTree", TREE_SCHEMA, "部门树"),
    # ---------- 角色 ----------
    ("GET", "/system/role/list", _table(ROLE_ROW), "角色列表"),
    ("GET", "/system/role/{id}", AJAX_SCHEMA, "角色详情"),
    ("POST", "/system/role", AJAX_SCHEMA, "新增角色"),
    ("PUT", "/system/role", AJAX_SCHEMA, "修改角色"),
    ("DELETE", "/system/role/{ids}", AJAX_SCHEMA, "删除角色"),
    ("GET", "/system/role/optionselect", AJAX_SCHEMA, "角色下拉选项"),
    ("GET", "/system/role/authUser/allocatedList", _table(USER_ROW), "已分配用户"),
    # ---------- 菜单 ----------
    ("GET", "/system/menu/list", AJAX_SCHEMA, "菜单列表"),
    ("GET", "/system/menu/{id}", AJAX_SCHEMA, "菜单详情"),
    ("GET", "/system/menu/treeselect", TREE_SCHEMA, "菜单下拉树"),
    ("POST", "/system/menu", AJAX_SCHEMA, "新增菜单"),
    ("PUT", "/system/menu", AJAX_SCHEMA, "修改菜单"),
    ("DELETE", "/system/menu/{id}", AJAX_SCHEMA, "删除菜单"),
    # ---------- 部门 ----------
    ("GET", "/system/dept/list", AJAX_SCHEMA, "部门列表"),
    ("GET", "/system/dept/{id}", AJAX_SCHEMA, "部门详情"),
    ("POST", "/system/dept", AJAX_SCHEMA, "新增部门"),
    ("PUT", "/system/dept", AJAX_SCHEMA, "修改部门"),
    ("DELETE", "/system/dept/{id}", AJAX_SCHEMA, "删除部门"),
    # ---------- 岗位 ----------
    ("GET", "/system/post/list", _table(POST_ROW), "岗位列表"),
    ("POST", "/system/post", AJAX_SCHEMA, "新增岗位"),
    ("PUT", "/system/post", AJAX_SCHEMA, "修改岗位"),
    ("DELETE", "/system/post/{ids}", AJAX_SCHEMA, "删除岗位"),
    # ---------- 字典 ----------
    ("GET", "/system/dict/type/list", _table(DICT_TYPE_ROW), "字典类型列表"),
    ("POST", "/system/dict/type", AJAX_SCHEMA, "新增字典类型"),
    ("PUT", "/system/dict/type", AJAX_SCHEMA, "修改字典类型"),
    ("DELETE", "/system/dict/type/{ids}", AJAX_SCHEMA, "删除字典类型"),
    ("GET", "/system/dict/data/list", _table(DICT_DATA_ROW), "字典数据列表"),
    ("GET", "/system/dict/data/type/{dictType}", AJAX_SCHEMA, "按类型查字典数据"),
    ("POST", "/system/dict/data", AJAX_SCHEMA, "新增字典数据"),
    ("PUT", "/system/dict/data", AJAX_SCHEMA, "修改字典数据"),
    ("DELETE", "/system/dict/data/{ids}", AJAX_SCHEMA, "删除字典数据"),
    # ---------- 参数配置 ----------
    ("GET", "/system/config/list", _table(CONFIG_ROW), "参数列表"),
    ("GET", "/system/config/{id}", AJAX_SCHEMA, "参数详情"),
    ("GET", "/system/config/configKey/{key}", AJAX_SCHEMA, "按键名查参数值"),
    ("POST", "/system/config", AJAX_SCHEMA, "新增参数"),
    ("PUT", "/system/config", AJAX_SCHEMA, "修改参数"),
    ("DELETE", "/system/config/{ids}", AJAX_SCHEMA, "删除参数"),
    # ---------- 通知公告 ----------
    ("GET", "/system/notice/list", _table(NOTICE_ROW), "公告列表"),
    ("GET", "/system/notice/{id}", AJAX_SCHEMA, "公告详情"),
    ("POST", "/system/notice", AJAX_SCHEMA, "新增公告"),
    ("PUT", "/system/notice", AJAX_SCHEMA, "修改公告"),
    ("DELETE", "/system/notice/{ids}", AJAX_SCHEMA, "删除公告"),
    ("GET", "/system/notice/listTop", AJAX_SCHEMA, "最新公告"),
    # ---------- 个人信息 ----------
    ("GET", "/system/user/profile", AJAX_SCHEMA, "个人信息"),
    ("PUT", "/system/user/profile", AJAX_SCHEMA, "修改个人信息"),
    ("PUT", "/system/user/profile/updatePwd", AJAX_SCHEMA, "修改密码"),
    # ---------- 监控 ----------
    ("GET", "/monitor/online/list", _table(ONLINE_ROW), "在线用户"),
    ("GET", "/monitor/job/list", _table(JOB_ROW), "定时任务列表"),
    ("POST", "/monitor/job", AJAX_SCHEMA, "新增定时任务"),
    ("PUT", "/monitor/job", AJAX_SCHEMA, "修改定时任务"),
    ("PUT", "/monitor/job/changeStatus", AJAX_SCHEMA, "任务状态变更"),
    ("DELETE", "/monitor/job/{ids}", AJAX_SCHEMA, "删除定时任务"),
    ("GET", "/monitor/jobLog/list", _table(JOBLOG_ROW), "调度日志"),
    ("GET", "/monitor/logininfor/list", _table(LOGININFOR_ROW), "登录日志"),
    ("GET", "/monitor/operlog/list", _table(OPERLOG_ROW), "操作日志"),
    ("GET", "/monitor/cache", AJAX_SCHEMA, "缓存信息"),
    ("GET", "/monitor/cache/getNames", AJAX_SCHEMA, "缓存名称列表"),
    ("GET", "/monitor/server", SERVER_SCHEMA, "服务监控"),
    # ---------- 代码生成 ----------
    ("GET", "/tool/gen/list", _table(GEN_TABLE_ROW), "代码生成列表"),
    ("GET", "/tool/gen/db/list", _table(GEN_TABLE_ROW), "数据库表列表"),
    # ---------- 通用 ----------
    ("POST", "/common/upload", UPLOAD_SCHEMA, "文件上传"),
]

def register_ruoyi_contracts():
    """把 RuoYi-Vue 的端点契约注册到框架契约中心

    同一 (method, pattern) 只注册一次：重复注册会让契约中心出现
    多条同端点记录，掩盖真实的结构覆盖缺口。
    """
    from api_automation.framework.contract import registry

    registered = set()
    count = 0
    for method, path, schema, desc in REGISTRATIONS:
        key = (method.upper(), path)
        if key in registered:
            continue
        registered.add(key)
        registry.register(method, path, response_schema=schema, description=f"RuoYi {desc}")
        count += 1
    return count


__all__ = [
    "LoginRequest", "UserCreateRequest", "RoleCreateRequest", "DeptCreateRequest",
    "PostCreateRequest", "DictTypeCreateRequest", "DictDataCreateRequest", "ConfigCreateRequest",
    "NoticeCreateRequest", "JobCreateRequest",
    "AJAX_SCHEMA", "TABLE_SCHEMA", "LOGIN_SCHEMA", "GETINFO_SCHEMA", "TREE_SCHEMA",
    "USER_ROW", "ROLE_ROW", "MENU_ROW", "DEPT_ROW", "POST_ROW", "DICT_TYPE_ROW",
    "DICT_DATA_ROW", "CONFIG_ROW", "NOTICE_ROW", "JOB_ROW", "JOBLOG_ROW",
    "LOGININFOR_ROW", "OPERLOG_ROW", "ONLINE_ROW", "GEN_TABLE_ROW", "UPLOAD_SCHEMA",
    "REGISTRATIONS", "register_ruoyi_contracts",
]
