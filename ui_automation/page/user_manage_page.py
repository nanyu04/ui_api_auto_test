"""
若依管理系统 - 用户管理页面对象
"""
import time
from ui_automation.base.base import Base
from ui_automation.base.logs import log
from ui_automation import page


class UserManagePage(Base):
    """用户管理页面操作封装"""

    def enter_system_manage(self):
        """展开系统管理菜单"""
        self.click_element(page.click_systemm)
        log.info("点击系统管理")
        time.sleep(2)

    def enter_user_manage(self):
        """进入用户管理页面"""
        self.click_element(page.click_userm)
        log.info("点击用户管理")
        time.sleep(2)

    def click_add_user(self):
        """点击新增用户按钮"""
        self.wait_click_element(page.click_addUser)
        log.info("点击新增用户")
        time.sleep(1)

    def input_user_nickname(self, nickname):
        """输入用户昵称"""
        self.send_keys(page.UserId, nickname)
        log.info(f"输入用户昵称: {nickname}")

    def input_phone(self, phone):
        """输入手机号码"""
        self.send_keys(page.PhoneNumber, phone)
        log.info(f"输入手机号码: {phone}")

    def input_user_name(self, username):
        """输入用户名称"""
        self.send_keys(page.UserName, username)
        log.info(f"输入用户名称: {username}")

    def select_gender(self):
        """选择性别(女)"""
        self.wait_click_element(page.Click_Gender)
        log.info("点击性别下拉框")
        self.wait_click_element(page.Gender)
        log.info("选中性别: 女")

    def select_post(self):
        """选择岗位(董事长)"""
        self.wait_click_element(page.Occuptionset)
        log.info("点击岗位下拉框")
        self.wait_click_element(page.Occuption)
        log.info("选中岗位: 董事长")

    def select_role(self):
        """选择角色(普通角色)"""
        self.wait_click_element(page.Click_Character)
        log.info("点击角色下拉框")
        time.sleep(1)
        self.wait_click_element(page.Character)
        log.info("选中角色: 普通角色")

    def select_dept(self):
        """选择部门(若依科技)"""
        self.wait_click_element(page.Click_partment)
        log.info("点击部门下拉框")
        time.sleep(1)
        self.wait_click_element(page.partment)
        log.info("选中部门: 若依科技")

    def input_email(self, email):
        """输入邮箱"""
        self.send_keys(page.PostId, email)
        log.info(f"输入邮箱: {email}")

    def click_confirm(self):
        """点击确定按钮"""
        self.wait_click_element(page.Ensure)
        log.info("点击确定")
        time.sleep(2)

    def click_cancel(self):
        """点击取消按钮"""
        self.wait_click_element(page.Cancel)
        log.info("点击取消")
        time.sleep(1)

    def get_success_message(self):
        """获取操作成功消息"""
        msg_element = self.element(page.Adduser_success)
        return msg_element.text

    def click_search(self):
        """点击搜索按钮"""
        self.wait_click_element(page.Search_Btn)
        log.info("点击搜索")
        time.sleep(2)

    def click_reset(self):
        """点击重置按钮"""
        self.wait_click_element(page.Reset_Btn)
        log.info("点击重置")
        time.sleep(1)

    def is_first_row_visible(self):
        """判断表格第一行是否可见"""
        return self.is_element_present(page.Table_First_Row)