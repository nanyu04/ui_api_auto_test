"""
====================================================
  RuoYi-Vue 接口自动化测试框架 — 全局配置中心
  基于 pydantic-settings，支持多环境 + 环境变量覆盖
====================================================
读取优先级：实例化传参 > 环境变量 > .env 文件 > 默认值
"""
from pathlib import Path
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class GlobalConfig(BaseSettings):
    """全局配置"""

    # -------------------- 项目路径 --------------------
    # 项目根目录（api_automation/config/__init__.py → 上三级）
    ROOT_DIR: Path = Path(__file__).resolve().parents[2]

    # -------------------- 环境选择 --------------------
    ENV: Literal["dev", "test", "staging", "prod"] = "dev"

    # -------------------- 被测服务 --------------------
    # 后端直连地址（application.yml 中 server.port=8081，context-path=/）
    BASE_URL: str = "http://localhost:8081"
    # 如果通过前端 dev-server 代理访问（vue.config.js 的 /dev-api），把这里设为 /dev-api
    API_PREFIX: str = ""
    API_VERSION: str = "v3.9.2"

    # -------------------- 请求默认值 --------------------
    REQUEST_TIMEOUT: int = 15
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    RETRY_MULTIPLIER: float = 2.0

    # -------------------- 鉴权配置 --------------------
    AUTH_TYPE: Literal["bearer", "basic", "apikey"] = "bearer"
    ACCESS_TOKEN: Optional[str] = None
    API_KEY: Optional[str] = None
    API_KEY_HEADER: str = "X-API-Key"

    # -------------------- 测试账号 --------------------
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    # 普通账号（角色 common，用于越权/权限用例；未配置则相关用例自动跳过）
    COMMON_USERNAME: Optional[str] = None
    COMMON_PASSWORD: Optional[str] = None

    # -------------------- 日志配置 --------------------
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "standard"  # standard=人读文本 / json=结构化日志

    # -------------------- 报告配置 --------------------
    # 原始结果与 HTML 报告必须是两个平级目录，不能互相嵌套
    ALLURE_RESULTS_DIR: Path = ROOT_DIR / "reports" / "allure-results"
    ALLURE_REPORT_DIR: Path = ROOT_DIR / "reports" / "allure-report"
    # 兼容旧字段名
    ALLURE_DIR: Path = ALLURE_REPORT_DIR
    REPORT_TITLE: str = "RuoYi-Vue 接口自动化测试报告"

    # -------------------- 数据库（用于落库校验） --------------------
    DB_ENABLED: bool = False
    DB_HOST: Optional[str] = None
    DB_PORT: int = 3306
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: str = "ry-vue"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # -------------------- 派生属性 --------------------
    @property
    def auth_headers(self) -> dict:
        """由配置生成的默认鉴权请求头"""
        headers = {}
        if self.AUTH_TYPE == "bearer" and self.ACCESS_TOKEN:
            headers["Authorization"] = f"Bearer {self.ACCESS_TOKEN}"
        elif self.AUTH_TYPE == "apikey" and self.API_KEY:
            headers[self.API_KEY_HEADER] = self.API_KEY
        return headers

    @property
    def api_base(self) -> str:
        """BASE_URL + API_PREFIX 拼接后的根地址"""
        base = self.BASE_URL.rstrip("/")
        prefix = self.API_PREFIX.strip("/")
        return f"{base}/{prefix}" if prefix else base


# 全局唯一配置实例
settings = GlobalConfig()
