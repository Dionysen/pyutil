import zipfile
import tarfile
from pathlib import Path
from ..core.base import BaseProcessor

class ArchiveOperations(BaseProcessor):
    """压缩文件操作处理器"""
    
    def __init__(self):
        super().__init__("ArchiveOperations")
    
    def extract_archive(self, archive_path, extract_dir=None, format=None):
        """解压压缩文件"""
        archive_path = Path(archive_path)
        
        if extract_dir is None:
            extract_dir = archive_path.parent / archive_path.stem
        else:
            extract_dir = Path(extract_dir)
        
        extract_dir.mkdir(parents=True, exist_ok=True)
        
        # 自动检测格式
        if format is None:
            if archive_path.suffix.lower() in ['.zip']:
                format = 'zip'
            elif archive_path.suffix.lower() in ['.tar', '.tgz', '.gz', '.bz2']:
                format = 'tar'
            else:
                raise ValueError("无法识别压缩文件格式")
        
        try:
            if format == 'zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
            elif format == 'tar':
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_dir)
            
            self.logger.info(f"已解压: {archive_path} -> {extract_dir}")
            return str(extract_dir)
        
        except Exception as e:
            self.logger.error(f"解压失败 {archive_path}: {e}")
            raise
    
    def create_archive(self, source_path, archive_path, format='zip', include_root=True):
        """创建压缩文件"""
        source_path = Path(source_path)
        archive_path = Path(archive_path)
        
        try:
            if format == 'zip':
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    if source_path.is_file():
                        zipf.write(source_path, source_path.name)
                    else:
                        for file in source_path.rglob('*'):
                            if file.is_file():
                                if include_root:
                                    # 包含根目录名称
                                    arcname = file.relative_to(source_path.parent)
                                else:
                                    # 不包含根目录名称，直接从内容开始
                                    arcname = file.relative_to(source_path)
                                zipf.write(file, arcname)
            
            elif format == 'tar':
                with tarfile.open(archive_path, 'w:gz') as tarf:
                    if source_path.is_file():
                        tarf.add(source_path, arcname=source_path.name)
                    else:
                        tarf.add(source_path, arcname=source_path.name)
            
            self.logger.info(f"已创建压缩文件: {archive_path}")
            return str(archive_path)
        
        except Exception as e:
            self.logger.error(f"创建压缩文件失败: {e}")
            raise