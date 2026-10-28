"""
若依管理系统 - 监控管理页面对象
"""
import time
from ui_automation.base.base import Base
from ui_automation.base.logs import log
from ui_automation import page


class MonitorPage(Base):
    """监控管理页面操作封装"""

    def enter_monitor_menu(self):
        """展开系统监控菜单"""
        self.click_element(page.click_monitor_m)
        log.info("点击系统监控")
        time.sleep(2)

    def enter_online_user(self):
        """进入在线用户页面"""
        self.click_element(page.click_online_m)
        log.info("点击在线用户")
        time.sleep(2)

    def enter_job_manage(self):
        """进入定时任务页面"""
        self.click_element(page.click_job_m)
        log.info("点击定时任务")
        time.sleep(2)

    def enter_server_monitor(self):
        """进入服务监控页面"""
        self.click_element(page.click_server_m)
        log.info("点击服务监控")
        time.sleep(2)

    def enter_cache_monitor(self):
        """进入缓存监控页面"""
        self.click_element(page.click_cache_m)
        log.info("点击缓存监控")
        time.sleep(2)

    def is_page_loaded(self):
        """判断页面是否正常加载"""
        return self.is_element_present(page.Home_Welcome) or self.is_element_present(page.Search_Btn)