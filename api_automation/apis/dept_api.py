"""
【接口层】— 部门管理模块（RuoYi-Vue）

对应接口文档 4.2.37 ~ 4.2.43。
"""
from typing import Optional

from api_automation.common import BaseApi


class DeptApi(BaseApi):
    """部门管理接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询部门列表 GET /system/dept/list（返回树形 data）"""
        return self.get("/system/dept/list", params=params)

    def list_exclude(self, dept_id):
        """查询部门列表（排除指定节点） GET /system/dept/list/exclude/{deptId}"""
        return self.get(f"/system/dept/list/exclude/{dept_id}")

    def detail(self, dept_id):
        """查询部门详细 GET /system/dept/{deptId}"""
        return self.get(f"/system/dept/{dept_id}")

    def create(self, body: dict):
        """新增部门 POST /system/dept"""
        return self.post("/system/dept", json=body)

    def update(self, body: dict):
        """修改部门 PUT /system/dept"""
        return self.put("/system/dept", json=body)

    def update_sort(self, body: dict):
        """保存部门排序 PUT /system/dept/updateSort"""
        return self.put("/system/dept/updateSort", json=body)

    def remove(self, dept_id):
        """删除部门 DELETE /system/dept/{deptId}"""
        return self.delete(f"/system/dept/{dept_id}")


dept_api = DeptApi()