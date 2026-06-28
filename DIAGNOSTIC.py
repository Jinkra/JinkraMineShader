'''
JinkraMineShader 完整诊断脚本
在 Blender Python 控制台中运行
'''

import bpy
import sys

print("\\n" + "="*60)
print("JinkraMineShader - 完整诊断")
print("="*60)

# 1. 系统信息
print(f"\\nBlender: {bpy.app.version_string}")
print(f"Python: {sys.version.split()[0]}")
print(f"操作系统: {sys.platform}")

# 2. 插件状态
addon = bpy.context.preferences.addons.get("jinkra_mine_shader_loader")
print(f"\\n插件: {'✓ 已安装' if addon else '✗ 未安装'}")

# 3. 模块导入
modules = [
    "jinkra_mine_shader_loader.core.zip_parser",
    "jinkra_mine_shader_loader.ui.panel",
    "jinkra_mine_shader_loader.environment.sky_creator",
]

print("\\n模块:")
for mod in modules:
    try:
        __import__(mod)
        print(f"  ✓ {mod.split('.')[-1]}")
    except:
        print(f"  ✗ {mod.split('.')[-1]}")

# 4. 渲染器
print(f"\\n渲染器: {bpy.context.scene.render.engine}")

print("\\n" + "="*60 + "\\n")

