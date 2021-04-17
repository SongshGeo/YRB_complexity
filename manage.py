import logging
import datetime
import os

UPDATE_FILE = os.path.join(os.getcwd(), r"../log/updates.log")


def create_a_logger(name, file=UPDATE_FILE, console=True):
    # 第一步，创建一个 Logger
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.INFO)

    # 第二步，创建一个 handle 用于写入日志文件
    file_handle = logging.FileHandler(file, mode='w')  # 输出到文件
    file_handle.setLevel(logging.INFO)  # 输出等级控制在信息

    # 第三步，定义 handler 的输出格式
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s: %(message)s")
    file_handle.setFormatter(formatter)

    # 第四步，将 logger 添加到 handle 里
    logger.addHandler(file_handle)

    # 如果控制台也要输出
    if console:
        console_handle = logging.StreamHandler()  # 输出到控制台
        console_handle.setLevel(logging.WARNING)  # 输出等级控制在警告
        console_handle.setFormatter(formatter)  # 控制输出格式
        logger.addHandler(console_handle)
    return logger


if __name__ == '__main__':
    # 创建该项目的时候运行该行代码
    # Run this file when the project created.
    print(UPDATE_FILE)
    prj_path = os.path.dirname(os.getcwd())
    prj_name = os.path.abspath(prj_path).split("/")[-1]
    log = create_a_logger('create')
    log.info(f'Project {prj_name} updated at {datetime.date.today()}')
