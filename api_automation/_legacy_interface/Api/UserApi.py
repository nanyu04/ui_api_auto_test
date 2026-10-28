from api_automation._legacy_interface.base_Api.base import Api_common


class UserApi(Api_common):
    def login_user(self,username,password):
        url="/dev-api/login"
        body={
            "username":username,
            "password":password
        }
        request=self.send_post(url=url,Json_date=body)
        return request