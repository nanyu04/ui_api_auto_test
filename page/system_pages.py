"""
若依管理系统 - 角色和菜单管理页面对象
"""
import time
from base.base import Base
from base.logs import log
import page


class RoleManagePage(Base):
    """角色管理页面操作封装"""

    def enter_role_manage(self):
        """进入角色管理页面"""
        self.click_element(page.click_role)
        log.info("点击角色管理")
        time.sleep(2)

    def click_add_role(self):
        """点击新增角色"""
        self.wait_click_element(page.Role_Add_Btn)
        log.info("点击新增角色")
        time.sleep(1)

    def is_page_loaded(self):
        """判断角色页面是否加载"""
        return self.is_element_present(page.Role_Add_Btn)


class MenuManagePage(Base):
    """菜单管理页面操作封装"""

    def enter_menu_manage(self):
        """进入菜单管理页面"""
        self.click_element(page.click_menu_m)
        log.info("点击菜单管理")
        time.sleep(2)

    def click_expand(self):
        """点击展开/折叠"""
        self.wait_click_element(page.Menu_Expand_Btn)
        log.info("点击展开/折叠")
        time.sleep(1)

    def is_page_loaded(self):
        """判断菜单页面是否加载"""
        return self.is_element_present(page.Menu_Expand_Btn)


class DeptManagePage(Base):
    """部门管理页面操作封装"""

    def enter_dept_manage(self):
        """进入部门管理页面"""
        self.click_element(page.click_dept_m)
        log.info("点击部门管理")
        time.sleep(2)

    def is_page_loaded(self):
        """判断部门页面是否加载"""
        return self.is_element_present(page.Search_Btn)


class PostManagePage(Base):
    """岗位管理页面操作封装"""

    def enter_post_manage(self):
        """进入岗位管理页面"""
        self.click_element(page.click_post_m)
        log.info("点击岗位管理")
        time.sleep(2)

    def is_page_loaded(self):
        """判断岗位页面是否加载"""
        return self.is_element_present(page.Search_Btn)


class DictManagePage(Base):
    """字典管理页面操作封装"""

    def enter_dict_manage(self):
        """进入字典管理页面"""
        self.click_element(page.click_dict_m)
        log.info("点击字典管理")
        time.sleep(2)

    def is_page_loaded(self):
        """判断字典页面是否加载"""
        return self.is_element_present(page.Search_Btn)


class ConfigManagePage(Base):
    """参数配置页面操作封装"""

    def enter_config_manage(self):
        """进入参数设置页面"""
        self.click_element(page.click_config_m)
        log.info("点击参数设置")
        time.sleep(2)

    def is_page_loaded(self):
        """判断参数页面是否加载"""
        return self.is_element_present(page.Search_Btn)


class NoticeManagePage(Base):
    """通知公告页面操作封装"""

    def enter_notice_manage(self):
        """进入通知公告页面"""
        self.click_element(page.click_notice_m)
        log.info("点击通知公告")
        time.sleep(2)

    def click_add_notice(self):
        """点击新增公告"""
        self.wait_click_element(page.Notice_Add_Btn)
        log.info("点击新增公告")
        time.sleep(1)

    def is_page_loaded(self):
        """判断通知公告页面是否加载"""
        return self.is_element_present(page.Notice_Add_Btn)