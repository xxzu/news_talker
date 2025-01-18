import os
import re
import logging
from logging.handlers import TimedRotatingFileHandler

class LOGGER(logging.Logger):  # Inherit from logging.Logger
    
    def __init__(self, default_path='./logs', logfile_name='my_log.log') -> None:
        # 初始化日志类
        super(LOGGER, self).__init__(logfile_name)  # 此处应该传递日志名称
        # 确保路径存在，不存在就创建
        log_dir = os.path.join(default_path)
        os.makedirs(log_dir, exist_ok=True)  # 确保日志目录存在

        # 构造日志文件的完整路径
        self.log_path = os.path.join(log_dir, logfile_name)
        self.setup_log()

    def setup_log(self):
        # 设置日志级别
        self.setLevel(logging.INFO)
        
        # 创建 TimedRotatingFileHandler 处理器，设置每天切割，保留7天日志
        file_handler = TimedRotatingFileHandler(filename=self.log_path, when="D", interval=1, backupCount=7)
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        
        # 设置日志输出格式
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        
        # 将文件处理器添加到 logger 中
        self.addHandler(file_handler)

# Example usage
if __name__ == "__main__":
    log_dir = "./logs1"  # 日志目录
    log_name = "my_log.log"  # 日志文件名
    
    # 实例化 logger
    logger = LOGGER(log_dir, log_name)
    
    # 记录日志
    logger.info("This is an info message")
    logger.error("This is an error message")
    logger.warning("This is a warning message")
