from api_automation._legacy_interface.base_Api.base import Api_common


class DeptApi(Api_common):
    def dept_api(self,params=None):
        url="/dev-api/system/dept/list"
        resp=self.send_get(url=url,params=params,headers=self.headers)
        return resp
