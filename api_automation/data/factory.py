"""
【数据工厂】 — RuoYi-Vue 业务测试数据生成

字段与约束均对齐后端实体（校验规则来自 getter 注解）：
  用户名 ≤30 / 昵称 ≤30 / 手机号 ≤11 / 邮箱 ≤50 且格式合法
  字典类型必须满足 ^[a-z][a-z0-9_]*$

唯一性策略：用户名交给 framework 的 context.tag() 打前缀（前缀 8 字符 + 下划线），
手机号与邮箱由工厂自带随机后缀保证唯一 —— 因为后端对三者都做了唯一性校验。
"""
import random
import uuid
from typing import Any, List, Optional

from faker import Faker

_faker = Faker(locale="zh_CN")


def _sn(n: int = 6) -> str:
    """短随机串"""
    return uuid.uuid4().hex[:n]


def _phone() -> str:
    """11 位手机号（后端 phonenumber 长度上限 11 且唯一）"""
    return "1" + "".join(random.choice("0123456789") for _ in range(10))


class DataFactory:
    """RuoYi-Vue 测试数据工厂"""

    # ========== 用户 ==========
    @staticmethod
    def sys_user(user_name: Optional[str] = None, **overrides: Any) -> dict:
        data = {
            "userName": user_name or f"ry_{_sn(6)}",
            "nickName": f"自动化用户{_sn(4)}",
            "password": "admin123",
            "deptId": 103,
            "email": f"auto_{_sn(8)}@test.com",
            "phonenumber": _phone(),
            "sex": "0",
            "status": "0",
            "roleIds": [],
            "postIds": [],
            "remark": "接口自动化创建",
        }
        data.update(overrides)
        return data

    # ========== 菜单 ==========
    @staticmethod
    def sys_menu(**overrides: Any) -> dict:
        data = {
            "menuName": f"自动化菜单{_sn(4)}",
            "parentId": 0,
            "orderNum": 1,
            "path": f"auto_{_sn(4)}",
            "component": "",
            "query": "",
            "isFrame": "1",
            "isCache": "0",
            "menuType": "C",
            "visible": "0",
            "status": "0",
            "perms": "",
            "icon": "#",
            "remark": "接口自动化创建",
        }
        data.update(overrides)
        return data

    # ========== 角色 ==========
    @staticmethod
    def sys_role(role_name: Optional[str] = None, role_key: Optional[str] = None, **overrides: Any) -> dict:
        data = {
            "roleName": role_name or f"自动化角色{_sn(4)}",
            "roleKey": role_key or f"auto_{_sn(6)}",
            "roleSort": 1,
            "status": "0",
            "remark": "接口自动化创建",
            "menuIds": [],
        }
        data.update(overrides)
        return data

    # ========== 部门 ==========
    @staticmethod
    def sys_dept(parent_id: int = 103, **overrides: Any) -> dict:
        data = {
            "deptName": f"自动化部门{_sn(4)}",
            "parentId": parent_id,
            "orderNum": 1,
            "leader": "ry",
            "phone": _phone(),
            "email": f"dept_{_sn(6)}@test.com",
            "status": "0",
        }
        data.update(overrides)
        return data

    # ========== 岗位 ==========
    @staticmethod
    def sys_post(**overrides: Any) -> dict:
        data = {
            "postCode": f"auto_{_sn(4)}",
            "postName": f"自动化岗位{_sn(4)}",
            "postSort": 1,
            "status": "0",
            "remark": "接口自动化创建",
        }
        data.update(overrides)
        return data

    # ========== 字典类型 ==========
    @staticmethod
    def sys_dict_type(**overrides: Any) -> dict:
        data = {
            "dictName": f"自动化字典{_sn(4)}",
            "dictType": f"auto_dict_{_sn(4)}",
            "status": "0",
            "remark": "接口自动化创建",
        }
        data.update(overrides)
        return data

    # ========== 字典数据 ==========
    @staticmethod
    def sys_dict_data(dict_type: str, **overrides: Any) -> dict:
        data = {
            "dictLabel": f"自动化标签{_sn(4)}",
            "dictValue": _sn(4),
            "dictType": dict_type,
            "dictSort": 1,
            "cssClass": "",
            "listClass": "default",
            "isDefault": "N",
            "status": "0",
            "remark": "接口自动化创建",
        }
        data.update(overrides)
        return data

    # ========== 参数配置 ==========
    @staticmethod
    def sys_config(**overrides: Any) -> dict:
        data = {
            "configName": f"自动化参数{_sn(4)}",
            "configKey": f"auto.config.{_sn(4)}",
            "configValue": "1",
            "configType": "N",
            "remark": "接口自动化创建",
        }
        data.update(overrides)
        return data

    # ========== 通知公告 ==========
    @staticmethod
    def sys_notice(**overrides: Any) -> dict:
        data = {
            "noticeTitle": f"自动化公告{_sn(4)}",
            "noticeType": "1",
            "noticeContent": "接口自动化创建的公告内容",
            "status": "0",
        }
        data.update(overrides)
        return data

    # ========== 定时任务 ==========
    @staticmethod
    def sys_job(**overrides: Any) -> dict:
        data = {
            "jobName": f"自动化任务{_sn(4)}",
            "jobGroup": "DEFAULT",
            "invokeTarget": "ryTask.ryNoParams",
            "cronExpression": "0/30 * * * * ?",
            "misfirePolicy": "1",
            "concurrent": "1",
            "status": "1",
        }
        data.update(overrides)
        return data

    # ========== 常用"非法值"构造 ==========
    @staticmethod
    def overlong(length: int, char: str = "a") -> str:
        """超长字符串（用于边界值用例）"""
        return char * length

    @staticmethod
    def xss_payload() -> str:
        """XSS 注入载荷（后端 @Xss 应拦截）"""
        return "<script>alert(1)</script>"

    @staticmethod
    def invalid_email() -> str:
        return "not-an-email"

    @staticmethod
    def random_id() -> int:
        """几乎不可能存在的 ID（用于"操作不存在的资源"用例）"""
        return 99999999 + random.randint(0, 9999)


# 全局工厂实例
factory = DataFactory()

__all__ = ["DataFactory", "factory", "_phone", "_sn"]
