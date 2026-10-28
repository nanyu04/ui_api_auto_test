from api_automation._legacy_interface.base_Api.base import Api_common


class MenuApi(Api_common):
    """菜单管理API"""

    def list_menu(self, params=None):
        """查询菜单列表"""
        url = "/dev-api/system/menu/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def treeselect(self):
        """查询菜单树下拉结构"""
        url = "/dev-api/system/menu/treeselect"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def get_menu(self, menu_id):
        """根据ID查询菜单详情"""
        url = f"/dev-api/system/menu/{menu_id}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def add_menu(self, body=None):
        """新增菜单"""
        url = "/dev-api/system/menu"
        resp = self.send_post(url=url, Json_date=body, headers=self.headers)
        return resp

    def edit_menu(self, body=None):
        """修改菜单"""
        url = "/dev-api/system/menu"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def delete_menu(self, menu_id):
        """删除菜单"""
        url = f"/dev-api/system/menu/{menu_id}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def role_menu_treeselect(self, role_id):
        """根据角色ID查询菜单树"""
        url = f"/dev-api/system/menu/roleMenuTreeselect/{role_id}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp