"""
【接口层】— 菜单管理模块（RuoYi-Vue）

对应接口文档 4.2.29 ~ 4.2.36。
"""
from typing import Optional

from api_automation.common import BaseApi


class MenuApi(BaseApi):
    """菜单管理接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询菜单列表 GET /system/menu/list（返回树形 data）"""
        return self.get("/system/menu/list", params=params)

    def detail(self, menu_id):
        """查询菜单详细 GET /system/menu/{menuId}"""
        return self.get(f"/system/menu/{menu_id}")

    def treeselect(self):
        """获取菜单下拉树 GET /system/menu/treeselect"""
        return self.get("/system/menu/treeselect")

    def role_menu_treeselect(self, role_id):
        """获取角色菜单树 GET /system/menu/roleMenuTreeselect/{roleId}"""
        return self.get(f"/system/menu/roleMenuTreeselect/{role_id}")

    def create(self, body: dict):
        """新增菜单 POST /system/menu"""
        return self.post("/system/menu", json=body)

    def update(self, body: dict):
        """修改菜单 PUT /system/menu"""
        return self.put("/system/menu", json=body)

    def update_sort(self, body: dict):
        """保存菜单排序 PUT /system/menu/updateSort"""
        return self.put("/system/menu/updateSort", json=body)

    def remove(self, menu_id):
        """删除菜单 DELETE /system/menu/{menuId}

        若依的菜单删除只接受单个 menuId，不支持逗号批量。
        """
        return self.delete(f"/system/menu/{menu_id}")


menu_api = MenuApi()