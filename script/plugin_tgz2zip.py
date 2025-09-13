#!/usr/bin/env python3
"""
插件处理脚本 - 使用工具库处理插件
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from dionysen import download_ops, archive_ops, file_ops, logger

# 插件数据
plugins = [
    {
        "icon": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/client/icons/optimization/optimization.png",
        "name": "AI灵感渲染器",
        "sort": 1,
        "description": "按照您的想法自动渲染效果图",
        "url": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/plugins/dev/AI灵感渲染器-1.2.0.5.tgz"
    },
    {
        "icon": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/client/icons/GD/GD.png",
        "name": "总图排布",
        "sort": 2,
        "description": "按照分区业态一键生成总图方案",
        "url": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/plugins/dev/总图排布-1.1.0.2.tgz"
    },
    {
        "icon": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/client/icons/optimization/optimization.png",
        "name": "总图优化",
        "sort": 3,
        "description": "通过优化楼栋的层数和位置，使方案更加贴合指标与规范",
        "url": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/plugins/dev/总图优化-1.1.0.2.tgz"
    },
    {
        "icon": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/client/icons/optimization/optimization.png",
        "name": "AI助手",
        "sort": 4,
        "description": "AI助手",
        "url": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/plugins/dev/AI助手-0.0.1.83.tgz"
    },
    {
        "icon": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/plugins/dev/场地定位.png",
        "name": "场地定位",
        "sort": 5,
        "description": "快速定位用地, 条件设置",
        "url": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/plugins/dev/场地定位-1.0.0.0.tgz"
    },
    {
        "icon": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/plugins/dev/AI成本估算.png",
        "name": "AI成本估算",
        "sort": 6,
        "description": "上传经济技术指标表快速估算成本",
        "url": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/plugins/dev/AI成本估算-0.0.0.15.tgz"
    },
    {
        "icon": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/client/icons/optimization/optimization.png",
        "name": "AI智绘立面",
        "sort": 1.1,
        "description": "",
        "url": "https://gaid-data.obs.cn-north-4.myhuaweicloud.com/IDE/plugins/dev/AI智绘立面-1.1.0.3.tgz"
    }
]

def process_plugins():
    """处理所有插件"""
    logger.info("开始处理插件")
    
    # 创建输出目录
    dist_dir = Path("tmp") / "dist"
    dist_zip_dir = Path("tmp") / "distZip" 
    dist_dir.mkdir(exist_ok=True)
    dist_zip_dir.mkdir(exist_ok=True)
    
    for plugin in plugins:
        try:
            logger.info(f"处理插件: {plugin['name']}")
            
            # 下载图标
            icon_path = download_ops.download_file(
                plugin['icon'], 
                dist_zip_dir / f"{plugin['name']}.png"
            )
            
            # 下载插件包
            tgz_path = download_ops.download_file(
                plugin['url'], 
                dist_dir / Path(plugin['url']).name
            )
            
            # 解压插件包
            extract_dir = archive_ops.extract_archive(
                tgz_path, 
                dist_dir / plugin['name']
            )
            
            # 删除指定文件
            package_dir = Path(extract_dir) / "package"
            files_to_delete = ['index.js', 'package.json', 'checksums.json']
            
            for file in files_to_delete:
                file_path = package_dir / file
                if file_path.exists():
                    file_path.unlink()
                    logger.info(f"已删除: {file}")
            
            # 创建ZIP文件
            zip_filename = f"{plugin['name']}.zip"
            zip_path = archive_ops.create_archive(
                package_dir, 
                dist_zip_dir / zip_filename
            )
            
            logger.info(f"成功处理插件: {plugin['name']}")
            
        except Exception as e:
            logger.error(f"处理插件失败 {plugin['name']}: {e}")
    
    logger.info("所有插件处理完成")

if __name__ == "__main__":
    process_plugins()