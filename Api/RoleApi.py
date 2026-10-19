from base_Api.base import Api_common


class RoleApi(Api_common):
    """角色管理API"""

    def list_role(self, params=None):
        """查询角色列表"""
        url = "/dev-api/system/role/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def get_role(self, role_id):
        """根据ID查询角色详情"""
        url = f"/dev-api/system/role/{role_id}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def add_role(self, body=None):
        """新增角色"""
        url = "/dev-api/system/role"
        resp = self.send_post(url=url, Json_date=body, headers=self.headers)
        return resp

    def edit_role(self, body=None):
        """修改角色"""
        url = "/dev-api/system/role"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def delete_role(self, role_ids):
        """删除角色"""
        url = f"/dev-api/system/role/{role_ids}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def change_role_status(self, body=None):
        """修改角色状态"""
        url = "/dev-api/system/role/changeStatus"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def allocated_list(self, params=None):
        """查询角色已授权用户列表"""
        url = "/dev-api/system/role/authUser/allocatedList"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def unallocated_list(self, params=None):
        """查询角色未授权用户列表"""
        url = "/dev-api/system/role/authUser/unallocatedList"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp