"""
Selenium 测试共享 fixture 配置
提供浏览器驱动生命周期管理
"""
import pytest
from ui_automation.base.GetDriver import Getdriver
from ui_automation.base.logs import log


@pytest.fixture(scope="class")
def selenium_driver():
    """Selenium测试：启动浏览器 -> 执行用例 -> 关闭浏览器"""
    log.info("========== 启动浏览器 ==========")
    driver = Getdriver.Get_driver()
    yield driver
    log.info("========== 关闭浏览器 ==========")
    Getdriver.quit_driver()