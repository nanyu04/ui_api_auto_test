from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os


class Getdriver:
    driver = None

    @classmethod
    def Get_driver(cls):
        """获取浏览器驱动（单例模式）"""
        if cls.driver is None:
            options = Options()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            # 使用项目本地的 chromedriver
            driver_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chromedriver.exe")
            service = Service(executable_path=driver_path)

            cls.driver = webdriver.Chrome(service=service, options=options)
            cls.driver.maximize_window()
            cls.driver.implicitly_wait(10)
            cls.driver.get("http://localhost:80/")
        return cls.driver

    @classmethod
    def quit_driver(cls):
        """关闭浏览器"""
        if cls.driver is not None:
            cls.driver.quit()
            cls.driver = None