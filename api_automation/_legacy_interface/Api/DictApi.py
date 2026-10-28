from api_automation._legacy_interface.base_Api.base import Api_common


class DictApi(Api_common):
    """字典管理API"""

    def list_dict_type(self, params=None):
        """查询字典类型列表"""
        url = "/dev-api/system/dict/type/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def get_dict_type(self, dict_id):
        """查询字典类型详情"""
        url = f"/dev-api/system/dict/type/{dict_id}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def add_dict_type(self, body=None):
        """新增字典类型"""
        url = "/dev-api/system/dict/type"
        resp = self.send_post(url=url, Json_date=body, headers=self.headers)
        return resp

    def edit_dict_type(self, body=None):
        """修改字典类型"""
        url = "/dev-api/system/dict/type"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def delete_dict_type(self, dict_ids):
        """删除字典类型"""
        url = f"/dev-api/system/dict/type/{dict_ids}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def list_dict_data(self, params=None):
        """查询字典数据列表"""
        url = "/dev-api/system/dict/data/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def get_dict_data(self, dict_code):
        """根据字典类型查询字典数据"""
        url = f"/dev-api/system/dict/data/type/{dict_code}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def add_dict_data(self, body=None):
        """新增字典数据"""
        url = "/dev-api/system/dict/data"
        resp = self.send_post(url=url, Json_date=body, headers=self.headers)
        return resp

    def edit_dict_data(self, body=None):
        """修改字典数据"""
        url = "/dev-api/system/dict/data"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def delete_dict_data(self, dict_codes):
        """删除字典数据"""
        url = f"/dev-api/system/dict/data/{dict_codes}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp