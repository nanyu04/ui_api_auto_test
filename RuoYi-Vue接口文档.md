# 若依（RuoYi-Vue）后台管理系统 · 完整接口文档

> **被测系统**：RuoYi-Vue 若依后台管理系统（SpringBoot + Vue 前后端分离版）
>
> **源码位置**：`D:\自动化测试\RuoYi-Vue`
>
> **文档来源**：依据后端源码（Controller 接口 / Domain 实体注解 / 数据库建表 SQL）整理生成
>
> **接口总数**：147 个，覆盖 24 个功能模块

---

## 一、系统功能说明

### 1.1 系统管理

| 模块 | 介绍 |
| ---- | ---- |
| 用户管理 | 系统用户的查询、新增、修改、删除、停用、重置密码、分配角色、导入导出 |
| 角色管理 | 角色的查询、新增、修改、删除、数据权限分配、分配用户、停用 |
| 菜单管理 | 系统菜单/按钮权限的查询、新增、修改、删除、排序 |
| 部门管理 | 树形组织机构的查询、新增、修改、删除、排序 |
| 岗位管理 | 岗位的查询、新增、修改、删除、导出 |
| 字典类型 | 字典类型的查询、新增、修改、删除、刷新缓存 |
| 字典数据 | 字典数据的查询、新增、修改、删除、按类型查询 |
| 参数设置 | 系统参数的查询、新增、修改、删除、按键名取值、刷新缓存 |
| 通知公告 | 公告的查询、新增、修改、删除、置顶、已读标记、已读用户查询 |
| 个人信息 | 查看个人资料、修改资料、修改密码、上传头像 |

### 1.2 系统监控

| 模块 | 介绍 |
| ---- | ---- |
| 在线用户 | 查询当前在线会话、强制退出指定用户 |
| 定时任务 | 任务的查询、新增、修改、删除、启停、立即执行一次、导出 |
| 调度日志 | 任务执行日志的查询、删除、清空、导出 |
| 缓存监控 | Redis 基本信息、缓存名称/键名/内容查询、缓存清理 |
| 服务监控 | CPU、内存、JVM、磁盘、服务器信息 |
| 操作日志 | 系统操作记录的查询、删除、清空、导出 |
| 登录日志 | 登录记录的查询、解锁、删除、清空、导出 |

### 1.3 系统工具

| 模块 | 介绍 |
| ---- | ---- |
| 代码生成 | 导入数据库表、编辑生成配置、预览/生成/下载代码、同步表结构 |
| 系统接口 | 系统对外提供的通用接口（文件上传下载、验证码） |

---

## 二、通用说明

| 项 | 说明 |
| ---- | ---- |
| 基础 URL | `http://localhost:8080`（默认端口，可通过 `application.yml` 的 `server.port` 修改） |
| 请求方式 | 以 `application/json` 为主，文件上传使用 `multipart/form-data` |
| 身份验证 | 登录后返回 `token`，后续请求放在请求头 `Authorization: Bearer {token}` 中 |
| 分页参数 | `pageNum`（页码，从 1 开始）、`pageSize`（每页条数）、`orderByColumn`、`isAsc` |
| 列表返回格式 | `TableDataInfo`：`{ total, rows, code, msg }` |
| 通用返回格式 | `AjaxResult`：`{ code, msg, data }` |
| R 返回格式 | `{ code, msg, data }`（`/test/user` 演示接口使用） |
| 成功状态码 | `code = 200` |
| 异常状态码 | `code = 401`（未认证/token 失效）、`403`（无访问权限）、`500`（系统异常） |
| 权限控制 | 接口通过 `@PreAuthorize` 校验权限标识（文档中「权限标识」一栏），无权限返回 403 |
| Swagger 文档 | 启动服务后访问 `http://localhost:8080/swagger-ui.html` 查看在线接口文档 |

---

## 三、数据库设计

库名：`ry-vue`（默认），共 20 张业务表（另有 Quartz 调度依赖的 `qrtz_*` 表见 `sql/quartz.sql`，业务不直接使用）。

### 3.1 部门表（`sys_dept`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| dept_id | bigint(20) | 是 | 部门id |
| parent_id | bigint(20) | 否 | 父部门id |
| ancestors | varchar(50) | 否 | 祖级列表 |
| dept_name | varchar(30) | 否 | 部门名称 |
| order_num | int(4) | 否 | 显示顺序 |
| leader | varchar(20) | 否 | 负责人 |
| phone | varchar(11) | 否 | 联系电话 |
| email | varchar(50) | 否 | 邮箱 |
| status | char(1) | 否 | 部门状态（0正常 1停用） |
| del_flag | char(1) | 否 | 删除标志（0代表存在 2代表删除） |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |

### 3.2 用户信息表（`sys_user`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| user_id | bigint(20) | 是 | 用户ID |
| dept_id | bigint(20) | 否 | 部门ID |
| user_name | varchar(30) | 是 | 用户账号 |
| nick_name | varchar(30) | 是 | 用户昵称 |
| user_type | varchar(2) | 否 | 用户类型（00系统用户） |
| email | varchar(50) | 否 | 用户邮箱 |
| phonenumber | varchar(11) | 否 | 手机号码 |
| sex | char(1) | 否 | 用户性别（0男 1女 2未知） |
| avatar | varchar(100) | 否 | 头像地址 |
| password | varchar(100) | 否 | 密码 |
| status | char(1) | 否 | 账号状态（0正常 1停用） |
| del_flag | char(1) | 否 | 删除标志（0代表存在 2代表删除） |
| login_ip | varchar(128) | 否 | 最后登录IP |
| login_date | datetime | 否 | 最后登录时间 |
| pwd_update_date | datetime | 否 | 密码最后更新时间 |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |
| remark | varchar(500) | 否 | 备注 |

### 3.3 岗位信息表（`sys_post`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| post_id | bigint(20) | 是 | 岗位ID |
| post_code | varchar(64) | 是 | 岗位编码 |
| post_name | varchar(50) | 是 | 岗位名称 |
| post_sort | int(4) | 是 | 显示顺序 |
| status | char(1) | 是 | 状态（0正常 1停用） |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |
| remark | varchar(500) | 否 | 备注 |

### 3.4 角色信息表（`sys_role`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| role_id | bigint(20) | 是 | 角色ID |
| role_name | varchar(30) | 是 | 角色名称 |
| role_key | varchar(100) | 是 | 角色权限字符串 |
| role_sort | int(4) | 是 | 显示顺序 |
| data_scope | char(1) | 否 | 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限） |
| menu_check_strictly | tinyint(1) | 否 | 菜单树选择项是否关联显示 |
| dept_check_strictly | tinyint(1) | 否 | 部门树选择项是否关联显示 |
| status | char(1) | 是 | 角色状态（0正常 1停用） |
| del_flag | char(1) | 否 | 删除标志（0代表存在 2代表删除） |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |
| remark | varchar(500) | 否 | 备注 |

### 3.5 菜单权限表（`sys_menu`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| menu_id | bigint(20) | 是 | 菜单ID |
| menu_name | varchar(50) | 是 | 菜单名称 |
| parent_id | bigint(20) | 否 | 父菜单ID |
| order_num | int(4) | 否 | 显示顺序 |
| path | varchar(200) | 否 | 路由地址 |
| component | varchar(255) | 否 | 组件路径 |
| query | varchar(255) | 否 | 路由参数 |
| route_name | varchar(50) | 否 | 路由名称 |
| is_frame | int(1) | 否 | 是否为外链（0是 1否） |
| is_cache | int(1) | 否 | 是否缓存（0缓存 1不缓存） |
| menu_type | char(1) | 否 | 菜单类型（M目录 C菜单 F按钮） |
| visible | char(1) | 否 | 菜单状态（0显示 1隐藏） |
| status | char(1) | 否 | 菜单状态（0正常 1停用） |
| perms | varchar(100) | 否 | 权限标识 |
| icon | varchar(100) | 否 | 菜单图标 |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |
| remark | varchar(500) | 否 | 备注 |

### 3.6 用户和角色关联表（`sys_user_role`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| user_id | bigint(20) | 是 | 用户ID |
| role_id | bigint(20) | 是 | 角色ID |

### 3.7 角色和菜单关联表（`sys_role_menu`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| role_id | bigint(20) | 是 | 角色ID |
| menu_id | bigint(20) | 是 | 菜单ID |

### 3.8 角色和部门关联表（`sys_role_dept`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| role_id | bigint(20) | 是 | 角色ID |
| dept_id | bigint(20) | 是 | 部门ID |

### 3.9 用户与岗位关联表（`sys_user_post`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| user_id | bigint(20) | 是 | 用户ID |
| post_id | bigint(20) | 是 | 岗位ID |

### 3.10 操作日志记录（`sys_oper_log`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| oper_id | bigint(20) | 是 | 日志主键 |
| title | varchar(50) | 否 | 模块标题 |
| business_type | int(2) | 否 | 业务类型（0其它 1新增 2修改 3删除） |
| method | varchar(200) | 否 | 方法名称 |
| request_method | varchar(10) | 否 | 请求方式 |
| operator_type | int(1) | 否 | 操作类别（0其它 1后台用户 2手机端用户） |
| oper_name | varchar(50) | 否 | 操作人员 |
| dept_name | varchar(50) | 否 | 部门名称 |
| oper_url | varchar(255) | 否 | 请求URL |
| oper_ip | varchar(128) | 否 | 主机地址 |
| oper_location | varchar(255) | 否 | 操作地点 |
| oper_param | varchar(2000) | 否 | 请求参数 |
| json_result | varchar(2000) | 否 | 返回参数 |
| status | int(1) | 否 | 操作状态（0正常 1异常） |
| error_msg | varchar(2000) | 否 | 错误消息 |
| oper_time | datetime | 否 | 操作时间 |
| cost_time | bigint(20) | 否 | 消耗时间 |

