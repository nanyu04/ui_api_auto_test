"""
【接口层】— 个人信息模块（RuoYi-Vue）

对应接口文档 4.2.83 ~ 4.2.86。
"""
from api_automation.common import BaseApi


class ProfileApi(BaseApi):
    """个人中心接口"""

    service_path = ""

    def profile(self):
        """查询个人信息 GET /system/user/profile"""
        return self.get("/system/user/profile")

    def update_profile(self, body: dict):
        """修改个人信息 PUT /system/user/profile"""
        return self.put("/system/user/profile", json=body)

    def update_pwd(self, old_password: str, new_password: str):
        """修改个人密码 PUT /system/user/profile/updatePwd（JSON 请求体）"""
        return self.put("/system/user/profile/updatePwd",
                        json={"oldPassword": old_password, "newPassword": new_password})

    def upload_avatar(self, files: dict):
        """上传个人头像 POST /system/user/profile/avatar（form-data: avatarfile）"""
        return self.post("/system/user/profile/avatar", files=files)


profile_api = ProfileApi()