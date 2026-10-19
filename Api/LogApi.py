from base_Api.base import Api_common


class LogApi(Api_common):
    """日志管理API"""

    def login_log_list(self, params=None):
        """查询登录日志列表"""
        url = "/dev-api/monitor/logininfor/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def delete_login_log(self, info_ids):
        """删除登录日志"""
        url = f"/dev-api/monitor/logininfor/{info_ids}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def clean_login_log(self):
        """清空登录日志"""
        url = "/dev-api/monitor/logininfor/clean"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def oper_log_list(self, params=None):
        """查询操作日志列表"""
        url = "/dev-api/monitor/operlog/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def delete_oper_log(self, oper_ids):
        """删除操作日志"""
        url = f"/dev-api/monitor/operlog/{oper_ids}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def clean_oper_log(self):
        """清空操作日志"""
        url = "/dev-api/monitor/operlog/clean"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp