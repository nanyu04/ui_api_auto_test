"""
【接口层】— 通知公告模块（RuoYi-Vue）

对应接口文档 4.2.74 ~ 4.2.82。
"""
from typing import Optional

from api_automation.common import BaseApi


class NoticeApi(BaseApi):
    """通知公告接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询公告列表 GET /system/notice/list"""
        return self.get("/system/notice/list", params=params)

    def detail(self, notice_id):
        """查询公告详细 GET /system/notice/{noticeId}"""
        return self.get(f"/system/notice/{notice_id}")

    def create(self, body: dict):
        """新增公告 POST /system/notice"""
        return self.post("/system/notice", json=body)

    def update(self, body: dict):
        """修改公告 PUT /system/notice"""
        return self.put("/system/notice", json=body)

    def remove(self, notice_ids):
        """删除公告 DELETE /system/notice/{noticeIds}"""
        return self.delete(f"/system/notice/{notice_ids}")

    # ---------- 顶部通知 / 已读 ----------

    def list_top(self):
        """查询最新公告（顶部通知） GET /system/notice/listTop"""
        return self.get("/system/notice/listTop")

    def mark_read(self, notice_id):
        """标记公告已读 POST /system/notice/markRead"""
        return self.post("/system/notice/markRead", params={"noticeId": notice_id})

    def mark_read_all(self, ids: str):
        """全部标记已读 POST /system/notice/markReadAll（ids 多个用逗号分隔）"""
        return self.post("/system/notice/markReadAll", params={"ids": ids})

    def read_users(self, params: Optional[dict] = None):
        """查询公告已读用户 GET /system/notice/readUsers/list"""
        return self.get("/system/notice/readUsers/list", params=params)


notice_api = NoticeApi()