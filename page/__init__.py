"""
若依管理系统 - 页面元素定位器汇总
所有定位器按照模块分组
"""
from selenium.webdriver.common.by import By

# ==================== 登录页面 ====================
# 登录按钮
Enter = (By.XPATH, "//*[@id='app']/div[1]/form/div[3]/div/button")
# 用户名输入框
Login_Username = (By.XPATH, "//input[@placeholder='账号']")
# 密码输入框
Login_Password = (By.XPATH, "//input[@placeholder='密码']")
# 验证码输入框
Login_Captcha = (By.XPATH, "//input[@placeholder='验证码']")
# 登录页面标题
Login_Title = (By.XPATH, "//h3[contains(text(),'若依')]")

# ==================== 首页 ====================
# 首页欢迎语
Home_Welcome = (By.XPATH, "//span[contains(text(),'首页')]")
# 用户头像下拉
User_Avatar = (By.XPATH, "//div[@class='avatar-wrapper']")
# 退出登录按钮
Logout_Btn = (By.XPATH, "//span[contains(text(),'退出登录')]")

# ==================== 侧边栏菜单 ====================
# 系统管理菜单
click_systemm = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[2]/li/div")
# 用户管理子菜单
click_userm = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[2]/li/ul/div[1]/a/li/span")
# 角色管理子菜单
click_role = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[2]/li/ul/div[2]/a/li/span")
# 菜单管理子菜单
click_menu_m = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[2]/li/ul/div[3]/a/li/span")
# 部门管理子菜单
click_dept_m = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[2]/li/ul/div[4]/a/li/span")
# 岗位管理子菜单
click_post_m = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[2]/li/ul/div[5]/a/li/span")
# 字典管理子菜单
click_dict_m = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[2]/li/ul/div[6]/a/li/span")
# 参数设置子菜单
click_config_m = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[2]/li/ul/div[7]/a/li/span")
# 通知公告子菜单
click_notice_m = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[2]/li/ul/div[8]/a/li/span")

# 系统监控菜单
click_monitor_m = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[3]/li/div")
# 在线用户
click_online_m = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[3]/li/ul/div[1]/a/li/span")
# 定时任务
click_job_m = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[3]/li/ul/div[2]/a/li/span")
# 服务监控
click_server_m = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[3]/li/ul/div[3]/a/li/span")
# 缓存监控
click_cache_m = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[1]/div/ul/div[3]/li/ul/div[4]/a/li/span")

# ==================== 用户管理页面 ====================
# 新增按钮
click_addUser = (By.XPATH, "//*[@id='app']/div[1]/div[2]/section/div/div[2]/div/div[1]/div[1]/button")
# 用户昵称输入框
UserId = (By.XPATH, "//input[contains(@placeholder,'请输入用户昵称')]")
# 手机号码输入框
PhoneNumber = (By.XPATH, "//div[contains(@class,'el-input--medium')]//input[contains(@placeholder,'请输入手机号码')]")
# 用户名称输入框
UserName = (By.XPATH, "//div[contains(@class,'el-input--medium')]//input[contains(@placeholder,'请输入用户名称')]")
# 邮箱输入框
PostId = (By.XPATH, "//input[contains(@placeholder,'请输入邮箱')]")
# 岗位下拉
Occuptionset = (By.XPATH, "//div[contains(@class,'el-select')]//input[@placeholder='请选择岗位']/ancestor::div[contains(@class,'el-select')]")
# 岗位-董事长选项
Occuption = (By.XPATH, "//div[contains(@class,'el-select-dropdown')]//span[text()='董事长']")
# 性别下拉
Click_Gender = (By.XPATH, "//input[contains(@placeholder,'请选择性别')]/ancestor::div[contains(@class,'el-select')]")
# 性别-女
Gender = (By.XPATH, "//div[contains(@class,'el-select-dropdown__wrap')]//li[contains(@class,'el-select-dropdown__item')]//span[text()='女']")
# 角色下拉
Click_Character = (By.XPATH, "//input[@placeholder='请选择角色']/ancestor::div[contains(@class,'el-select')]")
# 角色-普通角色
Character = (By.XPATH, "//div[contains(@class,'el-select-dropdown__wrap')]//span[text()='普通角色']")
# 部门树控件
Click_partment = (By.XPATH, "//input[@class='vue-treeselect__input']/ancestor::div[contains(@class,'vue-treeselect__control')]")
# 部门-若依科技
partment = (By.XPATH, "//div[contains(@class,'vue-treeselect__label-container')]//label[contains(text(),'若依科技')]")
# 确定按钮
Ensure = (By.CSS_SELECTOR, "body > div.el-dialog__wrapper > div > div.el-dialog__footer > div > button.el-button.el-button--primary.el-button--medium > span")
# 取消按钮
Cancel = (By.XPATH, "//span[text()='取 消']")
# 新增用户对话框标题
Dialog_Title = (By.XPATH, "//span[contains(text(),'添加用户')]")
# 消息提示
Adduser_success = (By.XPATH, "//p[@class='el-message__content']")
# 用户昵称不能为空提示
UserName_notNull = (By.XPATH, "//div[@class='el-form-item__error']")
# 搜索按钮
Search_Btn = (By.XPATH, "//button[contains(@class,'el-button--primary')]//span[text()='搜索']")
# 重置按钮
Reset_Btn = (By.XPATH, "//button[contains(@class,'el-button--default')]//span[text()='重置']")
# 表格第一行
Table_First_Row = (By.XPATH, "//tbody/tr[1]")
# 删除按钮(行内)
Delete_Btn = (By.XPATH, "//span[text()='删除']")

# ==================== 角色管理页面 ====================
# 角色新增按钮
Role_Add_Btn = (By.XPATH, "//button[contains(@class,'el-button--primary')]//span[text()='新增']")
# 角色名称输入框
Role_Name_Input = (By.XPATH, "//input[@placeholder='请输入角色名称']")
# 角色权限字符串输入
Role_Key_Input = (By.XPATH, "//input[@placeholder='请输入权限字符']")

# ==================== 菜单管理页面 ====================
# 菜单展开/折叠全部
Menu_Expand_Btn = (By.XPATH, "//span[text()='展开/折叠']")

# ==================== 通知公告页面 ====================
# 通知新增按钮
Notice_Add_Btn = (By.XPATH, "//button[contains(@class,'el-button--primary')]//span[text()='新增']")
# 公告标题输入框
Notice_Title_Input = (By.XPATH, "//input[@placeholder='请输入公告标题']")

# ==================== 个人信息/修改密码 ====================
# 旧密码
Old_Password = (By.XPATH, "//input[@placeholder='请输入旧密码']")
# 新密码
New_Password = (By.XPATH, "//input[@placeholder='请输入新密码']")
# 确认密码
Confirm_Password = (By.XPATH, "//input[@placeholder='请输入确认密码']")