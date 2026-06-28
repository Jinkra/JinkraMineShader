"""
UI 模块 - 注册面板和操作符
"""

import bpy
from . import panel


def register():
    """注册 UI 模块"""
    print("[JinkraMineShader] 注册 UI 模块...")
    try:
        panel.register()
        print("[JinkraMineShader] ✓ UI 模块已注册")
    except Exception as e:
        print(f"[JinkraMineShader] ✗ UI 模块注册失败: {e}")
        import traceback
        traceback.print_exc()


def unregister():
    """注销 UI 模块"""
    print("[JinkraMineShader] 注销 UI 模块...")
    try:
        panel.unregister()
        print("[JinkraMineShader] ✓ UI 模块已注销")
    except Exception as e:
        print(f"[JinkraMineShader] ✗ UI 模块注销失败: {e}")
