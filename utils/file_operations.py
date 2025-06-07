"""
文件操作工具模块
提供常用的文件系统操作功能
"""

import os
import shutil
import tempfile
from typing import Optional


def create_temp_dir(prefix: str = "appimage_converter_") -> str:
    """
    创建临时目录
    
    Args:
        prefix: 临时目录名称前缀
    
    Returns:
        临时目录的绝对路径
    """
    return tempfile.mkdtemp(prefix=prefix)


def remove_dir(path: str) -> None:
    """
    删除目录及其所有内容
    
    Args:
        path: 要删除的目录路径
    """
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)


def copy_file(src: str, dst: str) -> None:
    """
    复制文件，保留元数据
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
    """
    shutil.copy2(src, dst)


def copy_tree(src: str, dst: str) -> None:
    """
    递归复制整个目录树
    
    Args:
        src: 源目录路径
        dst: 目标目录路径
    """
    shutil.copytree(src, dst, dirs_exist_ok=True)


def make_dirs(path: str) -> None:
    """
    创建目录，如果父目录不存在则一并创建
    
    Args:
        path: 要创建的目录路径
    """
    os.makedirs(path, exist_ok=True)


def is_executable(path: str) -> bool:
    """
    检查文件是否可执行
    
    Args:
        path: 文件路径
    
    Returns:
        如果文件存在且可执行返回True，否则返回False
    """
    return os.path.isfile(path) and os.access(path, os.X_OK)


def find_file_in_path(filename: str, search_path: str) -> Optional[str]:
    """
    在指定路径下递归查找文件
    
    Args:
        filename: 要查找的文件名
        search_path: 搜索的根目录路径
    
    Returns:
        如果找到文件返回完整路径，否则返回None
    """
    for root, _, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


def get_file_size(path: str) -> int:
    """
    获取文件大小
    
    Args:
        path: 文件路径
    
    Returns:
        文件大小（字节），如果文件不存在返回0
    """
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def ensure_executable(path: str) -> None:
    """
    确保文件具有可执行权限
    
    Args:
        path: 文件路径
    """
    if os.path.isfile(path):
        current_mode = os.stat(path).st_mode
        os.chmod(path, current_mode | 0o755) 