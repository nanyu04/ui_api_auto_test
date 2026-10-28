"""
【重试工具】— 基于 tenacity 的测试重试装饰器

设计原则：
  只对"环境类"异常重试（连接失败 / 超时 / 连接中断）。
  断言失败不重试 —— 断言失败说明被测系统行为不符合预期，重试只会掩盖缺陷。

用法一：装饰器
    from common.retry import retry_on_failure

    @retry_on_failure(max_attempts=3, wait_seconds=2)
    def test_something(a_new_user):
        ...

用法二：safe_call —— 重试单个操作
    resp = safe_call(client.get, "/system/user/list", max_attempts=3)

参数：
    max_attempts: 最多执行次数（含第一次），默认 3
    wait_seconds: 两次重试之间的等待秒数，默认 2
"""
import requests
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

# 只有这几类异常才重试：属于网络/环境抖动，与被测系统缺陷无关
RETRYABLE_EXCEPTIONS = (
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
    requests.exceptions.ChunkedEncodingError,
)


def retry_on_failure(max_attempts: int = 3, wait_seconds: int = 2):
    """
    测试失败自动重试（装饰器版本）

    注意：tenacity 里 stop= 决定"什么时候停"，retry= 决定"要不要重试"，
    两者是不同的参数，不能互相顶替。
    """
    return retry(
        reraise=True,
        stop=stop_after_attempt(max_attempts),
        wait=wait_fixed(wait_seconds),
        retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
    )


def safe_call(func, *args, max_attempts: int = 3, wait_seconds: int = 2, **kwargs):
    """
    重试单个操作（函数调用版本）

    适用于只需要重试某一步 API 调用而非整个测试的场景。

    用法：
        resp = safe_call(user_api.list, params={"pageNum": 1}, max_attempts=5)
    """

    @retry(
        reraise=True,
        stop=stop_after_attempt(max_attempts),
        wait=wait_fixed(wait_seconds),
        retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
    )
    def _call():
        return func(*args, **kwargs)

    return _call()
