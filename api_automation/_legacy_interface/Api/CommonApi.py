from api_automation._legacy_interface.base_Api.base import Api_common


class CommonApi(Api_common):
    """系统通用API"""

    def login(self, username, password, code=None, uuid=None):
        """登录接口"""
        url = "/dev-api/login"
        body = {
            "username": username,
            "password": password
        }
        if code is not None:
            body["code"] = code
        if uuid is not None:
            body["uuid"] = uuid
        resp = self.send_post(url=url, Json_date=body, headers=self.headers)
        return resp

    def get_captcha(self):
        """获取验证码"""
        url = "/dev-api/captchaImage"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def get_info(self):
        """获取当前用户信息"""
        url = "/dev-api/getInfo"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def get_routers(self):
        """获取路由信息"""
        url = "/dev-api/getRouters"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def user_list(self, params=None):
        """查询用户列表"""
        url = "/dev-api/system/user/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def get_user(self, user_id=None):
        """查询用户详情"""
        url = f"/dev-api/system/user/{user_id or ''}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def add_user(self, body=None):
        """新增用户"""
        url = "/dev-api/system/user"
        resp = self.send_post(url=url, Json_date=body, headers=self.headers)
        return resp

    def edit_user(self, body=None):
        """修改用户"""
        url = "/dev-api/system/user"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def delete_user(self, user_ids):
        """删除用户"""
        url = f"/dev-api/system/user/{user_ids}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def reset_user_pwd(self, body=None):
        """重置用户密码"""
        url = "/dev-api/system/user/resetPwd"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def change_user_status(self, body=None):
        """修改用户状态"""
        url = "/dev-api/system/user/changeStatus"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def dept_list(self, params=None):
        """查询部门列表"""
        url = "/dev-api/system/dept/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def dept_treeselect(self):
        """查询部门树"""
        url = "/dev-api/system/dept/treeselect"
        resp = self.send_get(url=url, headers=self.headers)
        return resp