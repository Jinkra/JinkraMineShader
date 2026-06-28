"""
JinkraMineShader - 光影包版本适配模块

功能：
  1. 识别不同的光影包格式
  2. 处理 OptiFine 和 Iris 光影包
  3. 支持多个光影版本
"""

import os
import re
from typing import Tuple, Dict, List


# 光影包类型定义
SHADER_TYPES = {
    "optifine": "OptiFine Shader Pack",
    "iris": "Iris Shader Pack",
    "unknown": "Unknown Shader Format",
}

# 版本检测模式
VERSION_PATTERNS = {
    "optifine": r"shaders\.properties",
    "iris": r"iris\.properties|.+\.glsl",
    "generic": r"\.properties$",
}

# 支持的光影特性
SUPPORTED_FEATURES = {
    "4.0": [
        "basic_materials",
        "pbr_rendering",
        "day_night_cycle",
    ],
    "4.1": [
        "basic_materials",
        "pbr_rendering",
        "day_night_cycle",
        "weather_effects",
    ],
    "5.0": [
        "basic_materials",
        "pbr_rendering",
        "day_night_cycle",
        "weather_effects",
        "advanced_lighting",
        "custom_nodes",
    ],
}


def detect_shader_type(zip_path):
    """检测光影包类型
    
    Args:
        zip_path: ZIP 文件路径
    
    Returns:
        光影包类型字符串
    """
    import zipfile
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            namelist = z.namelist()
            
            # 检查 OptiFine 格式
            if any('shaders.properties' in n for n in namelist):
                return "optifine"
            
            # 检查 Iris 格式
            if any('iris.properties' in n for n in namelist):
                return "iris"
            
            # 检查通用光影格式
            if any(n.endswith('.properties') for n in namelist):
                return "generic"
    
    except Exception:
        pass
    
    return "unknown"


def get_shader_version(shader_type):
    """获取光影包支持的特性版本
    
    Args:
        shader_type: 光影包类型
    
    Returns:
        支持的特性列表
    """
    version_map = {
        "optifine": "4.0",
        "iris": "4.1",
        "generic": "4.0",
        "unknown": "4.0",
    }
    
    version = version_map.get(shader_type, "4.0")
    return SUPPORTED_FEATURES.get(version, [])


def get_shader_info(zip_path):
    """获取光影包信息
    
    Args:
        zip_path: ZIP 文件路径
    
    Returns:
        包含光影信息的字典
    """
    shader_type = detect_shader_type(zip_path)
    features = get_shader_version(shader_type)
    
    return {
        "type": shader_type,
        "type_name": SHADER_TYPES.get(shader_type, "Unknown"),
        "supported_features": features,
        "is_supported": shader_type != "unknown",
    }


def get_compatible_features_for_version(blender_version):
    """获取特定 Blender 版本支持的特性
    
    Args:
        blender_version: Blender 版本字符串 ("4.0", "4.1", "5.0")
    
    Returns:
        特性列表
    """
    return SUPPORTED_FEATURES.get(blender_version, [])


def is_feature_supported(blender_version, feature):
    """检查特定 Blender 版本是否支持某个特性
    
    Args:
        blender_version: Blender 版本
        feature: 特性名称
    
    Returns:
        True 如果支持
    """
    supported = get_compatible_features_for_version(blender_version)
    return feature in supported


def get_shader_compatibility_matrix():
    """获取光影包兼容性矩阵
    
    Returns:
        兼容性信息字典
    """
    return {
        "optifine": {
            "4.0": {"supported": True, "features": SUPPORTED_FEATURES["4.0"]},
            "4.1": {"supported": True, "features": SUPPORTED_FEATURES["4.1"]},
            "5.0": {"supported": True, "features": SUPPORTED_FEATURES["5.0"]},
        },
        "iris": {
            "4.0": {"supported": False, "reason": "Iris requires 4.1+"},
            "4.1": {"supported": True, "features": SUPPORTED_FEATURES["4.1"]},
            "5.0": {"supported": True, "features": SUPPORTED_FEATURES["5.0"]},
        },
    }
