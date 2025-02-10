# logger.py

import utime as time

class Logger:
    def __init__(self, filename=None, level="INFO", min_level="DEBUG"):
        self.level = level
        self.filename = filename
        self.min_level = min_level
    
    def log(self, message, level="INFO"):
        # 自定义日志级别
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        if levels.index(level) >= levels.index(self.min_level):
            runtime = time.ticks_ms()  # 获取系统运行时间（毫秒）
            log_message = "{} - {} - {}".format(runtime, level, message)
            
            # 输出到控制台
            print(log_message)
            
            # 如果设置了日志文件名，写入文件
            if self.filename:
                with open(self.filename, 'a') as log_file:
                    log_file.write(log_message + "\n")

    def debug(self, *args):
        self.log(self._format_message(*args), level="DEBUG")
    
    def info(self, *args):
        self.log(self._format_message(*args), level="INFO")
    
    def warning(self, *args):
        self.log(self._format_message(*args), level="WARNING")
    
    def error(self, *args):
        self.log(self._format_message(*args), level="ERROR")
    
    def critical(self, *args):
        self.log(self._format_message(*args), level="CRITICAL")
    
    # 新增方法来处理多个参数，将它们连接成一个字符串
    def _format_message(self, *args):
        return ' '.join(str(arg) for arg in args)
