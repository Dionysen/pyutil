import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from dionysen import logger

logger.setLevel(level="DEBUG")

logger.debug("这是一个调试信息")
logger.info("开始测试 logger 模块")
logger.warning("这是一个警告信息")
logger.error("这是一个错误信息")
logger.critical("这是一个严重错误信息")