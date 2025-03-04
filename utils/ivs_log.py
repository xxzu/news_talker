import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta, timezone
import re
class LOGGER(logging.Logger):
    def __init__(self, default_path='./logs', logfile_name='my_log') -> None:
        super(LOGGER, self).__init__(logfile_name)  
        
        log_dir = os.path.join(default_path)
        os.makedirs(log_dir, exist_ok=True)  

        
        self.log_path = os.path.join(log_dir, logfile_name)
        self.setup_log()

    def setup_log(self):
        self.setLevel(logging.INFO)  


        file_handler = TimedRotatingFileHandler(
            filename=self.log_path,
            when="D", 
            interval=1,
            backupCount=1,  
            utc=True 
        )

        
        formatter = CustomFormatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        # file_handler.suffix = "%Y-%m-%d-%H:%M:%S.log"
        # file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        
        file_handler.setFormatter(formatter)
       
        
        self.addHandler(file_handler)

        # 输出到控制台
        stream_handler = logging.StreamHandler()  
        stream_handler.setFormatter(formatter)  
        self.addHandler(stream_handler)  


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
       
        created_time = datetime.fromtimestamp(record.created, tz=timezone.utc)
        local_time = created_time.astimezone(timezone(timedelta(hours=8)))  # Convert to UTC+8
        return local_time.strftime("%Y-%m-%d %H:%M:%S")  

# Example usage
if __name__ == "__main__":
    log_dir = "./logs1"  
    log_name = "my_log" 
    
    
    logger = LOGGER(log_dir, log_name)

    logger.info("This is an info message")
    logger.error("This is an error message")
    logger.warning("This is a warning message")



