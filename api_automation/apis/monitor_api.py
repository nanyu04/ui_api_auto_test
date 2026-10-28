"""
【接口层】— 系统监控模块（RuoYi-Vue）

对应接口文档 4.3.1 ~ 4.3.32：在线用户 / 定时任务 / 调度日志 /
缓存监控 / 服务监控 / 登录日志 / 操作日志。
"""
from typing import Optional

from api_automation.common import BaseApi


class OnlineApi(BaseApi):
    """在线用户接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询在线用户列表 GET /monitor/online/list"""
        return self.get("/monitor/online/list", params=params)

    def force_logout(self, token_id):
        """强制退出用户 DELETE /monitor/online/{tokenId}"""
        return self.delete(f"/monitor/online/{token_id}")


class JobApi(BaseApi):
    """定时任务接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询定时任务列表 GET /monitor/job/list"""
        return self.get("/monitor/job/list", params=params)

    def detail(self, job_id):
        """查询定时任务详细 GET /monitor/job/{jobId}"""
        return self.get(f"/monitor/job/{job_id}")

    def create(self, body: dict):
        """新增定时任务 POST /monitor/job"""
        return self.post("/monitor/job", json=body)

    def update(self, body: dict):
        """修改定时任务 PUT /monitor/job"""
        return self.put("/monitor/job", json=body)

    def change_status(self, body: dict):
        """修改任务状态 PUT /monitor/job/changeStatus"""
        return self.put("/monitor/job/changeStatus", json=body)

    def run(self, body: dict):
        """立即执行一次任务 PUT /monitor/job/run"""
        return self.put("/monitor/job/run", json=body)

    def remove(self, job_ids):
        """删除定时任务 DELETE /monitor/job/{jobIds}"""
        return self.delete(f"/monitor/job/{job_ids}")

    def export(self, params: Optional[dict] = None):
        """导出定时任务 POST /monitor/job/export"""
        return self.post("/monitor/job/export", data=params or {})


class JobLogApi(BaseApi):
    """调度日志接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询调度日志列表 GET /monitor/jobLog/list"""
        return self.get("/monitor/jobLog/list", params=params)

    def detail(self, job_log_id):
        """查询调度日志详细 GET /monitor/jobLog/{jobLogId}"""
        return self.get(f"/monitor/jobLog/{job_log_id}")

    def remove(self, job_log_ids):
        """删除调度日志 DELETE /monitor/jobLog/{jobLogIds}"""
        return self.delete(f"/monitor/jobLog/{job_log_ids}")

    def clean(self):
        """清空调度日志 DELETE /monitor/jobLog/clean"""
        return self.delete("/monitor/jobLog/clean")

    def export(self, params: Optional[dict] = None):
        """导出调度日志 POST /monitor/jobLog/export"""
        return self.post("/monitor/jobLog/export", data=params or {})


class CacheApi(BaseApi):
    """缓存监控接口"""

    service_path = ""

    def info(self):
        """获取缓存监控信息 GET /monitor/cache"""
        return self.get("/monitor/cache")

    def names(self):
        """获取缓存名称列表 GET /monitor/cache/getNames"""
        return self.get("/monitor/cache/getNames")

    def keys(self, cache_name):
        """获取缓存键名列表 GET /monitor/cache/getKeys/{cacheName}"""
        return self.get(f"/monitor/cache/getKeys/{cache_name}")

    def value(self, cache_name, cache_key):
        """获取缓存内容 GET /monitor/cache/getValue/{cacheName}/{cacheKey}"""
        return self.get(f"/monitor/cache/getValue/{cache_name}/{cache_key}")

    def clear_name(self, cache_name):
        """清理缓存名称 DELETE /monitor/cache/clearCacheName/{cacheName}"""
        return self.delete(f"/monitor/cache/clearCacheName/{cache_name}")

    def clear_key(self, cache_key):
        """清理缓存键名 DELETE /monitor/cache/clearCacheKey/{cacheKey}"""
        return self.delete(f"/monitor/cache/clearCacheKey/{cache_key}")

    def clear_all(self):
        """清理全部缓存 DELETE /monitor/cache/clearCacheAll"""
        return self.delete("/monitor/cache/clearCacheAll")


class ServerApi(BaseApi):
    """服务监控接口"""

    service_path = ""

    def info(self):
        """获取服务器监控信息 GET /monitor/server"""
        return self.get("/monitor/server")


class LoginInfoApi(BaseApi):
    """登录日志接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询登录日志列表 GET /monitor/logininfor/list"""
        return self.get("/monitor/logininfor/list", params=params)

    def remove(self, info_ids):
        """删除登录日志 DELETE /monitor/logininfor/{infoIds}"""
        return self.delete(f"/monitor/logininfor/{info_ids}")

    def clean(self):
        """清空登录日志 DELETE /monitor/logininfor/clean"""
        return self.delete("/monitor/logininfor/clean")

    def unlock(self, user_name):
        """解锁用户登录 GET /monitor/logininfor/unlock/{userName}"""
        return self.get(f"/monitor/logininfor/unlock/{user_name}")

    def export(self, params: Optional[dict] = None):
        """导出登录日志 POST /monitor/logininfor/export"""
        return self.post("/monitor/logininfor/export", data=params or {})


class OperLogApi(BaseApi):
    """操作日志接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询操作日志列表 GET /monitor/operlog/list"""
        return self.get("/monitor/operlog/list", params=params)

    def remove(self, oper_ids):
        """删除操作日志 DELETE /monitor/operlog/{operIds}"""
        return self.delete(f"/monitor/operlog/{oper_ids}")

    def clean(self):
        """清空操作日志 DELETE /monitor/operlog/clean"""
        return self.delete("/monitor/operlog/clean")

    def export(self, params: Optional[dict] = None):
        """导出操作日志 POST /monitor/operlog/export"""
        return self.post("/monitor/operlog/export", data=params or {})


online_api = OnlineApi()
job_api = JobApi()
job_log_api = JobLogApi()
cache_api = CacheApi()
server_api = ServerApi()
login_info_api = LoginInfoApi()
oper_log_api = OperLogApi()