"""
【接口层】— 通用文件模块（RuoYi-Vue）

对应接口文档 4.5.1 ~ 4.5.4。
"""
from typing import Optional

from api_automation.common import BaseApi


class CommonApi(BaseApi):
    """通用文件上传 / 下载接口"""

    service_path = ""

    def upload(self, files: dict):
        """单文件上传 POST /common/upload（form-data: file）"""
        return self.post("/common/upload", files=files)

    def uploads(self, files: dict):
        """多文件上传 POST /common/uploads（form-data: files）"""
        return self.post("/common/uploads", files=files)

    def download(self, file_name: str, delete: bool = False):
        """通用文件下载 GET /common/download"""
        return self.get("/common/download",
                        params={"fileName": file_name, "delete": str(delete).lower()})

    def download_resource(self, resource: str):
        """资源文件下载 GET /common/download/resource"""
        return self.get("/common/download/resource", params={"resource": resource})


common_api = CommonApi()