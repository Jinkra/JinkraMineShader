"""
JinkraMineShader ZIP 解压诊断工具

用于诊断 ZIP 文件加载和解压的问题
在 Blender Python Console 中运行此脚本
"""

import os
import sys
import tempfile
import zipfile

# 获取临时目录
temp_dir = tempfile.gettempdir()
print(f"[诊断] 系统临时目录: {temp_dir}")
print(f"[诊断] 临时目录可写: {os.access(temp_dir, os.W_OK)}")

# 检查是否可以创建子目录
test_dir = os.path.join(temp_dir, "jinkra_test_dir")
try:
    os.makedirs(test_dir, exist_ok=True)
    print(f"[诊断] 可以在临时目录中创建子目录: ✓")
    os.rmdir(test_dir)
except Exception as e:
    print(f"[诊断] 无法在临时目录中创建子目录: ✗")
    print(f"       错误: {e}")

# 测试 ZIP 解压
print("\n[诊断] 测试 ZIP 解压功能...")

# 创建一个测试 ZIP 文件
import io

test_zip_path = os.path.join(temp_dir, "jinkra_test.zip")
try:
    with zipfile.ZipFile(test_zip_path, 'w') as zf:
        zf.writestr("test.txt", "测试内容")
    print(f"[诊断] 创建测试 ZIP: ✓")
except Exception as e:
    print(f"[诊断] 创建测试 ZIP 失败: ✗")
    print(f"       错误: {e}")
    sys.exit(1)

# 尝试解压测试 ZIP
test_extract_dir = os.path.join(temp_dir, "jinkra_test_extract")
try:
    if os.path.exists(test_extract_dir):
        import shutil
        shutil.rmtree(test_extract_dir, ignore_errors=True)
    
    os.makedirs(test_extract_dir, exist_ok=True)
    
    with zipfile.ZipFile(test_zip_path, 'r') as zf:
        zf.extractall(test_extract_dir)
    
    if os.path.exists(os.path.join(test_extract_dir, "test.txt")):
        print(f"[诊断] 解压测试 ZIP: ✓")
    else:
        print(f"[诊断] 解压测试 ZIP 失败: ✗ (文件不存在)")
except Exception as e:
    print(f"[诊断] 解压测试 ZIP 失败: ✗")
    print(f"       错误: {e}")

# 清理
try:
    import shutil
    os.remove(test_zip_path)
    shutil.rmtree(test_extract_dir, ignore_errors=True)
    print(f"[诊断] 清理测试文件: ✓")
except:
    pass

print("\n[诊断] 如果所有测试都通过，ZIP 解压功能正常")
print("[诊断] 如果有失败的测试，请检查磁盘空间和权限")
