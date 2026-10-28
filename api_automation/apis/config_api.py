"""
【接口层】— 参数配置模块（RuoYi-Vue）

对应接口文档 4.2.66 ~ 4.2.73。
"""
from typing import Optional

from api_automation.common import BaseApi


class ConfigApi(BaseApi):
    """参数配置接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询参数列表 GET /system/config/list"""
        return self.get("/system/config/list", params=params)

    def detail(self, config_id):
        """查询参数详细 GET /system/config/{configId}"""
        return self.get(f"/system/config/{config_id}")

    def by_key(self, config_key):
        """根据参数键名查询参数值 GET /system/config/configKey/{configKey}"""
        return self.get(f"/system/config/configKey/{config_key}")

    def create(self, body: dict):
        """新增参数 POST /system/config"""
        return self.post("/system/config", json=body)

    def update(self, body: dict):
        """修改参数 PUT /system/config"""
        return self.put("/system/config", json=body)

    def remove(self, config_ids):
        """删除参数 DELETE /system/config/{configIds}"""
        return self.delete(f"/system/config/{config_ids}")

    def refresh_cache(self):
        """刷新参数缓存 DELETE /system/config/refreshCache"""
        return self.delete("/system/config/refreshCache")

    def export(self, params: Optional[dict] = None):
        """导出参数 POST /system/config/export"""
        return self.post("/system/config/export", data=params or {})


config_api = ConfigApi()