"""
【接口层】— 用户管理模块（RuoYi-Vue）

对应接口文档 4.2.1 ~ 4.2.13。
"""
from typing import Optional

from api_automation.common import BaseApi


class UserApi(BaseApi):
    """用户管理接口"""

    service_path = ""

    # ---------- 查询 ----------

    def list(self, params: Optional[dict] = None):
        """查询用户列表 GET /system/user/list"""
        return self.get("/system/user/list", params=params)

    def detail(self, user_id):
        """查询用户详细 GET /system/user/{userId}"""
        return self.get(f"/system/user/{user_id}")

    def dept_tree(self, params: Optional[dict] = None):
        """获取部门树数据 GET /system/user/deptTree"""
        return self.get("/system/user/deptTree", params=params)

    # ---------- 增删改 ----------

    def create(self, body: dict):
        """新增用户 POST /system/user"""
        return self.post("/system/user", json=body)

    def update(self, body: dict):
        """修改用户 PUT /system/user"""
        return self.put("/system/user", json=body)

    def remove(self, user_ids):
        """删除用户 DELETE /system/user/{userIds}（多个用逗号分隔）

        注意：方法名不能叫 delete，否则会覆盖 BaseApi.delete 造成无限递归。
        """
        return self.delete(f"/system/user/{user_ids}")

    # ---------- 状态 / 密码 ----------

    def reset_pwd(self, body: dict):
        """重置用户密码 PUT /system/user/resetPwd"""
        return self.put("/system/user/resetPwd", json=body)

    def change_status(self, body: dict):
        """修改用户状态 PUT /system/user/changeStatus"""
        return self.put("/system/user/changeStatus", json=body)

    # ---------- 角色分配 ----------

    def auth_role(self, user_id):
        """查询用户已分配角色 GET /system/user/authRole/{userId}"""
        return self.get(f"/system/user/authRole/{user_id}")

    def insert_auth_role(self, body: dict):
        """给用户分配角色 PUT /system/user/authRole"""
        return self.put("/system/user/authRole", json=body)

    # ---------- 导入导出 ----------

    def export(self, params: Optional[dict] = None):
        """导出用户 POST /system/user/export（返回二进制流）"""
        return self.post("/system/user/export", data=params or {})

    def import_template(self):
        """下载用户导入模板 POST /system/user/importTemplate"""
        return self.post("/system/user/importTemplate")

    def import_data(self, files: dict, params: Optional[dict] = None):
        """导入用户数据 POST /system/user/importData"""
        return self.post("/system/user/importData", files=files, params=params)


user_api = UserApi()