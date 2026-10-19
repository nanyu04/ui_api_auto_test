"""
若依管理系统 - 登录页面对象
"""
import time
from base.base import Base
from base.logs import log
import page


class LoginPage(Base):
    """登录页面操作封装"""

    def enter_username(self, username):
        """输入用户名"""
        self.send_keys(page.Login_Username, username)
        log.info(f"输入用户名: {username}")

    def enter_password(self, password):
        """输入密码"""
        self.send_keys(page.Login_Password, password)
        log.info("输入密码")

    def click_login(self):
        """点击登录按钮"""
        self.click_element(page.Enter)
        log.info("点击登录按钮")
        time.sleep(2)

    def login(self, username, password):
        """完整登录流程"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def is_logged_in(self):
        """判断是否登录成功(首页可见)"""
        try:
            self.element(page.Home_Welcome)
            return True
        except:
            return False

    def logout(self):
        """退出登录"""
        self.click_element(page.User_Avatar)
        time.sleep(1)
        self.click_element(page.Logout_Btn)
        log.info("退出登录")
        time.sleep(2)