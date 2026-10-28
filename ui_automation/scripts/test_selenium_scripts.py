"""
若依管理系统 - Selenium UI 自动化测试用例 (10条)
覆盖场景：登录、用户管理、角色管理、菜单管理、部门管理、通知公告、监控
"""
import time
import unittest

import allure
import pytest
from ui_automation.base.GetDriver import Getdriver
from ui_automation.base.logs import log
from ui_automation.page.login_page import LoginPage
from ui_automation.page.user_manage_page import UserManagePage
from ui_automation.page.system_pages import (
    RoleManagePage, MenuManagePage, DeptManagePage,
    PostManagePage, DictManagePage, NoticeManagePage, ConfigManagePage
)
from ui_automation.page.monitor_page import MonitorPage


@pytest.mark.usefixtures("selenium_driver")
class TestSeleniumRuoYi:
    """若依管理系统Selenium UI自动化测试"""

    # ==================== 用例1: 登录成功 ====================
    @allure.epic("若依UI自动化测试")
    @allure.feature("登录模块")
    @allure.story("登录功能")
    @allure.title("TC01-正确的账号密码登录成功")
    def test01_login_success(self, selenium_driver):
        driver = selenium_driver
        login_page = LoginPage(driver)
        with allure.step("输入admin/admin123并登录"):
            login_page.login("admin", "admin123")
        with allure.step("验证登录成功进入首页"):
            assert login_page.is_logged_in(), "登录失败，未跳转到首页"
            log.info("TC01-登录成功验证通过")

    # ==================== 用例2: 登录后进入用户管理页面 ====================
    @allure.epic("若依UI自动化测试")
    @allure.feature("系统管理")
    @allure.story("用户管理")
    @allure.title("TC02-进入用户管理页面并显示用户列表")
    def test02_enter_user_manage(self, selenium_driver):
        driver = selenium_driver
        login_page = LoginPage(driver)
        user_page = UserManagePage(driver)
        with allure.step("先登录系统"):
            login_page.login("admin", "admin123")
        with allure.step("展开系统管理菜单"):
            user_page.enter_system_manage()
        with allure.step("进入用户管理页面"):
            user_page.enter_user_manage()
        with allure.step("验证用户列表加载"):
            assert user_page.is_first_row_visible(), "用户列表未加载"
            log.info("TC02-用户管理页面加载验证通过")

    # ==================== 用例3: 登录后进入角色管理页面 ====================
    @allure.epic("若依UI自动化测试")
    @allure.feature("系统管理")
    @allure.story("角色管理")
    @allure.title("TC03-进入角色管理页面并显示角色列表")
    def test03_enter_role_manage(self, selenium_driver):
        driver = selenium_driver
        login_page = LoginPage(driver)
        user_page = UserManagePage(driver)
        role_page = RoleManagePage(driver)
        with allure.step("先登录并展开系统管理"):
            login_page.login("admin", "admin123")
            user_page.enter_system_manage()
        with allure.step("进入角色管理页面"):
            role_page.enter_role_manage()
        with allure.step("验证角色列表加载"):
            assert role_page.is_page_loaded(), "角色列表未加载"
            log.info("TC03-角色管理页面加载验证通过")

    # ==================== 用例4: 登录后进入菜单管理页面 ====================
    @allure.epic("若依UI自动化测试")
    @allure.feature("系统管理")
    @allure.story("菜单管理")
    @allure.title("TC04-进入菜单管理页面并展开菜单树")
    def test04_enter_menu_manage(self, selenium_driver):
        driver = selenium_driver
        login_page = LoginPage(driver)
        user_page = UserManagePage(driver)
        menu_page = MenuManagePage(driver)
        with allure.step("先登录并展开系统管理"):
            login_page.login("admin", "admin123")
            user_page.enter_system_manage()
        with allure.step("进入菜单管理页面"):
            menu_page.enter_menu_manage()
        with allure.step("验证菜单树加载"):
            assert menu_page.is_page_loaded(), "菜单树未加载"
            log.info("TC04-菜单管理页面加载验证通过")

    # ==================== 用例5: 登录后进入部门管理页面 ====================
    @allure.epic("若依UI自动化测试")
    @allure.feature("系统管理")
    @allure.story("部门管理")
    @allure.title("TC05-进入部门管理页面并显示部门树")
    def test05_enter_dept_manage(self, selenium_driver):
        driver = selenium_driver
        login_page = LoginPage(driver)
        user_page = UserManagePage(driver)
        dept_page = DeptManagePage(driver)
        with allure.step("先登录并展开系统管理"):
            login_page.login("admin", "admin123")
            user_page.enter_system_manage()
        with allure.step("进入部门管理页面"):
            dept_page.enter_dept_manage()
        with allure.step("验证部门树加载"):
            assert dept_page.is_page_loaded(), "部门树未加载"
            log.info("TC05-部门管理页面加载验证通过")

    # ==================== 用例6: 登录后进入通知公告页面 ====================
    @allure.epic("若依UI自动化测试")
    @allure.feature("系统管理")
    @allure.story("通知公告")
    @allure.title("TC06-进入通知公告页面并显示公告列表")
    def test06_enter_notice_manage(self, selenium_driver):
        driver = selenium_driver
        login_page = LoginPage(driver)
        user_page = UserManagePage(driver)
        notice_page = NoticeManagePage(driver)
        with allure.step("先登录并展开系统管理"):
            login_page.login("admin", "admin123")
            user_page.enter_system_manage()
        with allure.step("进入通知公告页面"):
            notice_page.enter_notice_manage()
        with allure.step("验证公告列表加载"):
            assert notice_page.is_page_loaded(), "公告列表未加载"
            log.info("TC06-通知公告页面加载验证通过")

    # ==================== 用例7: 登录后进入在线用户监控 ====================
    @allure.epic("若依UI自动化测试")
    @allure.feature("系统监控")
    @allure.story("在线用户")
    @allure.title("TC07-进入在线用户页面查看在线用户")
    def test07_enter_online_user(self, selenium_driver):
        driver = selenium_driver
        login_page = LoginPage(driver)
        monitor_page = MonitorPage(driver)
        with allure.step("先登录"):
            login_page.login("admin", "admin123")
        with allure.step("展开系统监控菜单"):
            monitor_page.enter_monitor_menu()
        with allure.step("进入在线用户页面"):
            monitor_page.enter_online_user()
        with allure.step("验证在线用户页加载"):
            assert monitor_page.is_page_loaded(), "在线用户页面未加载"
            log.info("TC07-在线用户页面加载验证通过")

    # ==================== 用例8: 登录后进入服务监控 ====================
    @allure.epic("若依UI自动化测试")
    @allure.feature("系统监控")
    @allure.story("服务监控")
    @allure.title("TC08-进入服务监控页面查看服务器信息")
    def test08_enter_server_monitor(self, selenium_driver):
        driver = selenium_driver
        login_page = LoginPage(driver)
        monitor_page = MonitorPage(driver)
        with allure.step("先登录"):
            login_page.login("admin", "admin123")
        with allure.step("展开系统监控菜单"):
            monitor_page.enter_monitor_menu()
        with allure.step("进入服务监控页面"):
            monitor_page.enter_server_monitor()
        with allure.step("验证服务监控页加载"):
            assert monitor_page.is_page_loaded(), "服务监控页面未加载"
            log.info("TC08-服务监控页面加载验证通过")

    # ==================== 用例9: 登录后进入缓存监控 ====================
    @allure.epic("若依UI自动化测试")
    @allure.feature("系统监控")
    @allure.story("缓存监控")
    @allure.title("TC09-进入缓存监控页面查看缓存信息")
    def test09_enter_cache_monitor(self, selenium_driver):
        driver = selenium_driver
        login_page = LoginPage(driver)
        monitor_page = MonitorPage(driver)
        with allure.step("先登录"):
            login_page.login("admin", "admin123")
        with allure.step("展开系统监控菜单"):
            monitor_page.enter_monitor_menu()
        with allure.step("进入缓存监控页面"):
            monitor_page.enter_cache_monitor()
        with allure.step("验证缓存监控页加载"):
            assert monitor_page.is_page_loaded(), "缓存监控页面未加载"
            log.info("TC09-缓存监控页面加载验证通过")

    # ==================== 用例10: 新增用户-取消操作 ====================
    @allure.epic("若依UI自动化测试")
    @allure.feature("系统管理")
    @allure.story("用户管理")
    @allure.title("TC10-打开新增用户弹窗并取消操作")
    def test10_cancel_add_user(self, selenium_driver):
        driver = selenium_driver
        login_page = LoginPage(driver)
        user_page = UserManagePage(driver)
        with allure.step("先登录并进入用户管理"):
            login_page.login("admin", "admin123")
            user_page.enter_system_manage()
            user_page.enter_user_manage()
        with allure.step("点击新增按钮"):
            user_page.click_add_user()
        with allure.step("输入用户昵称"):
            user_page.input_user_nickname("测试用户_UI")
        with allure.step("点击取消"):
            user_page.click_cancel()
        with allure.step("验证弹窗关闭"):
            assert not user_page.is_element_present(
                ("xpath", "//span[contains(text(),'添加用户')]"), timeout=2
            ), "取消后弹窗未关闭"
            log.info("TC10-取消新增用户操作验证通过")