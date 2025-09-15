import os
import shutil
from pathlib import Path
from ..core.base import BaseProcessor

# import PIL
try:
    from PIL import Image
except ImportError:
    Image = None

class FileOperations(BaseProcessor):
    """文件操作处理器"""
    
    def __init__(self):
        super().__init__("FileOperations")
    
    def copy_files(self, source_pattern, destination_dir, overwrite=False):
        """复制匹配模式的文件到目标目录"""
        destination = Path(destination_dir)
        destination.mkdir(parents=True, exist_ok=True)
        
        copied_files = []
        for file_path in Path().glob(source_pattern):
            dest_path = destination / file_path.name
            if not overwrite and dest_path.exists():
                self.logger.warning(f"文件已存在，跳过: {dest_path}")
                continue
            
            shutil.copy2(file_path, dest_path)
            copied_files.append(str(dest_path))
            self.logger.info(f"已复制: {file_path} -> {dest_path}")
        
        return copied_files
    
    def delete_files(self, pattern, confirm=True):
        """删除匹配模式的文件"""
        files_to_delete = list(Path().glob(pattern))
        
        if not files_to_delete:
            self.logger.info("没有找到匹配的文件")
            return []
        
        if confirm:
            print(f"找到 {len(files_to_delete)} 个匹配的文件:")
            for f in files_to_delete:
                print(f"  {f}")
            
            response = input("确认删除这些文件吗? (y/N): ")
            if response.lower() != 'y':
                self.logger.info("取消删除操作")
                return []
        
        deleted_files = []
        for file_path in files_to_delete:
            try:
                if file_path.is_file():
                    file_path.unlink()
                    deleted_files.append(str(file_path))
                    self.logger.info(f"已删除: {file_path}")
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                    deleted_files.append(str(file_path))
                    self.logger.info(f"已删除目录: {file_path}")
            except Exception as e:
                self.logger.error(f"删除失败 {file_path}: {e}")
        
        return deleted_files
    
    def rename_files(self, pattern, new_name_pattern, dry_run=False):
        """重命名匹配模式的文件"""
        renamed_files = []
        for i, file_path in enumerate(Path().glob(pattern)):
            new_name = new_name_pattern.format(index=i+1, name=file_path.stem, ext=file_path.suffix[1:])
            new_path = file_path.parent / new_name
            
            if dry_run:
                self.logger.info(f"将会重命名: {file_path} -> {new_path}")
                renamed_files.append((str(file_path), str(new_path)))
            else:
                try:
                    file_path.rename(new_path)
                    renamed_files.append((str(file_path), str(new_path)))
                    self.logger.info(f"已重命名: {file_path} -> {new_path}")
                except Exception as e:
                    self.logger.error(f"重命名失败 {file_path}: {e}")
        
        return renamed_files

    def convert_image_format(self, source_pattern, target_format, delete_original=False):
        """
        转换匹配模式的图片文件格式.
        例如, 将 .jfif 转换为 .jpg
        
        :param source_pattern: 源文件匹配模式 (例如: '*.jfif')
        :param target_format: 目标格式 (例如: 'jpg')
        :param delete_original: 转换后是否删除源文件
        """
        if Image is None:
            self.logger.error("Pillow 库未安装或导入失败。请运行 'pip install Pillow' 来安装。")
            return []

        converted_files = []
        files_to_convert = list(Path().glob(source_pattern))

        if not files_to_convert:
            self.logger.info(f"没有找到匹配 '{source_pattern}' 的文件")
            return []

        for file_path in files_to_convert:
            if not file_path.is_file():
                continue

            try:
                new_path = file_path.with_suffix(f".{target_format.lower()}")

                if new_path.exists():
                    self.logger.warning(f"目标文件已存在，跳过: {new_path}")
                    continue

                with Image.open(file_path) as img:
                    # 对于JPEG，如果源图是RGBA（带透明通道），需要转为RGB
                    if img.mode in ("RGBA", "P") and target_format.lower() in ('jpeg', 'jpg'):
                        img = img.convert("RGB")
                    
                    # Pillow 需要 'JPEG' 作为格式名称
                    save_format = 'JPEG' if target_format.lower() in ('jpg', 'jpeg') else target_format.upper()
                    img.save(new_path, format=save_format)

                converted_files.append((str(file_path), str(new_path)))
                self.logger.info(f"已转换: {file_path} -> {new_path}")

                if delete_original:
                    file_path.unlink()
                    self.logger.info(f"已删除源文件: {file_path}")

            except Exception as e:
                self.logger.error(f"转换文件失败 {file_path}: {e}")
        return converted_files