### 3.11 字典类型表（`sys_dict_type`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| dict_id | bigint(20) | 是 | 字典主键 |
| dict_name | varchar(100) | 否 | 字典名称 |
| dict_type | varchar(100) | 否 | 字典类型 |
| status | char(1) | 否 | 状态（0正常 1停用） |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |
| remark | varchar(500) | 否 | 备注 |

### 3.12 字典数据表（`sys_dict_data`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| dict_code | bigint(20) | 是 | 字典编码 |
| dict_sort | int(4) | 否 | 字典排序 |
| dict_label | varchar(100) | 否 | 字典标签 |
| dict_value | varchar(100) | 否 | 字典键值 |
| dict_type | varchar(100) | 否 | 字典类型 |
| css_class | varchar(100) | 否 | 样式属性（其他样式扩展） |
| list_class | varchar(100) | 否 | 表格回显样式 |
| is_default | char(1) | 否 | 是否默认（Y是 N否） |
| status | char(1) | 否 | 状态（0正常 1停用） |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |
| remark | varchar(500) | 否 | 备注 |

### 3.13 参数配置表（`sys_config`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| config_id | int(5) | 是 | 参数主键 |
| config_name | varchar(100) | 否 | 参数名称 |
| config_key | varchar(100) | 否 | 参数键名 |
| config_value | varchar(500) | 否 | 参数键值 |
| config_type | char(1) | 否 | 系统内置（Y是 N否） |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |
| remark | varchar(500) | 否 | 备注 |

### 3.14 系统访问记录（`sys_logininfor`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| info_id | bigint(20) | 是 | 访问ID |
| user_name | varchar(50) | 否 | 用户账号 |
| ipaddr | varchar(128) | 否 | 登录IP地址 |
| login_location | varchar(255) | 否 | 登录地点 |
| browser | varchar(50) | 否 | 浏览器类型 |
| os | varchar(50) | 否 | 操作系统 |
| status | char(1) | 否 | 登录状态（0成功 1失败） |
| msg | varchar(255) | 否 | 提示消息 |
| login_time | datetime | 否 | 访问时间 |

### 3.15 定时任务调度表（`sys_job`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| job_id | bigint(20) | 是 | 任务ID |
| job_name | varchar(64) | 否 | 任务名称 |
| job_group | varchar(64) | 否 | 任务组名 |
| invoke_target | varchar(500) | 是 | 调用目标字符串 |
| cron_expression | varchar(255) | 否 | cron执行表达式 |
| misfire_policy | varchar(20) | 否 | 计划执行错误策略（1立即执行 2执行一次 3放弃执行） |
| concurrent | char(1) | 否 | 是否并发执行（0允许 1禁止） |
| status | char(1) | 否 | 状态（0正常 1暂停） |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |
| remark | varchar(500) | 否 | 备注信息 |

### 3.16 定时任务调度日志表（`sys_job_log`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| job_log_id | bigint(20) | 是 | 任务日志ID |
| job_name | varchar(64) | 是 | 任务名称 |
| job_group | varchar(64) | 是 | 任务组名 |
| invoke_target | varchar(500) | 是 | 调用目标字符串 |
| job_message | varchar(500) | 否 | 日志信息 |
| status | char(1) | 否 | 执行状态（0正常 1失败） |
| exception_info | varchar(2000) | 否 | 异常信息 |
| start_time | datetime | 否 | 执行开始时间 |
| end_time | datetime | 否 | 执行结束时间 |
| create_time | datetime | 否 | 创建时间 |

### 3.17 通知公告表（`sys_notice`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| notice_id | int(4) | 是 | 公告ID |
| notice_title | varchar(50) | 是 | 公告标题 |
| notice_type | char(1) | 是 | 公告类型（1通知 2公告） |
| notice_content | longblob | 否 | 公告内容 |
| status | char(1) | 否 | 公告状态（0正常 1关闭） |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |
| remark | varchar(255) | 否 | 备注 |

### 3.18 公告已读记录表（`sys_notice_read`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| read_id | bigint(20) | 是 | 已读主键 |
| notice_id | int(4) | 是 | 公告id |
| user_id | bigint(20) | 是 | 用户id |
| read_time | datetime | 是 | 阅读时间 |

### 3.19 代码生成业务表（`gen_table`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| table_id | bigint(20) | 是 | 编号 |
| table_name | varchar(200) | 否 | 表名称 |
| table_comment | varchar(500) | 否 | 表描述 |
| sub_table_name | varchar(64) | 否 | 关联子表的表名 |
| sub_table_fk_name | varchar(64) | 否 | 子表关联的外键名 |
| class_name | varchar(100) | 否 | 实体类名称 |
| tpl_category | varchar(200) | 否 | 使用的模板（crud单表操作 tree树表操作） |
| tpl_web_type | varchar(30) | 否 | 前端模板类型（element-ui模版 element-plus模版） |
| package_name | varchar(100) | 否 | 生成包路径 |
| module_name | varchar(30) | 否 | 生成模块名 |
| business_name | varchar(30) | 否 | 生成业务名 |
| function_name | varchar(50) | 否 | 生成功能名 |
| function_author | varchar(50) | 否 | 生成功能作者 |
| form_col_num | int(1) | 否 | 表单布局（单列 双列 三列） |
| gen_type | char(1) | 否 | 生成代码方式（0zip压缩包 1自定义路径） |
| gen_path | varchar(200) | 否 | 生成路径（不填默认项目路径） |
| options | varchar(1000) | 否 | 其它生成选项 |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |
| remark | varchar(500) | 否 | 备注 |

### 3.20 代码生成业务表字段（`gen_table_column`）

| 字段名 | 类型 | 是否必填 | 注释 |
| ---- | ---- | ---- | ---- |
| column_id | bigint(20) | 是 | 编号 |
| table_id | bigint(20) | 否 | 归属表编号 |
| column_name | varchar(200) | 否 | 列名称 |
| column_comment | varchar(500) | 否 | 列描述 |
| column_type | varchar(100) | 否 | 列类型 |
| java_type | varchar(500) | 否 | JAVA类型 |
| java_field | varchar(200) | 否 | JAVA字段名 |
| is_pk | char(1) | 否 | 是否主键（1是） |
| is_increment | char(1) | 否 | 是否自增（1是） |
| is_required | char(1) | 否 | 是否必填（1是） |
| is_insert | char(1) | 否 | 是否为插入字段（1是） |
| is_edit | char(1) | 否 | 是否编辑字段（1是） |
| is_list | char(1) | 否 | 是否列表字段（1是） |
| is_query | char(1) | 否 | 是否查询字段（1是） |
| query_type | varchar(200) | 否 | 查询方式（等于、不等于、大于、小于、范围） |
| html_type | varchar(200) | 否 | 显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件） |
| dict_type | varchar(200) | 否 | 字典类型 |
| sort | int | 否 | 排序 |
| create_by | varchar(64) | 否 | 创建者 |
| create_time | datetime | 否 | 创建时间 |
| update_by | varchar(64) | 否 | 更新者 |
| update_time | datetime | 否 | 更新时间 |

---

## 四、接口文档

### 4.1 登录认证与注册

#### 4.1.1 获取验证码

- 接口地址：/captchaImage
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
-（无请求参数，可携带 t 时间戳避免缓存）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "captchaEnabled": true,
    "uuid": "3f2f****-****-****-****",
    "img": "data:image/gif;base64,iVBORw0KGgo..."
}
```

#### 4.1.2 用户登录

- 接口地址：/login
- 请求方式：POST
- 权限标识：无（登录后即可访问）
- 请求参数：
```text
{
    "username": "admin",
    "password": "admin123",
    "code": "0",
    "uuid": "3f2f****-****-****-****"
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "token": "eyJhbGciOiJIUzUxMiJ9.****.****"
}
```

#### 4.1.3 获取当前登录用户信息

- 接口地址：/getInfo
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 无请求参数（从请求头 Authorization 中解析 token）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "user": { ...SysUser 用户对象... },
    "roles": ["admin"],
    "permissions": ["*:*:*"],
    "isDefaultModifyPwd": false,
    "isPasswordExpired": false
}
```

#### 4.1.4 获取当前用户路由菜单

- 接口地址：/getRouters
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": [
        {
            "name": "System",
            "path": "/system",
            "component": "Layout",
            "children": [ { "path": "user", "component": "system/user/index" } ]
        }
    ]
}
```

#### 4.1.5 用户注册

- 接口地址：/register
- 请求方式：POST
- 权限标识：无（登录后即可访问）
- 请求参数：
```text
{
    "username": "ry",
    "nickname": "若依",
    "password": "admin123",
    "confirmPassword": "admin123",
    "code": "0",
    "uuid": "3f2f****-****"
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.1.6 系统首页

- 接口地址：/
- 请求方式：GET/POST 均可
- 权限标识：无（登录后即可访问）
- 请求参数：
- 无请求参数
- 返回参数：
- 返回系统首页 HTML 字符串

#### 4.1.7 解锁屏幕

- 接口地址：/unlockscreen
- 请求方式：POST
- 权限标识：无（登录后即可访问）
- 请求参数：
```text
{
    "password": "admin123"
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

### 4.2 系统管理

#### 4.2.1 查询用户列表

- 接口地址：/system/user/list
- 请求方式：GET
- 权限标识：system:user:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "deptId": null,  // 部门编号
    "userName": null,  // 登录名称
    "phonenumber": null,  // 手机号码
    "status": null  // 账号状态
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "userId": 100,  // 用户序号
            "deptId": 103,  // 部门编号
            "userName": "ry",  // 登录名称
            "nickName": "若依",  // 用户名称
            "email": "ry@163.com",  // 用户邮箱
            "phonenumber": "15888888888",  // 手机号码
            "sex": "0",  // 用户性别
            "status": "0",  // 账号状态
            "loginDate": "2026-10-26 12:00:00",  // 最后登录时间
            "pwdUpdateDate": "2026-10-26 12:00:00",  // 密码最后更新时间
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.2.2 导出用户

- 接口地址：/system/user/export
- 请求方式：POST
- 权限标识：system:user:export
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "deptId": null,  // 部门编号
    "userName": null,  // 登录名称
    "phonenumber": null,  // 手机号码
    "status": null  // 账号状态
}
```
- 返回参数：
- 返回 Excel 文件流（Content-Type: application/vnd.ms-excel）

#### 4.2.3 导入用户数据

- 接口地址：/system/user/importData
- 请求方式：POST
- 权限标识：system:user:import
- 请求参数：
- form-data：
  - file：Excel 文件（必填）
  - updateSupport：是否更新已存在的用户数据（布尔值，可选）
- 返回参数：
```text
{
    "code": 200,
    "msg": "恭喜您，数据已全部导入成功！共 1 条，全部成功。"
}
```

#### 4.2.4 下载用户导入模板

- 接口地址：/system/user/importTemplate
- 请求方式：POST
- 权限标识：无（登录后即可访问）
- 请求参数：
- 无请求参数
- 返回参数：
- 返回 Excel 模板文件流

#### 4.2.5 查询用户详细

- 接口地址：/system/user  或  /system/user/{userId}
- 请求方式：GET
- 权限标识：system:user:query
- 请求参数：
- 路径参数：
  - userId：用户 ID（新增用户时可传 /system/user/ 不带 ID）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": { ...SysUser 用户对象... },
    "roleIds": [2],
    "postIds": [1],
    "roles": [ { ...SysRole 角色对象... } ],
    "posts": [ { ...SysPost 岗位对象... } ]
}
```

#### 4.2.6 新增用户

- 接口地址：/system/user
- 请求方式：POST
- 权限标识：system:user:add
- 请求参数：
```text
{
    "deptId": 103,  // 部门编号
    "userName": "ry",  // 登录名称
    "nickName": "若依",  // 用户名称
    "email": "ry@163.com",  // 用户邮箱
    "phonenumber": "15888888888",  // 手机号码
    "sex": "0",  // 用户性别
    "password": "admin123",  // 密码
    "status": "0",  // 账号状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.7 修改用户

- 接口地址：/system/user
- 请求方式：PUT
- 权限标识：system:user:edit
- 请求参数：
```text
{
    "userId": 100,  // 用户序号
    "deptId": 103,  // 部门编号
    "userName": "ry",  // 登录名称
    "nickName": "若依",  // 用户名称
    "email": "ry@163.com",  // 用户邮箱
    "phonenumber": "15888888888",  // 手机号码
    "sex": "0",  // 用户性别
    "password": "admin123",  // 密码
    "status": "0",  // 账号状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.8 删除用户

- 接口地址：/system/user/{userIds}
- 请求方式：DELETE
- 权限标识：system:user:remove
- 请求参数：
- 路径参数：
  - userIds：用户ID（多个用英文逗号分隔）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.9 重置用户密码

- 接口地址：/system/user/resetPwd
- 请求方式：PUT
- 权限标识：system:user:resetPwd
- 请求参数：
```text
{
    "userId": 100,
    "password": "admin123"
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.10 修改用户状态

- 接口地址：/system/user/changeStatus
- 请求方式：PUT
- 权限标识：system:user:edit
- 请求参数：
```text
{
    "userId": 100,
    "status": "0"
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.11 查询用户已分配角色

- 接口地址：/system/user/authRole/{userId}
- 请求方式：GET
- 权限标识：system:user:query
- 请求参数：
- 路径参数：userId 用户 ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "user": { ...SysUser 用户对象... },
    "roles": [ { "roleId": 2, "roleName": "普通角色", "flag": true } ]
}
```

#### 4.2.12 给用户分配角色

- 接口地址：/system/user/authRole
- 请求方式：PUT
- 权限标识：system:user:edit
- 请求参数：
- 查询参数：
  - userId：用户 ID（必填）
  - roleIds：角色 ID 数组（必填）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.13 获取部门树数据

- 接口地址：/system/user/deptTree
- 请求方式：GET
- 权限标识：system:user:list
- 请求参数：
- 查询参数：
  - deptName：部门名称（模糊查询，可选）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": [ { "id": 100, "label": "若依科技", "children": [] } ]
}
```

#### 4.2.14 查询角色列表

- 接口地址：/system/role/list
- 请求方式：GET
- 权限标识：system:role:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "roleName": null,  // 角色名称
    "roleKey": null,  // 角色权限
    "status": null  // 角色状态
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "roleName": "普通角色",  // 角色名称
            "roleKey": "common",  // 角色权限
            "roleSort": 2,  // 角色排序
            "dataScope": "1",  // 数据范围
            "status": "0",  // 角色状态
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.2.15 导出角色

- 接口地址：/system/role/export
- 请求方式：POST
- 权限标识：system:role:export
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "roleName": null,  // 角色名称
    "roleKey": null,  // 角色权限
    "status": null  // 角色状态
}
```
- 返回参数：
- 返回 Excel 文件流（Content-Type: application/vnd.ms-excel）

#### 4.2.16 查询角色详细

- 接口地址：/system/role/{roleId}
- 请求方式：GET
- 权限标识：system:role:query
- 请求参数：
- 路径参数：
  - roleId：角色ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "roleName": "普通角色",  // 角色名称
        "roleKey": "common",  // 角色权限
        "roleSort": 2,  // 角色排序
        "dataScope": "1",  // 数据范围
        "status": "0",  // 角色状态
        "createBy": "字符串",  // 创建者
        "createTime": "2026-10-26 12:00:00",  // 创建时间
        "updateBy": "字符串",  // 更新者
        "updateTime": "2026-10-26 12:00:00",  // 更新时间
        "remark":   // 备注
    }
}
```

#### 4.2.17 新增角色

- 接口地址：/system/role
- 请求方式：POST
- 权限标识：system:role:add
- 请求参数：
```text
{
    "roleName": "普通角色",  // 角色名称
    "roleKey": "common",  // 角色权限
    "roleSort": 2,  // 角色排序
    "dataScope": "1",  // 数据范围
    "status": "0",  // 角色状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.18 修改角色

- 接口地址：/system/role
- 请求方式：PUT
- 权限标识：system:role:edit
- 请求参数：
```text
{
    "roleName": "普通角色",  // 角色名称
    "roleKey": "common",  // 角色权限
    "roleSort": 2,  // 角色排序
    "dataScope": "1",  // 数据范围
    "status": "0",  // 角色状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.19 修改角色数据权限

- 接口地址：/system/role/dataScope
- 请求方式：PUT
- 权限标识：system:role:edit
- 请求参数：
```text
{
    "roleId": 2,
    "dataScope": "1",
    "deptIds": [103, 104, 105]
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.20 修改角色状态

- 接口地址：/system/role/changeStatus
- 请求方式：PUT
- 权限标识：system:role:edit
- 请求参数：
```text
{
    "roleId": 2,
    "status": "0"
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.21 删除角色

- 接口地址：/system/role/{roleIds}
- 请求方式：DELETE
- 权限标识：system:role:remove
- 请求参数：
- 路径参数：
  - roleIds：参数（多个用英文逗号分隔）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.22 获取角色下拉选项

- 接口地址：/system/role/optionselect
- 请求方式：GET
- 权限标识：system:role:query
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": [
        { "id": 1, "label": "若依" }
    ]
}
```

#### 4.2.23 查询已分配用户

- 接口地址：/system/role/authUser/allocatedList
- 请求方式：GET
- 权限标识：system:role:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "roleName": null,  // 角色名称
    "roleKey": null,  // 角色权限
    "status": null  // 角色状态
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "roleName": "普通角色",  // 角色名称
            "roleKey": "common",  // 角色权限
            "roleSort": 2,  // 角色排序
            "dataScope": "1",  // 数据范围
            "status": "0",  // 角色状态
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.2.24 查询未分配用户

- 接口地址：/system/role/authUser/unallocatedList
- 请求方式：GET
- 权限标识：system:role:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "roleName": null,  // 角色名称
    "roleKey": null,  // 角色权限
    "status": null  // 角色状态
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "roleName": "普通角色",  // 角色名称
            "roleKey": "common",  // 角色权限
            "roleSort": 2,  // 角色排序
            "dataScope": "1",  // 数据范围
            "status": "0",  // 角色状态
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.2.25 取消用户授权

- 接口地址：/system/role/authUser/cancel
- 请求方式：PUT
- 权限标识：system:role:edit
- 请求参数：
```text
{
    "roleName": "普通角色",  // 角色名称
    "roleKey": "common",  // 角色权限
    "roleSort": 2,  // 角色排序
    "dataScope": "1",  // 数据范围
    "status": "0",  // 角色状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.26 批量取消用户授权

- 接口地址：/system/role/authUser/cancelAll
- 请求方式：PUT
- 权限标识：system:role:edit
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.27 批量授权用户

- 接口地址：/system/role/authUser/selectAll
- 请求方式：PUT
- 权限标识：system:role:edit
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.28 获取角色关联部门树

- 接口地址：/system/role/deptTree/{roleId}
- 请求方式：GET
- 权限标识：system:role:query
- 请求参数：
- 路径参数：roleId 角色 ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "depts": [ { "id": 100, "label": "若依科技", "children": [] } ],
    "checkedKeys": [103]
}
```

#### 4.2.29 查询菜单列表

- 接口地址：/system/menu/list
- 请求方式：GET
- 权限标识：system:menu:list
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.30 查询菜单详细

- 接口地址：/system/menu/{menuId}
- 请求方式：GET
- 权限标识：system:menu:query
- 请求参数：
- 路径参数：
  - menuId：菜单ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "menuId": 1001,  // 菜单ID
        "menuName": "系统管理",  // 菜单名称
        "parentName": "字符串",
        "parentId": 0,  // 父部门id
        "orderNum": 1,  // 显示顺序
        "path": "system",  // 路由地址
        "component": "system/user/index",  // 组件路径
        "query": "",  // 路由参数
        "routeName": "",  // 路由名称
        "isFrame": "1",  // 是否为外链（0是 1否）
        "isCache": "0",  // 是否缓存（0缓存 1不缓存）
        "menuType": "M",  // 菜单类型（M目录 C菜单 F按钮）
        "visible": "0",  // 菜单状态（0显示 1隐藏）
        "status": "0",  // 部门状态（0正常 1停用）
        "perms": "system:user:list",  // 权限标识
        "icon": "system",  // 菜单图标
        "createBy": "字符串",  // 创建者
        "createTime": "2026-10-26 12:00:00",  // 创建时间
        "updateBy": "字符串",  // 更新者
        "updateTime": "2026-10-26 12:00:00",  // 更新时间
        "remark":   // 备注
    }
}
```

#### 4.2.31 获取菜单下拉树

- 接口地址：/system/menu/treeselect
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 查询参数：
  - menuName：菜单名称（模糊查询，可选）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": [ { "id": 1, "label": "系统管理", "children": [] } ]
}
```

