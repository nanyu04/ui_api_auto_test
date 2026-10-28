"""
【接口层】— 鉴权 / 会话模块（RuoYi-Vue）

对应接口文档 4.1：登录认证与注册。
路径一律使用后端裸路径（不带前端 dev-server 的 /dev-api 前缀）。
"""
from typing import Optional

from api_automation.common import BaseApi


class AuthApi(BaseApi):
    """鉴权接口"""

    service_path = ""

    def login(self, username: str, password: str,
              code: str = "", uuid: str = "") -> "Response":
        """用户登录 POST /login（成功返回 token）"""
        body = {"username": username, "password": password}
        if code:
            body["code"] = code
        if uuid:
            body["uuid"] = uuid
        return self.post("/login", json=body)

    def captcha(self):
        """获取验证码 GET /captchaImage（返回 uuid + base64 图片）"""
        return self.get("/captchaImage")

    def get_info(self):
        """获取当前登录用户信息 GET /getInfo（含 roles / permissions）"""
        return self.get("/getInfo")

    def get_routers(self):
        """获取当前用户路由菜单 GET /getRouters"""
        return self.get("/getRouters")

    def logout(self):
        """退出登录 POST /logout"""
        return self.post("/logout")

    def register(self, body: dict):
        """用户注册 POST /register"""
        return self.post("/register", json=body)

    def unlock_screen(self, password: str):
        """解锁屏幕 POST /unlockscreen"""
        return self.post("/unlockscreen", json={"password": password})

    def index(self):
        """系统首页 GET /"""
        return self.get("/")


auth_api = AuthApi()