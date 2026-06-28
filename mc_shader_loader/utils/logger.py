"""日志工具模块"""

import sys
import os
from typing import Optional, Tuple, List, Dict, Any


class Logger:
    """简单的日志记录器"""
    
    def info(self, msg: str):
        """输出信息"""
        print(f"[JinkraMineShader] ✓ [INFO] {msg}")
    
    def warning(self, msg: str):
        """输出警告"""
        print(f"[JinkraMineShader] ⚠️ {msg}")
    
    def error(self, msg: str):
        """输出错误"""
        print(f"[JinkraMineShader] ✗ {msg}")
    
    def debug(self, msg: str):
        """输出调试信息"""
        print(f"[JinkraMineShader] DEBUG: {msg}")


class PathHelper:
    """路径工具"""
    
    @staticmethod
    def get_addon_dir():
        """获取插件目录"""
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    @staticmethod
    def get_module_path(module_name: str):
        """获取模块路径"""
        addon_dir = PathHelper.get_addon_dir()
        return os.path.join(addon_dir, module_name.replace('.', os.sep))


# 全局日志记录器实例
logger = Logger()