from api_automation._legacy_interface.base_Api.base import Api_common


class NoticeApi(Api_common):
    """通知公告API"""

    def list_notice(self, params=None):
        """查询通知公告列表"""
        url = "/dev-api/system/notice/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def get_notice(self, notice_id):
        """根据ID查询通知公告详情"""
        url = f"/dev-api/system/notice/{notice_id}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def add_notice(self, body=None):
        """新增通知公告"""
        url = "/dev-api/system/notice"
        resp = self.send_post(url=url, Json_date=body, headers=self.headers)
        return resp

    def edit_notice(self, body=None):
        """修改通知公告"""
        url = "/dev-api/system/notice"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def delete_notice(self, notice_ids):
        """删除通知公告"""
        url = f"/dev-api/system/notice/{notice_ids}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp