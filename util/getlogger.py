import logging
import logging.config
import logging.handlers

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# 获取日志器
class GetLogger(object):
    _logger = ["root", "basiclogger", "smmslogger"]
    def __init__(self, logpath=None):
        self.logpath = logpath if logpath else f"{BASE_DIR}/config/logger.conf"

    def get_logger(self, logger="basiclogger") -> "return init logger":
        if logger in self._logger:
            logging.config.fileConfig(self.logpath)
            return logging.getLogger(logger)
        else:
            raise ValueError(f"选择的日志器未在配置中找到，请检查日志配置文件{self.logpath}")
