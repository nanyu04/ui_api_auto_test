"""一键执行：跑全部用例并生成 Allure 报告。

- 用例范围由 pytest.ini 的 testpaths 决定
- Allure 原始结果目录：reports/allure-results
- Allure HTML 报告目录：reports/allure-report
"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent
ALLURE_RESULTS = PROJECT_ROOT / "reports" / "allure-results"
ALLURE_REPORT = PROJECT_ROOT / "reports" / "allure-report"


def main():
    code = pytest.main([])

    try:
        result = subprocess.run(
            ["allure", "generate", str(ALLURE_RESULTS), "-o", str(ALLURE_REPORT), "--clean"],
            check=False,
        )
        if result.returncode == 0:
            print(f"报告已生成：{ALLURE_REPORT / 'index.html'}")
        else:
            print(f"Allure 生成失败，退出码：{result.returncode}")
    except FileNotFoundError:
        print("未找到 allure 命令行，请先安装 Allure 并配置 PATH")

    return code


if __name__ == "__main__":
    sys.exit(main())