#### 4.2.32 获取角色菜单树

- 接口地址：/system/menu/roleMenuTreeselect/{roleId}
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 路径参数：roleId 角色 ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "menus": [ { "id": 1, "label": "系统管理", "children": [] } ],
    "checkedKeys": [1001, 1002]
}
```

#### 4.2.33 新增菜单

- 接口地址：/system/menu
- 请求方式：POST
- 权限标识：system:menu:add
- 请求参数：
```text
{
    "menuName": "系统管理",  // 菜单名称
    "parentId": 0,  // 父部门id
    "orderNum": 1,  // 显示顺序
    "path": "system",  // 路由地址
    "component": "system/user/index",  // 组件路径
    "query": "",  // 路由参数
    "routeName": "",  // 路由名称
    "isFrame": "1",  // 是否为外链（0是 1否）
    "isCache": "0",  // 是否缓存（0缓存 1不缓存）
    "menuType": "M",  // 菜单类型（M目录 C菜单 F按钮）
    "visible": "0",  // 菜单状态（0显示 1隐藏）
    "status": "0",  // 部门状态（0正常 1停用）
    "perms": "system:user:list",  // 权限标识
    "icon": "system",  // 菜单图标
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.34 修改菜单

- 接口地址：/system/menu
- 请求方式：PUT
- 权限标识：system:menu:edit
- 请求参数：
```text
{
    "menuId": 1001,  // 菜单ID
    "menuName": "系统管理",  // 菜单名称
    "parentId": 0,  // 父部门id
    "orderNum": 1,  // 显示顺序
    "path": "system",  // 路由地址
    "component": "system/user/index",  // 组件路径
    "query": "",  // 路由参数
    "routeName": "",  // 路由名称
    "isFrame": "1",  // 是否为外链（0是 1否）
    "isCache": "0",  // 是否缓存（0缓存 1不缓存）
    "menuType": "M",  // 菜单类型（M目录 C菜单 F按钮）
    "visible": "0",  // 菜单状态（0显示 1隐藏）
    "status": "0",  // 部门状态（0正常 1停用）
    "perms": "system:user:list",  // 权限标识
    "icon": "system",  // 菜单图标
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.35 保存菜单排序

- 接口地址：/system/menu/updateSort
- 请求方式：PUT
- 权限标识：system:menu:edit
- 请求参数：
```text
{
    "menuIds": "1001,1002",
    "orderNum": "1"
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.36 删除菜单

- 接口地址：/system/menu/{menuId}
- 请求方式：DELETE
- 权限标识：system:menu:remove
- 请求参数：
- 路径参数：
  - menuId：菜单ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.37 查询部门列表

- 接口地址：/system/dept/list
- 请求方式：GET
- 权限标识：system:dept:list
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.38 查询部门列表（排除节点）

- 接口地址：/system/dept/list/exclude/{deptId}
- 请求方式：GET
- 权限标识：system:dept:list
- 请求参数：
- 路径参数：
  - deptId：部门ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.39 查询部门详细

- 接口地址：/system/dept/{deptId}
- 请求方式：GET
- 权限标识：system:dept:query
- 请求参数：
- 路径参数：
  - deptId：部门ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "deptId": 103,  // 部门id
        "parentId": 0,  // 父部门id
        "ancestors": "0,100,101",  // 祖级列表
        "deptName": "研发部门",  // 部门名称
        "orderNum": 1,  // 显示顺序
        "leader": "若依",  // 负责人
        "phone": "15888888888",  // 联系电话
        "email": "ry@163.com",  // 邮箱
        "status": "0",  // 部门状态（0正常 1停用）
        "parentName": "字符串",
        "createBy": "字符串",  // 创建者
        "createTime": "2026-10-26 12:00:00",  // 创建时间
        "updateBy": "字符串",  // 更新者
        "updateTime": "2026-10-26 12:00:00",  // 更新时间
        "remark":   // 备注
    }
}
```

#### 4.2.40 新增部门

- 接口地址：/system/dept
- 请求方式：POST
- 权限标识：system:dept:add
- 请求参数：
```text
{
    "parentId": 0,  // 父部门id
    "ancestors": "0,100,101",  // 祖级列表
    "deptName": "研发部门",  // 部门名称
    "orderNum": 1,  // 显示顺序
    "leader": "若依",  // 负责人
    "phone": "15888888888",  // 联系电话
    "email": "ry@163.com",  // 邮箱
    "status": "0",  // 部门状态（0正常 1停用）
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.41 修改部门

- 接口地址：/system/dept
- 请求方式：PUT
- 权限标识：system:dept:edit
- 请求参数：
```text
{
    "deptId": 103,  // 部门id
    "parentId": 0,  // 父部门id
    "ancestors": "0,100,101",  // 祖级列表
    "deptName": "研发部门",  // 部门名称
    "orderNum": 1,  // 显示顺序
    "leader": "若依",  // 负责人
    "phone": "15888888888",  // 联系电话
    "email": "ry@163.com",  // 邮箱
    "status": "0",  // 部门状态（0正常 1停用）
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.42 保存部门排序

- 接口地址：/system/dept/updateSort
- 请求方式：PUT
- 权限标识：system:dept:edit
- 请求参数：
```text
{
    "menuIds": "1001,1002",
    "orderNum": "1"
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.43 删除部门

- 接口地址：/system/dept/{deptId}
- 请求方式：DELETE
- 权限标识：system:dept:remove
- 请求参数：
- 路径参数：
  - deptId：部门ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.44 查询岗位列表

- 接口地址：/system/post/list
- 请求方式：GET
- 权限标识：system:post:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "postCode": null,  // 岗位编码
    "postName": null,  // 岗位名称
    "status": null  // 状态
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "postId": 1,  // 岗位序号
            "postCode": "ceo",  // 岗位编码
            "postName": "董事长",  // 岗位名称
            "postSort": 1,  // 岗位排序
            "status": "0",  // 状态
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.2.45 导出岗位

- 接口地址：/system/post/export
- 请求方式：POST
- 权限标识：system:post:export
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "postCode": null,  // 岗位编码
    "postName": null,  // 岗位名称
    "status": null  // 状态
}
```
- 返回参数：
- 返回 Excel 文件流（Content-Type: application/vnd.ms-excel）

#### 4.2.46 查询岗位详细

- 接口地址：/system/post/{postId}
- 请求方式：GET
- 权限标识：system:post:query
- 请求参数：
- 路径参数：
  - postId：岗位ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "postId": 1,  // 岗位序号
        "postCode": "ceo",  // 岗位编码
        "postName": "董事长",  // 岗位名称
        "postSort": 1,  // 岗位排序
        "status": "0",  // 状态
        "createBy": "字符串",  // 创建者
        "createTime": "2026-10-26 12:00:00",  // 创建时间
        "updateBy": "字符串",  // 更新者
        "updateTime": "2026-10-26 12:00:00",  // 更新时间
        "remark":   // 备注
    }
}
```

#### 4.2.47 新增岗位

- 接口地址：/system/post
- 请求方式：POST
- 权限标识：system:post:add
- 请求参数：
```text
{
    "postCode": "ceo",  // 岗位编码
    "postName": "董事长",  // 岗位名称
    "postSort": 1,  // 岗位排序
    "status": "0",  // 状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.48 修改岗位

- 接口地址：/system/post
- 请求方式：PUT
- 权限标识：system:post:edit
- 请求参数：
```text
{
    "postId": 1,  // 岗位序号
    "postCode": "ceo",  // 岗位编码
    "postName": "董事长",  // 岗位名称
    "postSort": 1,  // 岗位排序
    "status": "0",  // 状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.49 删除岗位

- 接口地址：/system/post/{postIds}
- 请求方式：DELETE
- 权限标识：system:post:remove
- 请求参数：
- 路径参数：
  - postIds：参数（多个用英文逗号分隔）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.50 获取岗位下拉选项

- 接口地址：/system/post/optionselect
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": [
        { "id": 1, "label": "若依" }
    ]
}
```

#### 4.2.51 查询字典类型列表

- 接口地址：/system/dict/type/list
- 请求方式：GET
- 权限标识：system:dict:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "dictName": null,  // 字典名称
    "dictType": null,  // 字典类型
    "status": null  // 状态
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "dictId": 1,  // 字典主键
            "dictName": "用户性别",  // 字典名称
            "dictType": "sys_user_sex",  // 字典类型
            "status": "0",  // 状态
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.2.52 导出字典类型

- 接口地址：/system/dict/type/export
- 请求方式：POST
- 权限标识：system:dict:export
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "dictName": null,  // 字典名称
    "dictType": null,  // 字典类型
    "status": null  // 状态
}
```
- 返回参数：
- 返回 Excel 文件流（Content-Type: application/vnd.ms-excel）

