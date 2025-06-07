"""
命令执行工具模块
提供安全执行外部命令的功能
"""

import subprocess
import os
from typing import Tuple, List, Optional


def execute_command(command: List[str], cwd: Optional[str] = None, shell: bool = False) -> Tuple[int, str, str]:
    """
    执行外部命令并捕获输出
    
    Args:
        command: 命令及其参数的列表，例如 ['ls', '-l']
        cwd: 命令执行的工作目录，None表示使用当前目录
        shell: 是否通过shell执行命令（出于安全考虑，默认False）
    
    Returns:
        元组 (返回码, 标准输出, 标准错误输出)
    """
    try:
        process = subprocess.run(
            command,
            cwd=cwd,
            shell=shell,
            capture_output=True,
            text=True,  # 以文本模式捕获输出
            check=False  # 不抛出异常，而是返回非零返回码
        )
        return process.returncode, process.stdout, process.stderr
    except FileNotFoundError:
        return -1, "", f"错误：命令 '{command[0]}' 未找到。请确保它已安装并在PATH环境变量中。"
    except Exception as e:
        return -1, "", f"执行命令时发生未知错误：{e}"


def check_command_exists(command: str) -> bool:
    """
    检查系统中是否存在指定命令
    
    Args:
        command: 要检查的命令名称
    
    Returns:
        如果命令存在返回True，否则返回False
    """
    return_code, _, _ = execute_command(['which', command])
    return return_code == 0


def get_command_version(command: str, version_flag: str = '--version') -> Optional[str]:
    """
    获取命令的版本信息
    
    Args:
        command: 命令名称
        version_flag: 获取版本的参数，默认为 '--version'
    
    Returns:
        版本字符串，如果获取失败返回None
    """
    return_code, stdout, stderr = execute_command([command, version_flag])
    if return_code == 0:
        return stdout.strip()
    return None 