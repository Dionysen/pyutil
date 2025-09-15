
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入 FileOperations 类
from dionysen.modules.file_ops import FileOperations

# 创建实例
file_ops = FileOperations()

# 将当前目录下所有 .jfif 文件转换为 .jpg，并删除原始文件
file_ops.convert_image_format('*.jfif', 'jpg', delete_original = True)

# 如果你只想转换不想删除原始文件
# file_ops.convert_image_format('*.jfif', 'jpg')