"""
【接口层】— 代码生成模块（RuoYi-Vue）

对应接口文档 4.4.1 ~ 4.4.13。

注意：预览 / 下载 / 生成代码类接口返回的是 HTML 或二进制流，
不是 JSON，因此不要对它们做 AssertionEngine 的 JSON 断言。
"""
from typing import Optional

from api_automation.common import BaseApi


class GenApi(BaseApi):
    """代码生成接口"""

    service_path = ""

    def list(self, params: Optional[dict] = None):
        """查询代码生成列表 GET /tool/gen/list"""
        return self.get("/tool/gen/list", params=params)

    def detail(self, table_id):
        """查询表详细信息 GET /tool/gen/{tableId}"""
        return self.get(f"/tool/gen/{table_id}")

    def db_list(self, params: Optional[dict] = None):
        """查询数据库表列表 GET /tool/gen/db/list"""
        return self.get("/tool/gen/db/list", params=params)

    def column(self, table_id):
        """查询表字段列表 GET /tool/gen/column/{tableId}"""
        return self.get(f"/tool/gen/column/{table_id}")

    def import_table(self, tables: str):
        """导入表结构 POST /tool/gen/importTable（tables 多个用逗号分隔）"""
        return self.post("/tool/gen/importTable", params={"tables": tables})

    def create_table(self, body: dict):
        """创建表结构 POST /tool/gen/createTable"""
        return self.post("/tool/gen/createTable", data=body)

    def update(self, body: dict):
        """修改代码生成业务 PUT /tool/gen"""
        return self.put("/tool/gen", json=body)

    def remove(self, table_ids):
        """删除表数据 DELETE /tool/gen/{tableIds}"""
        return self.delete(f"/tool/gen/{table_ids}")

    def preview(self, table_id):
        """预览生成代码 GET /tool/gen/preview/{tableId}（返回 HTML）"""
        return self.get(f"/tool/gen/preview/{table_id}")

    def download(self, table_name):
        """下载生成代码 GET /tool/gen/download/{tableName}（返回 zip）"""
        return self.get(f"/tool/gen/download/{table_name}")

    def gen_code(self, table_name):
        """生成代码（自定义路径） GET /tool/gen/genCode/{tableName}"""
        return self.get(f"/tool/gen/genCode/{table_name}")

    def synch_db(self, table_name):
        """同步表结构 GET /tool/gen/synchDb/{tableName}"""
        return self.get(f"/tool/gen/synchDb/{table_name}")

    def batch_gen_code(self, tables: str):
        """批量生成代码 GET /tool/gen/batchGenCode（tables 多个用逗号分隔）"""
        return self.get("/tool/gen/batchGenCode", params={"tables": tables})


gen_api = GenApi()