import os
import json
from pathlib import Path

class Config:
    """全局配置管理类"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._init_config()
        return cls._instance
    
    def _init_config(self):
        """初始化配置"""
        self.config_dir = Path.home() / ".dionysen_utils"
        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "log_level": "INFO",
            "max_retries": 3,
            "timeout": 30,
            "temp_dir": str(Path.home() / "dionysen_utils_temp")
        }
        
        # 确保配置目录存在
        self.config_dir.mkdir(exist_ok=True)
        
        # 加载或创建配置文件
        if self.config_file.exists():
            self.load()
        else:
            self.config = self.default_config.copy()
            self.save()
    
    def load(self):
        """加载配置文件"""
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
    
    def save(self):
        """保存配置文件"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置值"""
        self.config[key] = value
        self.save()