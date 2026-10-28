from api_automation._legacy_interface.base_Api.base import Api_common


class PostApi(Api_common):
    """岗位管理API"""

    def list_post(self, params=None):
        """查询岗位列表"""
        url = "/dev-api/system/post/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def get_post(self, post_id):
        """根据ID查询岗位详情"""
        url = f"/dev-api/system/post/{post_id}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def add_post(self, body=None):
        """新增岗位"""
        url = "/dev-api/system/post"
        resp = self.send_post(url=url, Json_date=body, headers=self.headers)
        return resp

    def edit_post(self, body=None):
        """修改岗位"""
        url = "/dev-api/system/post"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def delete_post(self, post_ids):
        """删除岗位"""
        url = f"/dev-api/system/post/{post_ids}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp