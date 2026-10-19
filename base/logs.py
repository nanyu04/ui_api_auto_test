import logging.handlers
import os

# 创建logs文件夹
logs = os.path.join(os.getcwd(), "logs")
if not os.path.exists(logs):
    os.mkdir(logs)
# 创建日志对象
lg = logging.getLogger()
# 设置级别
lg.setLevel(logging.INFO)
lg.handlers.clear()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')
# 创建控制台输出
console = logging.StreamHandler()
# 设置控制台输出级别
console.setLevel(logging.INFO)
# 设置控制台数据格式
console.setFormatter(formatter)
# 创建文件报错输出
worse_file = logging.handlers.TimedRotatingFileHandler(filename=os.path.join(logs, "worse.log"),
                                                       when="D",
                                                       interval=1,
                                                       backupCount=10,
                                                       encoding="utf-8", )
worse_file.setLevel(logging.ERROR)
worse_file.setFormatter(formatter)

lg.addHandler(console)
lg.addHandler(worse_file)

log = lg