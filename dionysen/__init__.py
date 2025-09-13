"""
Batch Utils - 一个强大的Python批处理工具库
"""

from .modules.file_ops import FileOperations
from .modules.download_ops import DownloadOperations
from .modules.archive_ops import ArchiveOperations
from .core.config import Config
from .core.logger import setup_logger

# 创建常用实例
file_ops = FileOperations()
download_ops = DownloadOperations()
archive_ops = ArchiveOperations()
config = Config()
logger = setup_logger()

__all__ = [
    'FileOperations',
    'DownloadOperations',
    'ArchiveOperations',
    'Config',
    'file_ops',
    'download_ops',
    'archive_ops',
    'config',
    'logger'
]

__version__ = '0.1.0'