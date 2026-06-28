"""
JinkraMineShader - Blender 版本兼容性模块

功能：
  1. 检测当前 Blender 版本
  2. 处理不同版本的 API 差异
  3. 提供版本特定的功能调整
"""

import bpy

# 最小支持版本
MIN_BLENDER_VERSION = (4, 0, 0)

# 当前支持的 Blender 版本
SUPPORTED_VERSIONS = [
    (4, 0),
    (4, 1),
    (5, 0),
]

# 版本信息
BLENDER_VERSION = bpy.app.version
BLENDER_MAJOR, BLENDER_MINOR = BLENDER_VERSION[:2]


def get_blender_version():
    """获取当前 Blender 版本 - 返回 (major, minor, patch)"""
    return bpy.app.version


def is_blender_version(major, minor=None):
    """检查是否为特定版本"""
    current_major, current_minor = BLENDER_VERSION[:2]
    
    if minor is None:
        return current_major == major
    else:
        return current_major == major and current_minor == minor


def is_blender_version_or_newer(major, minor=0):
    """检查是否为特定版本或更新"""
    current_version = (BLENDER_MAJOR, BLENDER_MINOR)
    target_version = (major, minor)
    return current_version >= target_version


def is_blender_version_or_older(major, minor=0):
    """检查是否为特定版本或更旧"""
    current_version = (BLENDER_MAJOR, BLENDER_MINOR)
    target_version = (major, minor)
    return current_version <= target_version


def is_supported_version():
    """检查是否为支持的版本"""
    current = (BLENDER_MAJOR, BLENDER_MINOR)
    return current in SUPPORTED_VERSIONS


def get_version_info():
    """获取版本信息字典"""
    major, minor, patch = get_blender_version()
    
    return {
        "version_string": bpy.app.version_string,
        "major": major,
        "minor": minor,
        "patch": patch,
        "full_version": f"{major}.{minor}.{patch}",
        "is_supported": is_supported_version(),
        "min_version": f"{MIN_BLENDER_VERSION[0]}.{MIN_BLENDER_VERSION[1]}.{MIN_BLENDER_VERSION[2]}",
    }


def get_version_specific_settings():
    """获取特定版本的设置"""
    settings = {
        "use_eevee_render": True,
        "node_group_prefix": "JinkraMineShader_",
        "material_prefix": "JinkraMineShader_",
    }
    
    if is_blender_version_or_newer(5, 0):
        settings.update({
            "use_new_shader_system": True,
            "use_bsdf_nodes": True,
        })
    
    if is_blender_version_or_newer(4, 1):
        settings.update({
            "use_advanced_modifiers": True,
        })
    
    return settings


def check_compatibility():
    """检查插件兼容性 - 返回 (是否兼容, 消息文本)"""
    current = get_blender_version()
    
    if current < MIN_BLENDER_VERSION:
        msg = f"JinkraMineShader 要求 Blender {MIN_BLENDER_VERSION[0]}.{MIN_BLENDER_VERSION[1]}+ 版本"
        return False, msg
    
    if not is_supported_version():
        msg = f"JinkraMineShader 该版本可能不被完全支持（{bpy.app.version_string}）"
        return True, msg
    
    return True, f"Blender {bpy.app.version_string} - 兼容"
