"""
【场景测试】— 通用文件上传（接口文档 4.5.1 ~ 4.5.4）

用内存字节流上传，不依赖磁盘上的样本文件，避免"CI 上找不到文件"的经典问题。
"""
import io

import allure
import pytest

from api_automation.apis import common_api
from api_automation.common import AssertionEngine

PNG_HEADER = bytes.fromhex("89504e470d0a1a0a")  # PNG 魔数，用于通过后端类型校验


@allure.epic("若依接口自动化")
@allure.feature("通用文件")
class TestUpload:
    """文件上传"""

    @pytest.mark.smoke
    @pytest.mark.P1
    @allure.story("单文件上传")
    @allure.title("上传图片返回文件名与可访问 url")
    def test_upload_single_file(self, logged_in_admin):
        files = {"file": ("auto_upload.png", io.BytesIO(PNG_HEADER + b"0" * 64), "image/png")}
        resp = common_api.upload(files)

        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200).has_field("fileName").has_field("url")

        url = ae.extract("url")
        assert url, f"上传成功但 url 为空：{resp.text}"
        assert url.startswith("/") or url.startswith("http"), f"url 格式不正确：{url}"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("多文件上传")
    @allure.title("一次上传多个文件返回文件列表")
    def test_upload_multiple_files(self, logged_in_admin):
        files = [
            ("files", ("auto_m1.png", io.BytesIO(PNG_HEADER + b"1" * 32), "image/png")),
            ("files", ("auto_m2.png", io.BytesIO(PNG_HEADER + b"2" * 32), "image/png")),
        ]
        resp = common_api.uploads(files)
        body = resp.json()

        AssertionEngine(resp).status_code(200)
        assert body.get("code") == 200, f"多文件上传失败：{resp.text}"

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("上传校验")
    @allure.title("上传不允许的扩展名被拒绝")
    def test_upload_rejected_extension(self, logged_in_admin):
        files = {"file": ("evil.exe", io.BytesIO(b"MZ" + b"0" * 32), "application/octet-stream")}
        resp = common_api.upload(files)
        body = resp.json()

        AssertionEngine(resp).status_code(200)
        assert body.get("code") == 500, f"非法扩展名竟然上传成功：{resp.text}"
        # 不同校验分支的提示文案不同（后缀不允许 / 文件类型不允许），只断言"给出了明确的失败原因"
        assert body.get("msg"), "上传失败却没有给出原因"
        assert "不正确" in body["msg"] or "不允许" in body["msg"] or "上传" in body["msg"], body["msg"]

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("文件下载")
    @allure.title("下载不存在的资源返回业务错误")
    def test_download_resource_not_exists(self, logged_in_admin):
        resp = common_api.download_resource("upload/not_exists_file.png")
        assert resp.status_code in (200, 404), f"异常状态码：{resp.status_code}"
        if "application/json" in (resp.headers.get("content-type") or ""):
            body = resp.json()
            assert body.get("code") == 500, f"下载不存在的资源应报错：{resp.text[:200]}"
        else:
            assert resp.text, "下载不存在的资源没有返回任何内容"
