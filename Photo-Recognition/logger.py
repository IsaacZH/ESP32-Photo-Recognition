# logger.py

import utime as time

class Logger:
    def __init__(self, filename=None, level="INFO", min_level="DEBUG"):
        self.level = level
        self.filename = filename
        self.min_level = min_level
    
    def log(self, message, level="INFO"):
        # Custom log levels
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        if levels.index(level) >= levels.index(self.min_level):
            runtime = time.ticks_ms()  # Get system runtime (milliseconds)
            log_message = "{} - {} - {}".format(runtime, level, message)
            
            # Output to console
            print(log_message)
            
            # If a log filename is set, write to file
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
    
    # New method to handle multiple arguments and concatenate them into a string
    def _format_message(self, *args):
        return ' '.join(str(arg) for arg in args)