#### 4.2.53 查询字典类型详细

- 接口地址：/system/dict/type/{dictId}
- 请求方式：GET
- 权限标识：system:dict:query
- 请求参数：
- 路径参数：
  - dictId：字典类型ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "dictId": 1,  // 字典主键
        "dictName": "用户性别",  // 字典名称
        "dictType": "sys_user_sex",  // 字典类型
        "status": "0",  // 状态
        "createBy": "字符串",  // 创建者
        "createTime": "2026-10-26 12:00:00",  // 创建时间
        "updateBy": "字符串",  // 更新者
        "updateTime": "2026-10-26 12:00:00",  // 更新时间
        "remark":   // 备注
    }
}
```

#### 4.2.54 新增字典类型

- 接口地址：/system/dict/type
- 请求方式：POST
- 权限标识：system:dict:add
- 请求参数：
```text
{
    "dictName": "用户性别",  // 字典名称
    "dictType": "sys_user_sex",  // 字典类型
    "status": "0",  // 状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.55 修改字典类型

- 接口地址：/system/dict/type
- 请求方式：PUT
- 权限标识：system:dict:edit
- 请求参数：
```text
{
    "dictId": 1,  // 字典主键
    "dictName": "用户性别",  // 字典名称
    "dictType": "sys_user_sex",  // 字典类型
    "status": "0",  // 状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.56 删除字典类型

- 接口地址：/system/dict/type/{dictIds}
- 请求方式：DELETE
- 权限标识：system:dict:remove
- 请求参数：
- 路径参数：
  - dictIds：字典类型ID（多个用英文逗号分隔）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.57 刷新字典缓存

- 接口地址：/system/dict/type/refreshCache
- 请求方式：DELETE
- 权限标识：system:dict:remove
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.58 获取字典类型下拉选项

- 接口地址：/system/dict/type/optionselect
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": [
        { "id": 1, "label": "若依" }
    ]
}
```

#### 4.2.59 查询字典数据列表

- 接口地址：/system/dict/data/list
- 请求方式：GET
- 权限标识：system:dict:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "dictLabel": null,  // 字典标签
    "dictType": null,  // 字典类型
    "status": null  // 状态
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "dictCode": 1,  // 字典编码
            "dictSort": 1,  // 字典排序
            "dictLabel": "男",  // 字典标签
            "dictValue": "0",  // 字典键值
            "dictType": "sys_user_sex",  // 字典类型
            "cssClass": "",  // 样式属性（其他样式扩展）
            "listClass": "default",  // 表格回显样式
            "isDefault": "Y",  // 是否默认
            "status": "0",  // 状态
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.2.60 导出字典数据

- 接口地址：/system/dict/data/export
- 请求方式：POST
- 权限标识：system:dict:export
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "dictLabel": null,  // 字典标签
    "dictType": null,  // 字典类型
    "status": null  // 状态
}
```
- 返回参数：
- 返回 Excel 文件流（Content-Type: application/vnd.ms-excel）

#### 4.2.61 查询字典数据详细

- 接口地址：/system/dict/data/{dictCode}
- 请求方式：GET
- 权限标识：system:dict:query
- 请求参数：
- 路径参数：
  - dictCode：字典数据ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "dictCode": 1,  // 字典编码
        "dictSort": 1,  // 字典排序
        "dictLabel": "男",  // 字典标签
        "dictValue": "0",  // 字典键值
        "dictType": "sys_user_sex",  // 字典类型
        "cssClass": "",  // 样式属性（其他样式扩展）
        "listClass": "default",  // 表格回显样式
        "isDefault": "Y",  // 是否默认
        "status": "0",  // 状态
        "createBy": "字符串",  // 创建者
        "createTime": "2026-10-26 12:00:00",  // 创建时间
        "updateBy": "字符串",  // 更新者
        "updateTime": "2026-10-26 12:00:00",  // 更新时间
        "remark":   // 备注
    }
}
```

#### 4.2.62 根据字典类型查询字典数据

- 接口地址：/system/dict/data/type/{dictType}
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 路径参数：dictType 字典类型
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": [ { "dictLabel": "男", "dictValue": "0", "dictSort": 1 } ]
}
```

#### 4.2.63 新增字典数据

- 接口地址：/system/dict/data
- 请求方式：POST
- 权限标识：system:dict:add
- 请求参数：
```text
{
    "dictSort": 1,  // 字典排序
    "dictLabel": "男",  // 字典标签
    "dictValue": "0",  // 字典键值
    "dictType": "sys_user_sex",  // 字典类型
    "cssClass": "",  // 样式属性（其他样式扩展）
    "listClass": "default",  // 表格回显样式
    "isDefault": "Y",  // 是否默认
    "status": "0",  // 状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.64 修改字典数据

- 接口地址：/system/dict/data
- 请求方式：PUT
- 权限标识：system:dict:edit
- 请求参数：
```text
{
    "dictCode": 1,  // 字典编码
    "dictSort": 1,  // 字典排序
    "dictLabel": "男",  // 字典标签
    "dictValue": "0",  // 字典键值
    "dictType": "sys_user_sex",  // 字典类型
    "cssClass": "",  // 样式属性（其他样式扩展）
    "listClass": "default",  // 表格回显样式
    "isDefault": "Y",  // 是否默认
    "status": "0",  // 状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.65 删除字典数据

- 接口地址：/system/dict/data/{dictCodes}
- 请求方式：DELETE
- 权限标识：system:dict:remove
- 请求参数：
- 路径参数：
  - dictCodes：参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.66 查询参数列表

- 接口地址：/system/config/list
- 请求方式：GET
- 权限标识：system:config:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "configName": null,  // 参数名称
    "configKey": null,  // 参数键名
    "configType": null  // 系统内置
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "configId": 1,  // 参数主键
            "configName": "主框架页-默认皮肤样式名称",  // 参数名称
            "configKey": "sys.index.skinName",  // 参数键名
            "configValue": "skin-blue",  // 参数键值
            "configType": "Y",  // 系统内置
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.2.67 导出参数

- 接口地址：/system/config/export
- 请求方式：POST
- 权限标识：system:config:export
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "configName": null,  // 参数名称
    "configKey": null,  // 参数键名
    "configType": null  // 系统内置
}
```
- 返回参数：
- 返回 Excel 文件流（Content-Type: application/vnd.ms-excel）

#### 4.2.68 查询参数详细

- 接口地址：/system/config/{configId}
- 请求方式：GET
- 权限标识：system:config:query
- 请求参数：
- 路径参数：
  - configId：参数主键
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "configId": 1,  // 参数主键
        "configName": "主框架页-默认皮肤样式名称",  // 参数名称
        "configKey": "sys.index.skinName",  // 参数键名
        "configValue": "skin-blue",  // 参数键值
        "configType": "Y",  // 系统内置
        "createBy": "字符串",  // 创建者
        "createTime": "2026-10-26 12:00:00",  // 创建时间
        "updateBy": "字符串",  // 更新者
        "updateTime": "2026-10-26 12:00:00",  // 更新时间
        "remark":   // 备注
    }
}
```

#### 4.2.69 根据参数键名查询参数值

- 接口地址：/system/config/configKey/{configKey}
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 路径参数：configKey 参数键名
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": "skin-blue"
}
```

#### 4.2.70 新增参数

- 接口地址：/system/config
- 请求方式：POST
- 权限标识：system:config:add
- 请求参数：
```text
{
    "configName": "主框架页-默认皮肤样式名称",  // 参数名称
    "configKey": "sys.index.skinName",  // 参数键名
    "configValue": "skin-blue",  // 参数键值
    "configType": "Y",  // 系统内置
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.71 修改参数

- 接口地址：/system/config
- 请求方式：PUT
- 权限标识：system:config:edit
- 请求参数：
```text
{
    "configId": 1,  // 参数主键
    "configName": "主框架页-默认皮肤样式名称",  // 参数名称
    "configKey": "sys.index.skinName",  // 参数键名
    "configValue": "skin-blue",  // 参数键值
    "configType": "Y",  // 系统内置
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.72 删除参数

- 接口地址：/system/config/{configIds}
- 请求方式：DELETE
- 权限标识：system:config:remove
- 请求参数：
- 路径参数：
  - configIds：参数ID（多个用英文逗号分隔）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.73 刷新参数缓存

- 接口地址：/system/config/refreshCache
- 请求方式：DELETE
- 权限标识：system:config:remove
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.74 查询公告列表

- 接口地址：/system/notice/list
- 请求方式：GET
- 权限标识：system:notice:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "noticeTitle": null,  // 公告标题
    "noticeType": null,  // 公告类型（1通知 2公告）
    "createBy": null  // 创建者
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "noticeId": 1,  // 公告ID
            "noticeTitle": "维护通知",  // 公告标题
            "noticeType": "1",  // 公告类型（1通知 2公告）
            "noticeContent": "系统将于今晚维护",  // 公告内容
            "status": "0",  // 部门状态（0正常 1停用）
            "isRead": false,
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.2.75 查询公告详细

- 接口地址：/system/notice/{noticeId}
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 路径参数：
  - noticeId：公告ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "noticeId": 1,  // 公告ID
        "noticeTitle": "维护通知",  // 公告标题
        "noticeType": "1",  // 公告类型（1通知 2公告）
        "noticeContent": "系统将于今晚维护",  // 公告内容
        "status": "0",  // 部门状态（0正常 1停用）
        "isRead": false,
        "createBy": "字符串",  // 创建者
        "createTime": "2026-10-26 12:00:00",  // 创建时间
        "updateBy": "字符串",  // 更新者
        "updateTime": "2026-10-26 12:00:00",  // 更新时间
        "remark":   // 备注
    }
}
```

#### 4.2.76 新增公告

- 接口地址：/system/notice
- 请求方式：POST
- 权限标识：system:notice:add
- 请求参数：
```text
{
    "noticeTitle": "维护通知",  // 公告标题
    "noticeType": "1",  // 公告类型（1通知 2公告）
    "noticeContent": "系统将于今晚维护",  // 公告内容
    "status": "0",  // 部门状态（0正常 1停用）
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.77 修改公告

- 接口地址：/system/notice
- 请求方式：PUT
- 权限标识：system:notice:edit
- 请求参数：
```text
{
    "noticeId": 1,  // 公告ID
    "noticeTitle": "维护通知",  // 公告标题
    "noticeType": "1",  // 公告类型（1通知 2公告）
    "noticeContent": "系统将于今晚维护",  // 公告内容
    "status": "0",  // 部门状态（0正常 1停用）
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.78 查询最新公告（顶部通知）

- 接口地址：/system/notice/listTop
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": [ { "noticeId": 1, "noticeTitle": "维护通知", "isRead": false } ]
}
```

#### 4.2.79 标记公告已读

- 接口地址：/system/notice/markRead
- 请求方式：POST
- 权限标识：无（登录后即可访问）
- 请求参数：
- 查询参数：
  - noticeId：公告 ID（必填）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.80 全部标记已读

- 接口地址：/system/notice/markReadAll
- 请求方式：POST
- 权限标识：无（登录后即可访问）
- 请求参数：
- 查询参数：
  - ids：公告 ID 字符串，多个用逗号分隔（必填）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.81 查询公告已读用户

- 接口地址：/system/notice/readUsers/list
- 请求方式：GET
- 权限标识：system:notice:list
- 请求参数：
- 查询参数：
  - noticeId：公告 ID（必填）
  - searchValue：搜索关键字（可选）
- 返回参数：
```text
{
    "total": 1,
    "rows": [ { "userId": 1, "userName": "admin", "readTime": "2026-10-26 12:00:00" } ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.2.82 删除公告

- 接口地址：/system/notice/{noticeIds}
- 请求方式：DELETE
- 权限标识：system:notice:remove
- 请求参数：
- 路径参数：
  - noticeIds：参数（多个用英文逗号分隔）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.83 查询个人信息

- 接口地址：/system/user/profile
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 无请求参数（取当前登录用户）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": { ...SysUser 用户对象... },
    "roleGroup": "超级管理员",
    "postGroup": "董事长"
}
```

#### 4.2.84 修改个人信息

- 接口地址：/system/user/profile
- 请求方式：PUT
- 权限标识：无（登录后即可访问）
- 请求参数：
```text
{
    "userId": 100,  // 用户序号
    "deptId": 103,  // 部门编号
    "userName": "ry",  // 登录名称
    "nickName": "若依",  // 用户名称
    "email": "ry@163.com",  // 用户邮箱
    "phonenumber": "15888888888",  // 手机号码
    "sex": "0",  // 用户性别
    "password": "admin123",  // 密码
    "status": "0",  // 账号状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.2.85 修改个人密码

- 接口地址：/system/user/profile/updatePwd
- 请求方式：PUT
- 权限标识：无（登录后即可访问）
- 请求参数：
```text
{
    "oldPassword": "admin123",
    "newPassword": "admin456"
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "修改成功"
}
```

#### 4.2.86 上传个人头像

- 接口地址：/system/user/profile/avatar
- 请求方式：POST
- 权限标识：无（登录后即可访问）
- 请求参数：
- form-data：
  - avatarfile：头像文件（必填）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "imgUrl": "/profile/avatar/2026/10/26/blob_123456.jpg"
}
```

### 4.3 系统监控

#### 4.3.1 查询在线用户列表

- 接口地址：/monitor/online/list
- 请求方式：GET
- 权限标识：monitor:online:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "tokenId": "e4f8****-****-****",
            "deptName": "研发部门",  // 部门名称
            "userName": "ry",  // 用户账号
            "ipaddr": "127.0.0.1",  // 登录IP地址
            "loginLocation": "内网IP",  // 登录地点
            "browser": "Chrome 120",  // 浏览器类型
            "os": "Windows 10",  // 操作系统
            "loginTime": "2026-10-26 12:00:00"  // 访问时间
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.3.2 强制退出用户

- 接口地址：/monitor/online/{tokenId}
- 请求方式：DELETE
- 权限标识：monitor:online:forceLogout
- 请求参数：
- 路径参数：tokenId 会话编号
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.3 查询定时任务列表

- 接口地址：/monitor/job/list
- 请求方式：GET
- 权限标识：monitor:job:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "jobName": null,  // 任务名称
    "jobGroup": null,  // 任务组名
    "status": null  // 任务状态
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "jobId": 100,  // 任务序号
            "jobName": "系统默认（无参）",  // 任务名称
            "jobGroup": "DEFAULT",  // 任务组名
            "invokeTarget": "ryTask.ryNoParams",  // 调用目标字符串
            "cronExpression": "0/10 * * * * ?",  // 执行表达式 
            "misfirePolicy": "1",  // 计划策略 
            "concurrent": "1",  // 并发执行
            "status": "0",  // 任务状态
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.3.4 导出定时任务

- 接口地址：/monitor/job/export
- 请求方式：POST
- 权限标识：monitor:job:export
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "jobName": null,  // 任务名称
    "jobGroup": null,  // 任务组名
    "status": null  // 任务状态
}
```
- 返回参数：
- 返回 Excel 文件流（Content-Type: application/vnd.ms-excel）

#### 4.3.5 查询定时任务详细

- 接口地址：/monitor/job/{jobId}
- 请求方式：GET
- 权限标识：monitor:job:query
- 请求参数：
- 路径参数：
  - jobId：任务ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "jobId": 100,  // 任务序号
        "jobName": "系统默认（无参）",  // 任务名称
        "jobGroup": "DEFAULT",  // 任务组名
        "invokeTarget": "ryTask.ryNoParams",  // 调用目标字符串
        "cronExpression": "0/10 * * * * ?",  // 执行表达式 
        "misfirePolicy": "1",  // 计划策略 
        "concurrent": "1",  // 并发执行
        "status": "0",  // 任务状态
        "createBy": "字符串",  // 创建者
        "createTime": "2026-10-26 12:00:00",  // 创建时间
        "updateBy": "字符串",  // 更新者
        "updateTime": "2026-10-26 12:00:00",  // 更新时间
        "remark":   // 备注
    }
}
```

#### 4.3.6 新增定时任务

- 接口地址：/monitor/job
- 请求方式：POST
- 权限标识：monitor:job:add
- 请求参数：
```text
{
    "jobName": "系统默认（无参）",  // 任务名称
    "jobGroup": "DEFAULT",  // 任务组名
    "invokeTarget": "ryTask.ryNoParams",  // 调用目标字符串
    "cronExpression": "0/10 * * * * ?",  // 执行表达式 
    "misfirePolicy": "1",  // 计划策略 
    "concurrent": "1",  // 并发执行
    "status": "0",  // 任务状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.7 修改定时任务

- 接口地址：/monitor/job
- 请求方式：PUT
- 权限标识：monitor:job:edit
- 请求参数：
```text
{
    "jobId": 100,  // 任务序号
    "jobName": "系统默认（无参）",  // 任务名称
    "jobGroup": "DEFAULT",  // 任务组名
    "invokeTarget": "ryTask.ryNoParams",  // 调用目标字符串
    "cronExpression": "0/10 * * * * ?",  // 执行表达式 
    "misfirePolicy": "1",  // 计划策略 
    "concurrent": "1",  // 并发执行
    "status": "0",  // 任务状态
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.8 修改任务状态

- 接口地址：/monitor/job/changeStatus
- 请求方式：PUT
- 权限标识：monitor:job:changeStatus
- 请求参数：
```text
{
    "jobId": 100,
    "status": "0"
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.9 立即执行一次任务

- 接口地址：/monitor/job/run
- 请求方式：PUT
- 权限标识：monitor:job:changeStatus
- 请求参数：
```text
{
    "jobId": 100,
    "jobGroup": "DEFAULT"
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.10 删除定时任务

- 接口地址：/monitor/job/{jobIds}
- 请求方式：DELETE
- 权限标识：monitor:job:remove
- 请求参数：
- 路径参数：
  - jobIds：任务ID（多个用英文逗号分隔）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.11 查询调度日志列表

- 接口地址：/monitor/jobLog/list
- 请求方式：GET
- 权限标识：monitor:job:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "jobName": null,  // 任务名称
    "jobGroup": null,  // 任务组名
    "status": null  // 执行状态
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "jobLogId": 1,  // 日志序号
            "jobName": "系统默认（无参）",  // 任务名称
            "jobGroup": "DEFAULT",  // 任务组名
            "invokeTarget": "ryTask.ryNoParams",  // 调用目标字符串
            "jobMessage": "执行成功",  // 日志信息
            "status": "0",  // 执行状态
            "exceptionInfo": null,  // 异常信息
            "startTime": "2026-10-26 12:00:00",  // 执行开始时间
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.3.12 导出调度日志

- 接口地址：/monitor/jobLog/export
- 请求方式：POST
- 权限标识：monitor:job:export
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "jobName": null,  // 任务名称
    "jobGroup": null,  // 任务组名
    "status": null  // 执行状态
}
```
- 返回参数：
- 返回 Excel 文件流（Content-Type: application/vnd.ms-excel）

#### 4.3.13 查询调度日志详细

- 接口地址：/monitor/jobLog/{jobLogId}
- 请求方式：GET
- 权限标识：monitor:job:query
- 请求参数：
- 路径参数：
  - jobLogId：任务日志ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "jobLogId": 1,  // 日志序号
        "jobName": "系统默认（无参）",  // 任务名称
        "jobGroup": "DEFAULT",  // 任务组名
        "invokeTarget": "ryTask.ryNoParams",  // 调用目标字符串
        "jobMessage": "执行成功",  // 日志信息
        "status": "0",  // 执行状态
        "exceptionInfo": null,  // 异常信息
        "startTime": "2026-10-26 12:00:00",  // 执行开始时间
        "createBy": "字符串",  // 创建者
        "createTime": "2026-10-26 12:00:00",  // 创建时间
        "updateBy": "字符串",  // 更新者
        "updateTime": "2026-10-26 12:00:00",  // 更新时间
        "remark":   // 备注
    }
}
```

#### 4.3.14 删除调度日志

- 接口地址：/monitor/jobLog/{jobLogIds}
- 请求方式：DELETE
- 权限标识：monitor:job:remove
- 请求参数：
- 路径参数：
  - jobLogIds：调度日志ID（多个用英文逗号分隔）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.15 清空调度日志

- 接口地址：/monitor/jobLog/clean
- 请求方式：DELETE
- 权限标识：monitor:job:remove
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.16 获取缓存监控信息

- 接口地址：/monitor/cache
- 请求方式：GET
- 权限标识：monitor:cache:list
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "info": { "redis_version": "7.2.0", "used_memory": "1.2M" },
        "dbSize": 128,
        "commandStats": [ { "name": "get", "value": 100 } ]
    }
}
```

#### 4.3.17 获取缓存名称列表

- 接口地址：/monitor/cache/getNames
- 请求方式：GET
- 权限标识：monitor:cache:list
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": [ { "cacheName": "sys_config", "remark": "参数管理" } ]
}
```

