"""
包构建器抽象基类
定义DEB和RPM包构建器的通用接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from core.appimage import AppImageInfo


class PackageBuilder(ABC):
    """包构建器抽象基类"""
    
    def __init__(self, app_info: AppImageInfo, extracted_dir: str):
        """
        初始化包构建器
        
        Args:
            app_info: AppImage信息对象
            extracted_dir: AppImage提取后的目录路径
        """
        self.app_info = app_info
        self.extracted_dir = extracted_dir
        self.build_dir: str = ""
        self.package_config: Dict[str, Any] = {}
    
    @abstractmethod
    def prepare_build_directory(self) -> str:
        """
        准备构建目录
        
        Returns:
            构建目录路径
        """
        pass
    
    @abstractmethod
    def create_package_structure(self) -> None:
        """创建包的目录结构"""
        pass
    
    @abstractmethod
    def copy_application_files(self) -> None:
        """复制应用程序文件到包目录"""
        pass
    
    @abstractmethod
    def generate_metadata_files(self) -> None:
        """生成包的元数据文件"""
        pass
    
    @abstractmethod
    def build_package(self, output_path: str) -> str:
        """
        构建最终的包文件
        
        Args:
            output_path: 输出包文件的路径
        
        Returns:
            生成的包文件路径
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """清理临时文件"""
        pass
    
    def set_package_config(self, config: Dict[str, Any]) -> None:
        """
        设置包配置
        
        Args:
            config: 包配置字典
        """
        self.package_config.update(config)
    
    def get_package_name(self, preserve_case: bool = False) -> str:
        """
        获取包名称（转换为符合规范的格式）
        
        Args:
            preserve_case: 是否保持原始大小写，默认False（转为小写以符合包管理规范）
        
        Returns:
            规范化的包名称
        """
        name = self.app_info.name if preserve_case else self.app_info.name.lower()
        # 移除特殊字符，只保留字母、数字、连字符和下划线
        import re
        if preserve_case:
            name = re.sub(r'[^a-zA-Z0-9\-_]', '-', name)
        else:
            name = re.sub(r'[^a-z0-9\-_]', '-', name)
        # 移除连续的连字符
        name = re.sub(r'-+', '-', name)
        # 移除开头和结尾的连字符
        name = name.strip('-')
        return name or "unknown-app"
    
    def get_display_name(self) -> str:
        """
        获取应用程序的显示名称（保持原始大小写）
        
        Returns:
            原始显示名称
        """
        return self.app_info.name or "Unknown App"
    
    def _detect_system_architecture(self) -> str:
        """
        自动检测系统架构
        
        Returns:
            系统架构字符串
        """
        import platform
        
        # 获取机器架构
        machine = platform.machine().lower()
        
        # 映射到标准架构名称
        arch_mapping = {
            'x86_64': 'amd64',    # 64位 x86
            'amd64': 'amd64',     # 64位 x86 (Windows风格)
            'i386': 'i386',       # 32位 x86
            'i686': 'i386',       # 32位 x86
            'armv7l': 'armhf',    # ARM 32位
            'aarch64': 'arm64',   # ARM 64位
            'arm64': 'arm64',     # ARM 64位 (macOS风格)
        }
        
        return arch_mapping.get(machine, 'amd64')  # 默认返回amd64
    
    def get_architecture(self, package_type: str = 'deb') -> str:
        """
        获取目标架构
        
        Args:
            package_type: 包类型 ('deb' 或 'rpm')
        
        Returns:
            架构字符串
        """
        # 如果配置中指定了架构，使用配置的架构
        if 'architecture' in self.package_config and self.package_config['architecture']:
            return self.package_config['architecture']
        
        # 自动检测系统架构
        detected_arch = self._detect_system_architecture()
        
        # 根据包类型调整架构名称
        if package_type == 'rpm':
            # RPM通常使用x86_64而不是amd64
            if detected_arch == 'amd64':
                return 'x86_64'
            elif detected_arch == 'arm64':
                return 'aarch64'
        
        return detected_arch
    
    def get_package_version(self) -> str:
        """
        获取包版本号
        
        Returns:
            版本号字符串
        """
        version = self.app_info.version
        if not version or version == "":
            version = "1.0.0"
        
        # 确保版本号符合规范
        import re
        # 移除非数字、点、连字符的字符
        version = re.sub(r'[^0-9.\-]', '', version)
        if not version:
            version = "1.0.0"
        
        return version 