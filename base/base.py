from datetime import datetime
import time
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.logs import log


class Base:
    """Selenium 基础操作封装"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def element(self, locator):
        """等待元素可见并返回"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click_element(self, locator):
        """等待元素可见后点击"""
        return self.wait.until(EC.visibility_of_element_located(locator)).click()

    def wait_click_element(self, locator):
        """等待元素可点击后点击"""
        wait_control = self.wait.until(EC.element_to_be_clickable(locator))
        wait_control.click()
        time.sleep(1)

    def send_keys(self, locator, key):
        """等待元素可点击后清空并输入文本"""
        send_keya = self.wait.until(EC.element_to_be_clickable(locator))
        send_keya.clear()
        send_keya.send_keys(key)

    def Save_screenshot(self):
        """错误截图保存"""
        screenshot_path = os.path.join(os.getcwd(), 'screenshot')
        if not os.path.exists(screenshot_path):
            os.mkdir(screenshot_path)
        file_name = datetime.now().strftime('%Y%m%d%H%M%S') + ".png"
        file_path = os.path.join(screenshot_path, file_name)
        self.driver.save_screenshot(file_path)
        return file_path

    def check_text(self, locator, excepted_text):
        """断言元素文本是否与预期一致"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator)).text
            assert excepted_text == element, f"预期文本{excepted_text},实际文本{element} 断言失败"
            log.info("断言用例通过")
        except AssertionError as e:
            path_url = self.Save_screenshot()
            log.error(f"断言不通过 报错信息{str(e)}，截图路径为{path_url}", exc_info=True)
            raise

    def check_element_contains_text(self, locator, expected_text):
        """断言元素文本包含预期文本（用于消息提示等场景）"""
        try:
            element_text = self.wait.until(EC.visibility_of_element_located(locator)).text
            assert expected_text in element_text, f"预期包含'{expected_text}'，实际文本'{element_text}'"
            log.info(f"文本包含断言通过: {element_text}")
        except AssertionError as e:
            path_url = self.Save_screenshot()
            log.error(f"断言不通过 报错信息{str(e)}，截图路径为{path_url}", exc_info=True)
            raise

    def is_element_present(self, locator, timeout=3):
        """判断元素是否存在（不会抛异常）"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except:
            return False

    def switch_to_iframe(self, locator):
        """切换到iframe"""
        iframe = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.switch_to.frame(iframe)

    def scroll_to_element(self, locator):
        """滚动到元素位置"""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)