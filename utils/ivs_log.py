import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta, timezone
import re
class LOGGER(logging.Logger):
    def __init__(self, default_path='./logs', logfile_name='my_log.log') -> None:
        # Initialize the logger class
        super(LOGGER, self).__init__(logfile_name)  # Should pass the log file name
        # Ensure the directory exists, create if it doesn't
        log_dir = os.path.join(default_path)
        os.makedirs(log_dir, exist_ok=True)  # Ensure log directory exists

        # Construct the full path for the log file
        self.log_path = os.path.join(log_dir, logfile_name)
        self.setup_log()

    def setup_log(self):
        self.setLevel(logging.INFO)  # Set log level

        # Create TimedRotatingFileHandler
        file_handler = TimedRotatingFileHandler(
            filename=self.log_path,
            when="D",  # Rotate logs daily
            interval=1,
            backupCount=2,  # Keep the last 2 log files
            utc=False  # Use local time for rotation
        )

        # Custom formatter with UTC+8
        formatter = CustomFormatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        
        file_handler.setFormatter(formatter)
       
        # Add the file handler to logger
        self.addHandler(file_handler)

        # Create StreamHandler to output logs to the console
        stream_handler = logging.StreamHandler()  # Output to sys.stdout by default
        stream_handler.setFormatter(formatter)  # Use the same format
        self.addHandler(stream_handler)  # Add the stream handler to the logger


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # Get the UTC time and convert to UTC+8 (Asia/Shanghai)
        created_time = datetime.fromtimestamp(record.created, tz=timezone.utc)
        local_time = created_time.astimezone(timezone(timedelta(hours=8)))  # Convert to UTC+8
        return local_time.strftime("%Y-%m-%d %H:%M:%S")  # Return in the desired format

# Example usage
if __name__ == "__main__":
    log_dir = "./logs1"  # Log directory
    log_name = "my_log.log"  # Log file name
    
    # Instantiate logger
    logger = LOGGER(log_dir, log_name)
    
    # Record some logs
    logger.info("This is an info message")
    logger.error("This is an error message")
    logger.warning("This is a warning message")
