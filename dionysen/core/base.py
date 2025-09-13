from .logger import setup_logger

class BaseProcessor:
    """所有处理器的基类"""
    
    def __init__(self, name=None):
        self.logger = setup_logger(name or self.__class__.__name__)
        self._validate_requirements()
    
    def _validate_requirements(self):
        """验证所需的依赖是否已安装"""
        pass
    
    def process(self, *args, **kwargs):
        """处理方法的抽象定义"""
        raise NotImplementedError("子类必须实现process方法")