#### 4.3.18 获取缓存键名列表

- 接口地址：/monitor/cache/getKeys/{cacheName}
- 请求方式：GET
- 权限标识：monitor:cache:list
- 请求参数：
- 路径参数：cacheName 缓存名称
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": [ { "cacheKey": "sys_config:sys.index.skinName", "remark": "皮肤" } ]
}
```

#### 4.3.19 获取缓存内容

- 接口地址：/monitor/cache/getValue/{cacheName}/{cacheKey}
- 请求方式：GET
- 权限标识：monitor:cache:list
- 请求参数：
- 路径参数：cacheName 缓存名称、cacheKey 缓存键名
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "cacheName": "sys_config",
        "cacheKey": "sys_config:sys.index.skinName",
        "cacheValue": "skin-blue",
        "remark": "皮肤"
    }
}
```

#### 4.3.20 清理缓存名称

- 接口地址：/monitor/cache/clearCacheName/{cacheName}
- 请求方式：DELETE
- 权限标识：monitor:cache:list
- 请求参数：
- 路径参数：
  - cacheName：缓存名称
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.21 清理缓存键名

- 接口地址：/monitor/cache/clearCacheKey/{cacheKey}
- 请求方式：DELETE
- 权限标识：monitor:cache:list
- 请求参数：
- 路径参数：
  - cacheKey：缓存键名
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.22 清理全部缓存

- 接口地址：/monitor/cache/clearCacheAll
- 请求方式：DELETE
- 权限标识：monitor:cache:list
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.23 获取服务器监控信息

- 接口地址：/monitor/server
- 请求方式：GET
- 权限标识：monitor:server:list
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "cpu": { "cpuNum": 8, "used": 12.5 },
        "mem": { "total": 16.0, "used": 8.2 },
        "jvm": { "total": 512, "used": 256 },
        "sys": { "computerName": "RY-PC", "osName": "Windows 10" },
        "sysFiles": [ { "dirName": "C:\", "usage": "45%" } ]
    }
}
```

#### 4.3.24 查询登录日志列表

- 接口地址：/monitor/logininfor/list
- 请求方式：GET
- 权限标识：monitor:logininfor:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "userName": null,  // 用户账号
    "status": null,  // 登录状态
    "ipaddr": null  // 登录地址
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "infoId": 1,  // 序号
            "userName": "ry",  // 用户账号
            "status": "0",  // 登录状态
            "ipaddr": "127.0.0.1",  // 登录地址
            "loginLocation": "内网IP",  // 登录地点
            "browser": "Chrome 120",  // 浏览器
            "os": "Windows 10",  // 操作系统
            "msg": "操作成功",  // 提示消息
            "loginTime": "2026-10-26 12:00:00",  // 访问时间
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.3.25 导出登录日志

- 接口地址：/monitor/logininfor/export
- 请求方式：POST
- 权限标识：monitor:logininfor:export
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "userName": null,  // 用户账号
    "status": null,  // 登录状态
    "ipaddr": null  // 登录地址
}
```
- 返回参数：
- 返回 Excel 文件流（Content-Type: application/vnd.ms-excel）

#### 4.3.26 删除登录日志

- 接口地址：/monitor/logininfor/{infoIds}
- 请求方式：DELETE
- 权限标识：monitor:logininfor:remove
- 请求参数：
- 路径参数：
  - infoIds：登录日志ID（多个用英文逗号分隔）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.27 清空登录日志

- 接口地址：/monitor/logininfor/clean
- 请求方式：DELETE
- 权限标识：monitor:logininfor:remove
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.28 解锁用户登录

- 接口地址：/monitor/logininfor/unlock/{userName}
- 请求方式：GET
- 权限标识：monitor:logininfor:unlock
- 请求参数：
- 路径参数：userName 用户名
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.29 查询操作日志列表

- 接口地址：/monitor/operlog/list
- 请求方式：GET
- 权限标识：monitor:operlog:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "title": null,  // 操作模块
    "businessType": null,  // 业务类型
    "operName": null,  // 操作人员
    "status": null  // 状态
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "operId": 1,  // 操作序号
            "title": "用户管理",  // 操作模块
            "businessType": 1,  // 业务类型
            "method": "字符串",  // 请求方法
            "requestMethod": "PUT",  // 请求方式
            "operatorType": 1,  // 操作类别
            "operName": "admin",  // 操作人员
            "deptName": "研发部门",  // 部门名称
            "operUrl": "/system/user",  // 请求地址
            "operIp": "127.0.0.1",  // 操作地址
            "operLocation": "字符串",  // 操作地点
            "operParam": "{...}",  // 请求参数
            "jsonResult": "{...}",  // 返回参数
            "status": "0",  // 状态
            "errorMsg": null,  // 错误消息
            "operTime": "2026-10-26 12:00:00",  // 操作时间
            "costTime": 10,  // 消耗时间
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.3.30 导出操作日志

- 接口地址：/monitor/operlog/export
- 请求方式：POST
- 权限标识：monitor:operlog:export
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "title": null,  // 操作模块
    "businessType": null,  // 业务类型
    "operName": null,  // 操作人员
    "status": null  // 状态
}
```
- 返回参数：
- 返回 Excel 文件流（Content-Type: application/vnd.ms-excel）

#### 4.3.31 删除操作日志

- 接口地址：/monitor/operlog/{operIds}
- 请求方式：DELETE
- 权限标识：monitor:operlog:remove
- 请求参数：
- 路径参数：
  - operIds：操作日志ID（多个用英文逗号分隔）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.3.32 清空操作日志

- 接口地址：/monitor/operlog/clean
- 请求方式：DELETE
- 权限标识：monitor:operlog:remove
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

### 4.4 系统工具

#### 4.4.1 查询代码生成列表

- 接口地址：/tool/gen/list
- 请求方式：GET
- 权限标识：tool:gen:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "tableName": null,  // 表名称
    "tableComment": null  // 表描述
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "tableId": 1,  // 编号
            "tableName": "sys_user",  // 表名称
            "tableComment": "用户信息表",  // 表描述
            "subTableName": "",  // 关联子表的表名
            "subTableFkName": "",  // 子表关联的外键名
            "className": "SysUser",  // 实体类名称
            "tplCategory": "crud",  // 使用的模板（crud单表操作 tree树表操作）
            "tplWebType": "element-ui",  // 前端模板类型（element-ui模版 element-plus模版）
            "packageName": "com.ruoyi.system",  // 生成包路径
            "moduleName": "system",  // 生成模块名
            "businessName": "user",  // 生成业务名
            "functionName": "用户信息",  // 生成功能名
            "functionAuthor": "ruoyi",  // 生成功能作者
            "formColNum": 1,  // 表单布局（单列 双列 三列）
            "genType": "0",  // 生成代码方式（0zip压缩包 1自定义路径）
            "genPath": "/",  // 生成路径（不填默认项目路径）
            "treeCode": "",
            "treeParentCode": "",
            "treeName": "",
            "parentMenuId": null,
            "parentMenuName": null,
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.4.2 查询表详细信息

- 接口地址：/tool/gen/{tableId}
- 请求方式：GET
- 权限标识：tool:gen:query
- 请求参数：
- 路径参数：
  - tableId：表ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "tableId": 1,  // 编号
        "tableName": "sys_user",  // 表名称
        "tableComment": "用户信息表",  // 表描述
        "subTableName": "",  // 关联子表的表名
        "subTableFkName": "",  // 子表关联的外键名
        "className": "SysUser",  // 实体类名称
        "tplCategory": "crud",  // 使用的模板（crud单表操作 tree树表操作）
        "tplWebType": "element-ui",  // 前端模板类型（element-ui模版 element-plus模版）
        "packageName": "com.ruoyi.system",  // 生成包路径
        "moduleName": "system",  // 生成模块名
        "businessName": "user",  // 生成业务名
        "functionName": "用户信息",  // 生成功能名
        "functionAuthor": "ruoyi",  // 生成功能作者
        "formColNum": 1,  // 表单布局（单列 双列 三列）
        "genType": "0",  // 生成代码方式（0zip压缩包 1自定义路径）
        "genPath": "/",  // 生成路径（不填默认项目路径）
        "treeCode": "",
        "treeParentCode": "",
        "treeName": "",
        "parentMenuId": null,
        "parentMenuName": null,
        "createBy": "字符串",  // 创建者
        "createTime": "2026-10-26 12:00:00",  // 创建时间
        "updateBy": "字符串",  // 更新者
        "updateTime": "2026-10-26 12:00:00",  // 更新时间
        "remark":   // 备注
    }
}
```

