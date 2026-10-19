from base_Api.base import Api_common


class ConfigApi(Api_common):
    """参数配置API"""

    def list_config(self, params=None):
        """查询参数配置列表"""
        url = "/dev-api/system/config/list"
        resp = self.send_get(url=url, params=params, headers=self.headers)
        return resp

    def get_config(self, config_id):
        """根据ID查询参数详情"""
        url = f"/dev-api/system/config/{config_id}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def get_config_by_key(self, config_key):
        """根据键名查询参数"""
        url = f"/dev-api/system/config/configKey/{config_key}"
        resp = self.send_get(url=url, headers=self.headers)
        return resp

    def add_config(self, body=None):
        """新增参数配置"""
        url = "/dev-api/system/config"
        resp = self.send_post(url=url, Json_date=body, headers=self.headers)
        return resp

    def edit_config(self, body=None):
        """修改参数配置"""
        url = "/dev-api/system/config"
        resp = self.send_put(url=url, Json_date=body, headers=self.headers)
        return resp

    def delete_config(self, config_ids):
        """删除参数配置"""
        url = f"/dev-api/system/config/{config_ids}"
        resp = self.send_delete(url=url, headers=self.headers)
        return resp

    def refresh_cache(self):
        """刷新参数缓存"""
        url = "/dev-api/system/config/refreshCache"
        resp = self.send_get(url=url, headers=self.headers)
        return resp