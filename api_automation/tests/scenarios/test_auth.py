"""
【场景测试】— 登录认证（接口文档 4.1）

覆盖：验证码、登录成功/失败、令牌使用、认证失败时的响应语义。
"""
import allure
import pytest

from api_automation.apis import auth_api
from api_automation.common import AssertionEngine, logger
from api_automation.config import settings
from api_automation.utils import get_project_root, read_yaml

LOGIN_CASES = read_yaml(get_project_root() / "data/test_data/login_cases.yaml")


@allure.epic("若依接口自动化")
@allure.feature("登录认证")
class TestLogin:
    """登录接口"""

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("正确登录")
    @allure.title("admin 正确账号密码登录成功并返回 token")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_success(self):
        resp = auth_api.login(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)

        ae = AssertionEngine(resp)
        ae.status_code(200).jsonpath_eq("$.code", 200).has_field("token")
        token = ae.extract("token")
        assert token, f"登录成功但 token 为空：{resp.text}"
        logger.info(f"🔐 获取到 token，长度 {len(token)}")

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("登录失败")
    @allure.title("登录失败场景参数化：密码错误 / 用户不存在 / 字段为空 / 超长 / 注入")
    @pytest.mark.parametrize("case", LOGIN_CASES, ids=[c["title"] for c in LOGIN_CASES])
    def test_login_failure_scenarios(self, case):
        resp = auth_api.login(case["username"], case["password"])
        body = resp.json()

        # 若依的约定：业务异常也是 HTTP 200，靠 body.code 区分
        AssertionEngine(resp).status_code(200)
        assert body.get("code") == case["expect_code"], (
            f"[{case['title']}] 期望 code={case['expect_code']}，实际 {body.get('code')}：{resp.text}"
        )
        if case.get("expect_msg"):
            assert case["expect_msg"] in body.get("msg", ""), (
                f"[{case['title']}] 提示信息不含 '{case['expect_msg']}'：{body.get('msg')}"
            )

    @pytest.mark.regression
    @pytest.mark.P2
    @allure.story("登录失败")
    @allure.title("错误密码与不存在用户的提示一致（不泄露账号是否存在）")
    def test_failure_message_does_not_leak_account_existence(self):
        wrong_pwd = auth_api.login(settings.ADMIN_USERNAME, "definitely_wrong_pwd_123").json()
        no_user = auth_api.login("no_such_user_zzz_001", "definitely_wrong_pwd_123").json()

        assert wrong_pwd["code"] == no_user["code"] == 500
        assert wrong_pwd["msg"] == no_user["msg"], (
            "密码错误与用户不存在的提示不同，攻击者可据此枚举有效账号"
        )


@allure.epic("若依接口自动化")
@allure.feature("登录认证")
class TestCaptchaAndSession:
    """验证码与登录态"""

    @pytest.mark.smoke
    @pytest.mark.P1
    @allure.story("验证码")
    @allure.title("获取验证码返回 uuid 与 base64 图片，且未开启时 img 为空")
    def test_captcha_image(self):
        resp = auth_api.captcha()
        body = resp.json()

        AssertionEngine(resp).status_code(200)
        assert body.get("code") == 200
        assert "captchaEnabled" in body, f"缺少 captchaEnabled 字段：{body}"

        if body.get("captchaEnabled"):
            assert body.get("uuid"), "开启验证码时必须返回 uuid"
            assert body.get("img"), "开启验证码时必须返回图片 base64"
        else:
            assert body.get("img") in (None, ""), "关闭验证码时不应返回图片"

    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.story("登录态")
    @allure.title("登录后携带 token 可获取用户信息与路由菜单")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_info_and_routers_after_login(self, logged_in_admin):
        ae = AssertionEngine(auth_api.get_info())
        ae.status_code(200).jsonpath_eq("$.code", 200).has_field("user").has_field("roles").has_field("permissions")
        assert ae.extract("user.userName") == settings.ADMIN_USERNAME

        routers = AssertionEngine(auth_api.get_routers())
        routers.status_code(200).jsonpath_eq("$.code", 200)
        assert routers.extract("data"), "路由菜单不应为空"

    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("登录态")
    @allure.title("登出后原 token 失效（再次访问 getInfo 被拒绝）")
    def test_logout_invalidates_token(self, logged_in_admin):
        AssertionEngine(auth_api.logout()).status_code(200).jsonpath_eq("$.code", 200)

        resp = auth_api.get_info()
        assert _is_rejected(resp), f"登出后仍能访问受保护接口：{resp.text}"


@allure.epic("若依接口自动化")
@allure.feature("认证与鉴权语义")
class TestAuthSemantics:
    """未认证访问的响应语义"""

    @pytest.mark.smoke
    @pytest.mark.P1
    @allure.story("未认证访问")
    @allure.title("未携带 token 访问受保护接口：HTTP 200 但业务码 401")
    def test_unauthenticated_returns_401_business_code(self, api_client):
        api_client.clear_auth()
        resp = api_client.get("/system/user/list")

        # 记录实际语义：若依的 AuthenticationEntryPoint 主动把 HTTP 状态设为 200，
        # 只靠 body.code=401 表达未认证 —— 这正是需要固化下来的接口契约。
        AssertionEngine(resp).status_code(200)
        body = resp.json()
        assert body.get("code") == 401, f"未认证访问应返回业务码 401，实际 {body}"
        assert "认证失败" in body.get("msg", "")
    @pytest.mark.regression
    @pytest.mark.P1
    @allure.story("未认证访问")
    @allure.title("伪造 token 访问受保护接口同样被拒绝")
    def test_forged_token_is_rejected(self, api_client):
        api_client.clear_auth()
        api_client.set_header("Authorization", "Bearer this.is.not.a.valid.token")
        try:
            resp = api_client.get("/system/user/list")
            assert _is_rejected(resp), f"伪造 token 竟然通过了鉴权：{resp.text}"
        finally:
            api_client.clear_auth()


def _is_rejected(resp) -> bool:
    """兼容两种拒绝语义：HTTP 401/403，或 HTTP 200 但业务码 401/403"""
    if resp.status_code in (401, 403):
        return True
    try:
        return resp.json().get("code") in (401, 403)
    except Exception:
        return False