#### 4.4.3 查询数据库表列表

- 接口地址：/tool/gen/db/list
- 请求方式：GET
- 权限标识：tool:gen:list
- 请求参数：
```text
{
    "pageNum": 1,
    "pageSize": 10,
    "tableName": null,  // 表名称
    "tableComment": null  // 表描述
}
```
- 返回参数：
```text
{
    "total": 1,
    "rows": [
        {
            "tableId": 1,  // 编号
            "tableName": "sys_user",  // 表名称
            "tableComment": "用户信息表",  // 表描述
            "subTableName": "",  // 关联子表的表名
            "subTableFkName": "",  // 子表关联的外键名
            "className": "SysUser",  // 实体类名称
            "tplCategory": "crud",  // 使用的模板（crud单表操作 tree树表操作）
            "tplWebType": "element-ui",  // 前端模板类型（element-ui模版 element-plus模版）
            "packageName": "com.ruoyi.system",  // 生成包路径
            "moduleName": "system",  // 生成模块名
            "businessName": "user",  // 生成业务名
            "functionName": "用户信息",  // 生成功能名
            "functionAuthor": "ruoyi",  // 生成功能作者
            "formColNum": 1,  // 表单布局（单列 双列 三列）
            "genType": "0",  // 生成代码方式（0zip压缩包 1自定义路径）
            "genPath": "/",  // 生成路径（不填默认项目路径）
            "treeCode": "",
            "treeParentCode": "",
            "treeName": "",
            "parentMenuId": null,
            "parentMenuName": null,
            "createBy": "字符串",  // 创建者
            "createTime": "2026-10-26 12:00:00",  // 创建时间
            "updateBy": "字符串",  // 更新者
            "updateTime": "2026-10-26 12:00:00",  // 更新时间
            "remark":   // 备注
        }
    ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.4.4 查询表字段列表

- 接口地址：/tool/gen/column/{tableId}
- 请求方式：GET
- 权限标识：tool:gen:list
- 请求参数：
- 路径参数：tableId 表 ID
- 返回参数：
```text
{
    "total": 12,
    "rows": [ { ...GenTableColumn 字段对象... } ],
    "code": 200,
    "msg": "查询成功"
}
```

#### 4.4.5 导入表结构

- 接口地址：/tool/gen/importTable
- 请求方式：POST
- 权限标识：tool:gen:import
- 请求参数：
- form-data：
  - tables：待导入的表名，多个用逗号分隔（必填）
  - tplWebType：模板类型，如 element-ui（必填）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.4.6 创建表结构

- 接口地址：/tool/gen/createTable
- 请求方式：POST
- 权限标识：角色:admin
- 请求参数：
- form-data：
  - sql：建表 SQL 语句（必填）
  - tplWebType：模板类型（必填）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.4.7 修改代码生成业务

- 接口地址：/tool/gen
- 请求方式：PUT
- 权限标识：tool:gen:edit
- 请求参数：
```text
{
    "tableId": 1,  // 编号
    "tableName": "sys_user",  // 表名称 必填
    "tableComment": "用户信息表",  // 表描述 必填
    "subTableName": "",  // 关联子表的表名
    "subTableFkName": "",  // 子表关联的外键名
    "className": "SysUser",  // 实体类名称 必填
    "tplCategory": "crud",  // 使用的模板（crud单表操作 tree树表操作）
    "tplWebType": "element-ui",  // 前端模板类型（element-ui模版 element-plus模版）
    "packageName": "com.ruoyi.system",  // 生成包路径 必填
    "moduleName": "system",  // 生成模块名 必填
    "businessName": "user",  // 生成业务名 必填
    "functionName": "用户信息",  // 生成功能名 必填
    "functionAuthor": "ruoyi",  // 生成功能作者 必填
    "formColNum": 1,  // 表单布局（单列 双列 三列）
    "genType": "0",  // 生成代码方式（0zip压缩包 1自定义路径）
    "genPath": "/",  // 生成路径（不填默认项目路径）
    "treeCode": "",
    "treeParentCode": "",
    "treeName": "",
    "parentMenuId": null,
    "parentMenuName": null,
    "remark":   // 备注
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.4.8 删除表数据

- 接口地址：/tool/gen/{tableIds}
- 请求方式：DELETE
- 权限标识：tool:gen:remove
- 请求参数：
- 路径参数：
  - tableIds：表ID（多个用英文逗号分隔）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.4.9 预览生成代码

- 接口地址：/tool/gen/preview/{tableId}
- 请求方式：GET
- 权限标识：tool:gen:preview
- 请求参数：
- 路径参数：tableId 表 ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": { "domain.java.vm": "package com.ruoyi.system.domain;...", "api.js.vm": "..." }
}
```

#### 4.4.10 下载生成代码

- 接口地址：/tool/gen/download/{tableName}
- 请求方式：GET
- 权限标识：tool:gen:code
- 请求参数：
- 路径参数：tableName 表名
- 返回参数：
- 返回生成的代码压缩包（.zip）文件流

#### 4.4.11 生成代码（自定义路径）

- 接口地址：/tool/gen/genCode/{tableName}
- 请求方式：GET
- 权限标识：tool:gen:code
- 请求参数：
- 路径参数：tableName 表名
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.4.12 同步表结构

- 接口地址：/tool/gen/synchDb/{tableName}
- 请求方式：GET
- 权限标识：tool:gen:edit
- 请求参数：
- 路径参数：
  - tableName：表名
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功"
}
```

#### 4.4.13 批量生成代码

- 接口地址：/tool/gen/batchGenCode
- 请求方式：GET
- 权限标识：tool:gen:code
- 请求参数：
- 查询参数：
  - tables：表名，多个用逗号分隔（必填）
- 返回参数：
- 返回生成的代码压缩包（.zip）文件流

### 4.5 通用接口

#### 4.5.1 通用文件下载

- 接口地址：/common/download
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 查询参数：
  - fileName：文件名（必填）
  - delete：下载后是否删除（布尔值，可选）
- 返回参数：
- 返回文件流

#### 4.5.2 单文件上传

- 接口地址：/common/upload
- 请求方式：POST
- 权限标识：无（登录后即可访问）
- 请求参数：
- form-data：
  - file：上传的文件（必填）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "fileName": "/profile/upload/2026/10/26/abc.jpg",
    "url": "http://localhost:8080/profile/upload/2026/10/26/abc.jpg",
    "newFileName": "abc.jpg",
    "originalFilename": "abc.jpg"
}
```

#### 4.5.3 多文件上传

- 接口地址：/common/uploads
- 请求方式：POST
- 权限标识：无（登录后即可访问）
- 请求参数：
- form-data：
  - files：上传的文件列表（必填，可多选）
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "urls": [ "http://localhost:8080/profile/upload/2026/10/26/abc.jpg" ]
}
```

#### 4.5.4 资源文件下载

- 接口地址：/common/download/resource
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 查询参数：
  - resource：资源路径（必填）
- 返回参数：
- 返回文件流

### 4.6 测试接口

#### 4.6.1 查询测试用户列表

- 接口地址：/test/user/list
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 无请求参数
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": [ { "userId": 1, "username": "admin", "password": "123456", "mobile": "15888888888" } ]
}
```

#### 4.6.2 查询测试用户详细

- 接口地址：/test/user/{userId}
- 请求方式：GET
- 权限标识：无（登录后即可访问）
- 请求参数：
- 路径参数：
  - userId：用户ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "userId": 100,  // 用户ID
        "username": "ry",  // 用户账号
        "mobile": "15888888888"  // 手机号
    }
}
```

#### 4.6.3 新增测试用户

- 接口地址：/test/user/save
- 请求方式：POST
- 权限标识：无（登录后即可访问）
- 请求参数：
```text
{
    "userId": 100,  // 用户ID
    "username": "ry",  // 用户账号
    "password": "admin123",  // 密码
    "mobile": "15888888888"  // 手机号
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "userId": 100,  // 用户ID
        "username": "ry",  // 用户账号
        "mobile": "15888888888"  // 手机号
    }
}
```

#### 4.6.4 修改测试用户

- 接口地址：/test/user/update
- 请求方式：PUT
- 权限标识：无（登录后即可访问）
- 请求参数：
```text
{
    "userId": 100,  // 用户ID
    "username": "ry",  // 用户账号
    "password": "admin123",  // 密码
    "mobile": "15888888888"  // 手机号
}
```
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "userId": 100,  // 用户ID
        "username": "ry",  // 用户账号
        "mobile": "15888888888"  // 手机号
    }
}
```

#### 4.6.5 删除测试用户

- 接口地址：/test/user/{userId}
- 请求方式：DELETE
- 权限标识：无（登录后即可访问）
- 请求参数：
- 路径参数：
  - userId：用户ID
- 返回参数：
```text
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "userId": 100,  // 用户ID
        "username": "ry",  // 用户账号
        "mobile": "15888888888"  // 手机号
    }
}
```

---

> 文档由源码自动整理生成，接口以实际运行版本为准。