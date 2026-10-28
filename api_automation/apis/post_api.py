"""
【接口层】— 岗位管理模块（RuoYi-Vue）

对应接口文档 4.2.44 ~ 4.2.50。
"""
from typing import Optional

from api_automation.common import BaseApi


class PostApi(BaseApi):
    """岗位管理接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询岗位列表 GET /system/post/list"""
        return self.get("/system/post/list", params=params)

    def detail(self, post_id):
        """查询岗位详细 GET /system/post/{postId}"""
        return self.get(f"/system/post/{post_id}")

    def create(self, body: dict):
        """新增岗位 POST /system/post"""
        return self.post("/system/post", json=body)

    def update(self, body: dict):
        """修改岗位 PUT /system/post"""
        return self.put("/system/post", json=body)

    def remove(self, post_ids):
        """删除岗位 DELETE /system/post/{postIds}"""
        return self.delete(f"/system/post/{post_ids}")

    def option_select(self):
        """获取岗位下拉选项 GET /system/post/optionselect"""
        return self.get("/system/post/optionselect")

    def export(self, params: Optional[dict] = None):
        """导出岗位 POST /system/post/export"""
        return self.post("/system/post/export", data=params or {})


post_api = PostApi()