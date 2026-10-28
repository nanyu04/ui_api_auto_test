"""
【接口层】— 统一导出

约定：
  - 每个模块导出「类」+「单例」，用例层只使用单例；
  - ALL_API_SINGLETONS 供 conftest 把全部模块的 client 绑定到同一个
    session 级 HttpClient 上 —— 否则登录态只存在于某个模块自己的会话里，
    自动清理发出的请求不带鉴权头会静默失败。
"""
from api_automation.apis.auth_api import AuthApi, auth_api
from api_automation.apis.user_api import UserApi, user_api
from api_automation.apis.role_api import RoleApi, role_api
from api_automation.apis.menu_api import MenuApi, menu_api
from api_automation.apis.dept_api import DeptApi, dept_api
from api_automation.apis.post_api import PostApi, post_api
from api_automation.apis.dict_api import DictTypeApi, DictDataApi, dict_type_api, dict_data_api
from api_automation.apis.config_api import ConfigApi, config_api
from api_automation.apis.notice_api import NoticeApi, notice_api
from api_automation.apis.profile_api import ProfileApi, profile_api
from api_automation.apis.monitor_api import (
    OnlineApi, JobApi, JobLogApi, CacheApi, ServerApi, LoginInfoApi, OperLogApi,
    online_api, job_api, job_log_api, cache_api, server_api, login_info_api, oper_log_api,
)
from api_automation.apis.gen_api import GenApi, gen_api
from api_automation.apis.common_api import CommonApi, common_api

# 所有单例（conftest 用它统一绑定会话）
ALL_API_SINGLETONS = [
    auth_api, user_api, role_api, menu_api, dept_api, post_api,
    dict_type_api, dict_data_api, config_api, notice_api, profile_api,
    online_api, job_api, job_log_api, cache_api, server_api,
    login_info_api, oper_log_api, gen_api, common_api,
]

__all__ = [
    "AuthApi", "auth_api",
    "UserApi", "user_api",
    "RoleApi", "role_api",
    "MenuApi", "menu_api",
    "DeptApi", "dept_api",
    "PostApi", "post_api",
    "DictTypeApi", "DictDataApi", "dict_type_api", "dict_data_api",
    "ConfigApi", "config_api",
    "NoticeApi", "notice_api",
    "ProfileApi", "profile_api",
    "OnlineApi", "JobApi", "JobLogApi", "CacheApi", "ServerApi",
    "LoginInfoApi", "OperLogApi",
    "online_api", "job_api", "job_log_api", "cache_api", "server_api",
    "login_info_api", "oper_log_api",
    "GenApi", "gen_api",
    "CommonApi", "common_api",
    "ALL_API_SINGLETONS",
]