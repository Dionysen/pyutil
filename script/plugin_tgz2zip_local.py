#!/usr/bin/env python3
"""
插件处理脚本 - 使用工具库处理插件
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from dionysen import archive_ops, file_ops, logger

# 本地插件文件映射
local_plugins = {
    "AI灵感渲染器-1.2.0.5.tgz": "AI灵感渲染器__1.2.0.6",
    "总图排布-1.2.0.2.tgz": "总图排布__1.2.0.3", 
    "总图优化-1.2.0.2.tgz": "总图优化__1.2.0.3",
    "AI助手-1.2.0.1.tgz": "AI助手__1.2.0.2",
    "AI成本估算-1.2.0.3.tgz": "AI成本估算__1.2.0.4",
    "AI智绘立面-1.2.0.1.tgz": "AI智绘立面__1.2.0.2"
}

def process_plugins():
    """处理本地插件文件"""
    logger.info("开始处理本地插件")
    
    # 定义路径
    tmp_dir = Path("tmp")
    dist_dir = tmp_dir / "dist"
    dist_zip_dir = tmp_dir / "distZip"
    
    # 创建输出目录
    dist_dir.mkdir(exist_ok=True)
    dist_zip_dir.mkdir(exist_ok=True)
    
    for tgz_filename, plugin_name in local_plugins.items():
        try:
            logger.info(f"处理插件: {plugin_name}")
            
            # 本地tgz文件路径
            tgz_path = tmp_dir / tgz_filename
            
            if not tgz_path.exists():
                logger.warning(f"文件不存在: {tgz_path}")
                continue
            
            # 解压插件包
            extract_dir = archive_ops.extract_archive(
                tgz_path, 
                dist_dir / plugin_name
            )
            
            # 删除指定文件
            package_dir = Path(extract_dir) / "package"
            files_to_delete = ['index.js', 'package.json', 'checksums.json']
            
            for file in files_to_delete:
                file_path = package_dir / file
                if file_path.exists():
                    file_path.unlink()
                    logger.info(f"已删除: {file}")
            
            # 创建ZIP文件 - 打包package目录中的内容，不包含package父目录
            zip_filename = f"{plugin_name}.zip"
            zip_path = archive_ops.create_archive(
                package_dir, 
                dist_zip_dir / zip_filename,
                include_root=False
            )
            
            logger.info(f"成功处理插件: {plugin_name}")
            
        except Exception as e:
            logger.error(f"处理插件失败 {plugin_name}: {e}")
    
    logger.info("所有插件处理完成")

if __name__ == "__main__":
    process_plugins()