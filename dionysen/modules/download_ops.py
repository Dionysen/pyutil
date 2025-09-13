import requests
from pathlib import Path
from urllib.parse import urlparse
from ..core.base import BaseProcessor

class DownloadOperations(BaseProcessor):
    """下载操作处理器"""
    
    def __init__(self):
        super().__init__("DownloadOperations")
    
    def download_file(self, url, destination=None, overwrite=False):
        """下载文件到指定位置"""
        if destination is None:
            # 从URL提取文件名
            parsed_url = urlparse(url)
            filename = Path(parsed_url.path).name
            destination = Path.cwd() / filename
        else:
            destination = Path(destination)
        
        # 检查文件是否已存在
        if destination.exists() and not overwrite:
            self.logger.warning(f"文件已存在，跳过下载: {destination}")
            return str(destination)
        
        # 创建目录（如果不存在）
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            self.logger.info(f"开始下载: {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.logger.info(f"下载完成: {destination}")
            return str(destination)
        
        except Exception as e:
            self.logger.error(f"下载失败 {url}: {e}")
            raise
    
    def batch_download(self, url_list, output_dir, overwrite=False):
        """批量下载文件"""
        downloaded_files = []
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for url in url_list:
            try:
                parsed_url = urlparse(url)
                filename = Path(parsed_url.path).name
                destination = output_dir / filename
                
                file_path = self.download_file(url, destination, overwrite)
                downloaded_files.append(file_path)
            
            except Exception as e:
                self.logger.error(f"批量下载失败 {url}: {e}")
                continue
        
        return downloaded_files