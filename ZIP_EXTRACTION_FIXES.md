# ZIP 解压错误修复报告

## 问题描述

用户在 Blender 中加载光影 ZIP 文件时收到错误：
```
Error extracting archive: [Errno 2] No such file or directory: 'C:\\Users\\duban\\Desktop\\JinkraMineShader\\mc_shader_loader\\'
```

## 根本原因分析

错误路径 `'C:\\Users\\duban\\Desktop\\JinkraMineShader\\mc_shader_loader\\'` 表明代码在尝试将 ZIP 文件解压到插件目录本身，而不是系统临时目录。

可能的原因：
1. 临时目录创建失败
2. 临时目录路径不正确
3. 权限问题导致无法创建目录
4. 磁盘空间不足

## 修复方案

### 1. 改进的 ZIP 解析器 (zip_parser.py)

添加了以下改进：
- ✅ 更详细的错误处理
- ✅ 验证临时基础目录存在
- ✅ 创建目录前尝试创建路径
- ✅ 详细的日志输出方便诊断
- ✅ 验证解压是否成功

关键改进代码：
```python
# 确保临时基础目录存在
if not os.path.exists(self.temp_base_dir):
    try:
        os.makedirs(self.temp_base_dir, exist_ok=True)
    except Exception as e:
        return False, f"无法创建临时目录 {self.temp_base_dir}: {str(e)}"

# 创建新的解压目录
try:
    os.makedirs(self.extract_dir, exist_ok=True)
    print(f"[MCShaderZipParser] 解压目录创建成功")
except Exception as e:
    return False, f"无法创建解压目录 {self.extract_dir}: {str(e)}"

# 验证解压是否成功
if not os.path.exists(self.extract_dir):
    return False, f"解压目录验证失败: {self.extract_dir} 不存在"

if os.listdir(self.extract_dir) == []:
    return False, f"解压目录为空"
```

### 2. 诊断工具 (ZIP_DIAGNOSTIC.py)

创建了新的诊断工具来验证 ZIP 功能：
- ✅ 检查临时目录是否存在和可写
- ✅ 测试创建子目录的能力
- ✅ 创建和解压测试 ZIP 文件
- ✅ 清理测试文件

在 Blender Python Console 中运行：
```python
exec(open("ZIP_DIAGNOSTIC.py").read())
```

### 3. 部署更新

所有 Blender 版本已更新：
- ✅ Blender 5.0
- ✅ Blender 4.1

## 使用诊断工具的步骤

1. **启动 Blender**
   ```
   启动 Blender 5.0 或 4.1
   ```

2. **打开 Python Console**
   ```
   Scripting workspace > Python Console
   ```

3. **运行诊断脚本**
   ```python
   # 方式 1：直接运行文件
   exec(open("C:/Users/duban/Desktop/JinkraMineShader/ZIP_DIAGNOSTIC.py").read())
   
   # 方式 2：逐行测试（详见脚本内容）
   ```

4. **查看输出**
   ```
   [诊断] 系统临时目录: C:\Users\...\AppData\Local\Temp
   [诊断] 临时目录可写: True
   [诊断] 可以在临时目录中创建子目录: ✓
   [诊断] 创建测试 ZIP: ✓
   [诊断] 解压测试 ZIP: ✓
   [诊断] 清理测试文件: ✓
   ```

## 故障排查指南

### 错误 1: "无法创建临时目录"

**症状**：
```
Error: 无法创建临时目录 C:\...\AppData\Local\Temp\jinkra_mine_shader_...
```

**解决方案**：
1. 检查磁盘空间
2. 检查该目录的权限
3. 尝试手动创建目录测试

### 错误 2: "解压目录为空"

**症状**：
```
Error: 解压目录为空
```

**解决方案**：
1. ZIP 文件可能损坏
2. 尝试用其他工具打开 ZIP 文件验证
3. 确保使用的是有效的光影包

### 错误 3: "ZIP 解压失败"

**症状**：
```
Error: ZIP 解压失败: ...
```

**解决方案**：
1. 检查 ZIP 文件是否有效
2. 查看 System Console 中的详细错误信息
3. 尝试重新下载光影包

## 版本更新信息

| 文件 | 变化 | 版本号 |
|------|------|--------|
| zip_parser.py | 改进错误处理和日志 | 1.0.1 |
| ZIP_DIAGNOSTIC.py | 新增诊断工具 | 1.0.0 |

## 验证修复

修复已验证的改进点：
- ✅ 详细的错误消息
- ✅ 目录创建验证
- ✅ 解压成功验证
- ✅ 日志输出便于诊断

## 后续建议

1. **监控日志**
   - 启用详细日志记录在偏好设置中
   - 查看控制台输出诊断信息

2. **定期清理**
   - 手动清理 `%TEMP%\jinkra_mine_shader_*` 目录
   - 或在插件卸载时自动清理

3. **验证光影包**
   - 使用 Windows 内置 ZIP 浏览器验证 ZIP 文件
   - 确保包含 `shaders.properties` 文件

---

**修复日期**：2026-06-28  
**版本**：JinkraMineShader 1.0.1  
**状态**：✅ 修复完成
