"""
【框架自测】— 重试机制

这是框架里曾经真实存在的缺陷：tenacity 的 stop= 和 retry= 是两个参数，
原实现把 stop_after_attempt(...) 传给了 retry=，
结果是"重试策略"变成了"只对 StopAfterAttempt 异常重试"，
真遇到网络抖动反而一次都不重试 —— 加了装饰器等于没加。

这组用例就是为了防止该缺陷回归。
"""
import pytest
import requests

from api_automation.common.retry import retry_on_failure, safe_call, RETRYABLE_EXCEPTIONS


class TestRetry:
    """重试装饰器行为验证"""

    def test_connection_error_is_retried(self):
        """连接类异常必须重试：调用 3 次说明重试真的生效了"""
        calls = []

        @retry_on_failure(max_attempts=3, wait_seconds=0)
        def flaky():
            calls.append(1)
            raise requests.exceptions.ConnectionError("boom")

        with pytest.raises(requests.exceptions.ConnectionError):
            flaky()

        assert len(calls) == 3, f"期望重试到 3 次，实际只执行了 {len(calls)} 次"

    def test_success_after_failure_stops_retrying(self):
        """第 2 次成功就不该再重试"""
        calls = []

        @retry_on_failure(max_attempts=5, wait_seconds=0)
        def flaky():
            calls.append(1)
            if len(calls) < 2:
                raise requests.exceptions.Timeout("slow")
            return "ok"

        assert flaky() == "ok"
        assert len(calls) == 2

    def test_business_assertion_is_not_retried(self):
        """断言失败不重试 —— 重试会掩盖真实的业务缺陷"""
        calls = []

        @retry_on_failure(max_attempts=5, wait_seconds=0)
        def always_fail():
            calls.append(1)
            raise AssertionError("业务断言不通过")

        with pytest.raises(AssertionError):
            always_fail()

        assert len(calls) == 1, "断言失败不应触发重试"

    def test_safe_call_retries_operation(self):
        """safe_call 对单步操作重试"""
        calls = []

        def op():
            calls.append(1)
            if len(calls) < 3:
                raise requests.exceptions.ConnectionError("boom")
            return "done"

        assert safe_call(op, max_attempts=3, wait_seconds=0) == "done"
        assert len(calls) == 3

    def test_retryable_exception_whitelist(self):
        """白名单只覆盖环境类异常，不含业务异常"""
        assert requests.exceptions.ConnectionError in RETRYABLE_EXCEPTIONS
        assert requests.exceptions.Timeout in RETRYABLE_EXCEPTIONS
        assert AssertionError not in RETRYABLE_EXCEPTIONS