import logging
from .config import Config
from colorama import Fore, Style

class CustomFormatter(logging.Formatter):
    """自定义日志格式化器，带方括号和可选颜色"""
    
    def __init__(self, use_color=False):
        super().__init__(
            '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.use_color = use_color
        
        if use_color:
            try:
                from colorama import Fore, Style, init
                init()
                self.COLORS = {
                    'DEBUG': Fore.CYAN,
                    'INFO': Fore.GREEN,
                    'WARNING': Fore.YELLOW,
                    'ERROR': Fore.RED,
                    'CRITICAL': Fore.RED + Style.BRIGHT
                }
            except ImportError:
                self.use_color = False

    def format(self, record):
        message = super().format(record)
        if self.use_color:
            level_color = self.COLORS.get(record.levelname, '')
            message = message.replace(
                f'[{record.levelname}]', 
                f'[{level_color}{record.levelname}{Style.RESET_ALL}]'
            )
        return message

def setup_logger(name=None, use_color=True):
    """设置和返回日志记录器
    
    Args:
        name (str, optional): 日志记录器名称. Defaults to None.
        use_color (bool, optional): 是否使用彩色输出. Defaults to True.
    """
    config = Config()
    
    logger = logging.getLogger(name or "batch_utils")
    
    if not logger.handlers:
        logger.setLevel(getattr(logging, config.get("log_level", "INFO")))
        
        # 创建控制台处理器
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # 创建格式化器
        formatter = CustomFormatter(use_color=use_color)
        ch.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        logger.addHandler(ch)
    
    return logger