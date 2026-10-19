"""
pytest 共享 fixture 配置文件
提供 base_api（鉴权基类）、login_with_token（获取登录token）等夹具
"""
import pytest

from Api.UserApi import UserApi


@pytest.fixture(scope="class")
def base_api():
    """提供 Api_common 鉴权基类实例"""
    from base_Api.base import Api_common
    return Api_common()


@pytest.fixture(scope="class")
def login_with_token():
    """登录并返回 Bearer token，后续API测试复用此token"""
    login_api = UserApi()
    resp = login_api.login_user(username="admin", password="admin123")
    result = resp.json()
    token = result["token"]
    return token