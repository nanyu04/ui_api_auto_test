"""
【接口层】— 角色管理模块（RuoYi-Vue）

对应接口文档 4.2.14 ~ 4.2.28。
方法名避开 get/post/put/delete，防止覆盖 BaseApi 的同名方法。
"""
from typing import Optional

from api_automation.common import BaseApi


class RoleApi(BaseApi):
    """角色管理接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询角色列表 GET /system/role/list"""
        return self.get("/system/role/list", params=params)

    def detail(self, role_id):
        """查询角色详细 GET /system/role/{roleId}"""
        return self.get(f"/system/role/{role_id}")

    def create(self, body: dict):
        """新增角色 POST /system/role"""
        return self.post("/system/role", json=body)

    def update(self, body: dict):
        """修改角色 PUT /system/role"""
        return self.put("/system/role", json=body)

    def remove(self, role_ids):
        """删除角色 DELETE /system/role/{roleIds}"""
        return self.delete(f"/system/role/{role_ids}")

    def data_scope(self, body: dict):
        """修改角色数据权限 PUT /system/role/dataScope"""
        return self.put("/system/role/dataScope", json=body)

    def change_status(self, body: dict):
        """修改角色状态 PUT /system/role/changeStatus"""
        return self.put("/system/role/changeStatus", json=body)

    def option_select(self):
        """获取角色下拉选项 GET /system/role/optionselect"""
        return self.get("/system/role/optionselect")

    # ---------- 角色授权用户 ----------

    def allocated_list(self, params: Optional[dict] = None):
        """查询已分配用户 GET /system/role/authUser/allocatedList"""
        return self.get("/system/role/authUser/allocatedList", params=params)

    def unallocated_list(self, params: Optional[dict] = None):
        """查询未分配用户 GET /system/role/authUser/unallocatedList"""
        return self.get("/system/role/authUser/unallocatedList", params=params)

    def cancel_auth(self, body: dict):
        """取消用户授权 PUT /system/role/authUser/cancel"""
        return self.put("/system/role/authUser/cancel", json=body)

    def cancel_auth_all(self, body: dict):
        """批量取消用户授权 PUT /system/role/authUser/cancelAll"""
        return self.put("/system/role/authUser/cancelAll", json=body)

    def select_auth_all(self, body: dict):
        """批量授权用户 PUT /system/role/authUser/selectAll"""
        return self.put("/system/role/authUser/selectAll", json=body)

    def dept_tree(self, role_id):
        """获取角色关联部门树 GET /system/role/deptTree/{roleId}"""
        return self.get(f"/system/role/deptTree/{role_id}")

    def export(self, params: Optional[dict] = None):
        """导出角色 POST /system/role/export"""
        return self.post("/system/role/export", data=params or {})


role_api = RoleApi()