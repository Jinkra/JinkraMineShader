'''
JinkraMineShader 验证脚本
在 Blender Python 控制台中运行
'''

import bpy

print("\\n" + "="*60)
print("JinkraMineShader - 验证检查")
print("="*60)

# 检查插件
addon = bpy.context.preferences.addons.get("jinkra_mine_shader_loader")
if addon:
    print("✓ 插件已安装: jinkra_mine_shader_loader")
else:
    print("✗ 插件未找到")

# 检查 Blender 版本
print(f"✓ Blender: {bpy.app.version_string}")

# 检查渲染器
if bpy.context.scene.render.engine == 'BLENDER_EEVEE':
    print("✓ 使用 EEVEE 渲染器")
else:
    print(f"⚠ 当前渲染器: {bpy.context.scene.render.engine}")

print("="*60 + "\\n")

