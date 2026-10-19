import requests
from requests import Session


class Api_common:
    def __init__(self):
        self.session = Session()
        self.base_url = "http://127.0.0.1:8081"
        self.headers = {
            "Content-Type": "application/json"
        }

        self.session.trust_env = False
    def request(self, path, **kwargs):
        url = path if path.startswith("http") else f"{self.base_url}/{path.lstrip('/')}"
        return self.session.request(url=url, **kwargs)

    def feihua(self):
        print("feihua")

    # 提供鉴权头
    def set_token(self, token):
        self.headers["Authorization"] = f"Bearer {token}"

    # post的请求方法
    def send_post(self, url=None, Json_date=None, headers=None):
        full_url = self.base_url + url
        res = self.session.post(full_url, json=Json_date, headers=self.headers)
        return res

    # Get的请求方法
    def send_get(self, url=None, params=None, headers=None):
        full_url = self.base_url + url
        res = self.session.get(full_url, params=params, headers=self.headers)
        print(f"\n=== 调试信息 ===")
        print(f"请求URL: {res.request.url}")
        print(f"请求方法: {res.request.method}")
        print(f"请求头: {res.request.headers}")
        print(f"状态码: {res.status_code}")
        print(f"响应体: {res.text[:500]}")
        return res

    # Put的请求方法
    def send_put(self, url=None, Json_date=None, headers=None):
        full_url = self.base_url + url
        res = self.session.put(full_url, json=Json_date, headers=self.headers)
        print(f"\n=== 调试信息 ===")
        print(f"请求URL: {res.request.url}")
        print(f"请求方法: {res.request.method}")
        print(f"状态码: {res.status_code}")
        print(f"响应体: {res.text[:500]}")
        return res

    # Delete的请求方法
    def send_delete(self, url=None, headers=None):
        full_url = self.base_url + url
        res = self.session.delete(full_url, headers=self.headers)
        print(f"\n=== 调试信息 ===")
        print(f"请求URL: {res.request.url}")
        print(f"请求方法: {res.request.method}")
        print(f"状态码: {res.status_code}")
        print(f"响应体: {res.text[:500]}")
        return res
