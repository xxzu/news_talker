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
        self.setLevel(logging.INFO)  # 设置日志级别
        
        # 创建 TimedRotatingFileHandler
        file_handler = TimedRotatingFileHandler(
            filename=self.log_path,
            when="D",  # 按天切割
            interval=1,
            backupCount=2,  # 保留最近的2个日志文件
            utc=False  # False 表示按系统时间（本地时间）切割日志
        )
        file_handler.suffix = "%Y-%m-%d.log"
        
        # 设置日志格式
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        
        # 添加文件处理器到 logger
        self.addHandler(file_handler)

        # 创建 StreamHandler，将日志输出到标准输出（控制台）
        stream_handler = logging.StreamHandler()  # 默认输出到 sys.stdout
        stream_handler.setFormatter(formatter)  # 使用相同的格式
        self.addHandler(stream_handler)  # 将控制台输出处理器添加到 logger

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
