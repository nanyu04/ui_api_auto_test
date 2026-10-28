"""
【接口层】— 字典管理模块（RuoYi-Vue）

对应接口文档 4.2.51 ~ 4.2.65。
字典类型与字典数据分开封装（后端是两个 Controller）。
"""
from typing import Optional

from api_automation.common import BaseApi


class DictTypeApi(BaseApi):
    """字典类型接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询字典类型列表 GET /system/dict/type/list"""
        return self.get("/system/dict/type/list", params=params)

    def detail(self, dict_id):
        """查询字典类型详细 GET /system/dict/type/{dictId}"""
        return self.get(f"/system/dict/type/{dict_id}")

    def create(self, body: dict):
        """新增字典类型 POST /system/dict/type"""
        return self.post("/system/dict/type", json=body)

    def update(self, body: dict):
        """修改字典类型 PUT /system/dict/type"""
        return self.put("/system/dict/type", json=body)

    def remove(self, dict_ids):
        """删除字典类型 DELETE /system/dict/type/{dictIds}"""
        return self.delete(f"/system/dict/type/{dict_ids}")

    def refresh_cache(self):
        """刷新字典缓存 DELETE /system/dict/type/refreshCache"""
        return self.delete("/system/dict/type/refreshCache")

    def option_select(self):
        """获取字典类型下拉选项 GET /system/dict/type/optionselect"""
        return self.get("/system/dict/type/optionselect")

    def export(self, params: Optional[dict] = None):
        """导出字典类型 POST /system/dict/type/export"""
        return self.post("/system/dict/type/export", data=params or {})


class DictDataApi(BaseApi):
    """字典数据接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询字典数据列表 GET /system/dict/data/list"""
        return self.get("/system/dict/data/list", params=params)

    def detail(self, dict_code):
        """查询字典数据详细 GET /system/dict/data/{dictCode}"""
        return self.get(f"/system/dict/data/{dict_code}")

    def by_type(self, dict_type):
        """根据字典类型查询字典数据 GET /system/dict/data/type/{dictType}"""
        return self.get(f"/system/dict/data/type/{dict_type}")

    def create(self, body: dict):
        """新增字典数据 POST /system/dict/data"""
        return self.post("/system/dict/data", json=body)

    def update(self, body: dict):
        """修改字典数据 PUT /system/dict/data"""
        return self.put("/system/dict/data", json=body)

    def remove(self, dict_codes):
        """删除字典数据 DELETE /system/dict/data/{dictCodes}"""
        return self.delete(f"/system/dict/data/{dict_codes}")

    def export(self, params: Optional[dict] = None):
        """导出字典数据 POST /system/dict/data/export"""
        return self.post("/system/dict/data/export", data=params or {})


dict_type_api = DictTypeApi()
dict_data_api = DictDataApi()