from api_automation._legacy_interface.base_Api.base import Api_common


class MonitorApi(Api_common):
    """监控管理API"""

    def server_info(self):
        """查询服务器信息"""
        url = "/dev-api/monitor/server"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def online_user_list(self, params=None):
        """查询在线用户列表"""
        url = "/dev-api/monitor/online/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def force_logout(self, token_id):
        """强退在线用户"""
        url = f"/dev-api/monitor/online/{token_id}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def job_list(self, params=None):
        """查询定时任务列表"""
        url = "/dev-api/monitor/job/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def get_job(self, job_id):
        """根据ID查询定时任务详情"""
        url = f"/dev-api/monitor/job/{job_id}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def add_job(self, body=None):
        """新增定时任务"""
        url = "/dev-api/monitor/job"
        resp = self.send_post(url=url, Json_date=body, headers=self.headers)
        return resp

    def edit_job(self, body=None):
        """修改定时任务"""
        url = "/dev-api/monitor/job"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def delete_job(self, job_ids):
        """删除定时任务"""
        url = f"/dev-api/monitor/job/{job_ids}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def change_job_status(self, body=None):
        """修改定时任务状态"""
        url = "/dev-api/monitor/job/changeStatus"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def run_job(self, body=None):
        """立即执行定时任务"""
        url = "/dev-api/monitor/job/run"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def cache_info(self):
        """查询缓存信息"""
        url = "/dev-api/monitor/cache"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def cache_names(self):
        """查询缓存名称列表"""
        url = "/dev-api/monitor/cache/getNames"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def cache_keys(self, cache_name):
        """查询缓存键名列表"""
        url = f"/dev-api/monitor/cache/getKeys/{cache_name}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def cache_value(self, cache_name, cache_key):
        """查询缓存内容"""
        url = f"/dev-api/monitor/cache/getValue/{cache_name}/{cache_key}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def clear_cache_name(self, cache_name):
        """清理指定名称缓存"""
        url = f"/dev-api/monitor/cache/clearCacheName/{cache_name}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def clear_cache_key(self, cache_key):
        """清理指定Key缓存"""
        url = f"/dev-api/monitor/cache/clearCacheKey/{cache_key}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def clear_all_cache(self):
        """清理全部缓存"""
        url = "/dev-api/monitor/cache/clearCacheAll"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp