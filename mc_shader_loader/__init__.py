bl_info = {
    "name": "JinkraMineShader",
    "description": "Load Minecraft OptiFine/Iris Shaders for Blender",
    "author": "Jinkra",
    "version": (1, 0, 2),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > JinkraMineShader",
    "category": "Render",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

import sys
import os


import bpy
import os
import sys
import shutil
import tempfile
from bpy.props import StringProperty, FloatProperty, IntProperty, EnumProperty, BoolProperty
from bpy.types import AddonPreferences

print(f"\n[JinkraMineShader] 插件正在加载...")

# ============== 全局配置 ==============
ADDON_NAME = bl_info["name"]
ADDON_VERSION = bl_info["version"]


# ============== 偏好设置 ==============
class MCShaderLoaderPreferences(AddonPreferences):
    """插件全局配置"""
    bl_idname = __name__
    
    temp_dir: StringProperty(
        name="Temp Directory",
        description="临时解压目录路径",
        subtype='DIR_PATH',
        default=""
    )
    
    auto_switch_eevee: BoolProperty(
        name="Auto Switch to EEVEE",
        description="如果当前不是 EEVEE 渲染器，自动切换",
        default=True
    )
    
    verbose_logging: BoolProperty(
        name="Verbose Logging",
        description="启用详细日志输出到控制台",
        default=False
    )
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "auto_switch_eevee")
        layout.prop(self, "verbose_logging")


# ============== 注册 ==============
def register():
    """注册插件"""
    print(f"[JinkraMineShader] 开始注册插件 v{ADDON_VERSION}...")
    
    try:
        bpy.utils.register_class(MCShaderLoaderPreferences)
        print("[JinkraMineShader] ✓ 偏好设置已注册")
    except RuntimeError as e:
        print(f"[JinkraMineShader] ⚠️ 偏好设置注册失败: {e}")
    
    # 直接导入子模块，不用 __import__
    modules_to_register = [
        ('mc_shader_loader.core', 'core'),
        ('mc_shader_loader.utils', 'utils'),
        ('mc_shader_loader.config', 'config'),
        ('mc_shader_loader.materials', 'materials'),
        ('mc_shader_loader.environment', 'environment'),
        ('mc_shader_loader.ui', 'ui'),
    ]
    
    for module_path, module_name in modules_to_register:
        try:
            # 使用标准导入而不是相对导入
            module = __import__(module_path, fromlist=[''])
            
            if hasattr(module, 'register'):
                module.register()
                print(f"[JinkraMineShader] ✓ {module_name} 模块已注册")
            else:
                print(f"[JinkraMineShader] ⚠️ {module_name} 没有 register() 函数")
        except Exception as e:
            print(f"[JinkraMineShader] ✗ {module_name} 注册失败: {e}")
    
    print(f"[JinkraMineShader] ✅ 插件注册完成")


def unregister():
    """注销插件"""
    print(f"\n[JinkraMineShader] 开始注销插件...")
    
    modules_to_unregister = [
        ('mc_shader_loader.ui', 'ui'),
        ('mc_shader_loader.environment', 'environment'),
        ('mc_shader_loader.materials', 'materials'),
        ('mc_shader_loader.config', 'config'),
        ('mc_shader_loader.utils', 'utils'),
        ('mc_shader_loader.core', 'core'),
    ]
    
    for module_path, module_name in modules_to_unregister:
        try:
            module = __import__(module_path, fromlist=[''])
            if hasattr(module, 'unregister'):
                module.unregister()
                print(f"[JinkraMineShader] ✓ {module_name} 模块已注销")
        except Exception as e:
            print(f"[JinkraMineShader] ⚠️ {module_name} 注销失败: {e}")
    
    try:
        bpy.utils.unregister_class(MCShaderLoaderPreferences)
        print("[JinkraMineShader] ✓ 偏好设置已注销")
    except RuntimeError as e:
        print(f"[JinkraMineShader] ⚠️ 偏好设置注销失败: {e}")
    
    print(f"[JinkraMineShader] ✅ 插件注销完成")


if __name__ == "__main__":
    register()
