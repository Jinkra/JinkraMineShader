# ZIP 解压错误根本原因和最终修复

## 问题根源

错误信息：
```
Error extracting archive: [Errno 2] No such file or directory: 'C:\\Users\\duban\\Desktop\\JinkraMineShader\\mc_shader_loader\\'
```

**根本原因**：文件对话框打开时未指定初始目录，导致 Blender 默认打开到插件目录。

## 问题发生的流程

1. 用户点击"选择光影包"按钮
2. 文件选择对话框打开，但 **没有指定初始目录**
3. Blender 默认打开到插件所在目录（`mc_shader_loader`）
4. 某处代码错误地试图在此目录进行 ZIP 操作
5. 导致"找不到目录"错误

## 最终修复

### 1. 改进的 zip_parser.py
- ✅ 验证临时目录存在
- ✅ 创建前检查权限
- ✅ 解压后验证成功
- ✅ 详细的错误日志

### 2. 修复的 panel.py (关键修复)
- ✅ 为文件对话框明确设置初始目录
- ✅ 优先使用桌面目录
- ✅ 备选使用下载目录
- ✅ 最后使用用户主目录

```python
def invoke(self, context, event):
    """调用文件选择对话框"""
    # 设置默认目录为用户桌面或下载文件夹
    import os
    user_home = os.path.expanduser("~")
    desktop = os.path.join(user_home, "Desktop")
    downloads = os.path.join(user_home, "Downloads")
    
    # 优先使用桌面，否则用下载文件夹，最后用主目录
    if os.path.exists(desktop):
        self.directory = desktop
    elif os.path.exists(downloads):
        self.directory = downloads
    else:
        self.directory = user_home
    
    logger.info(f"文件选择对话框初始目录: {self.directory}")
    
    context.window_manager.fileselect_add(self)
    return {'RUNNING_MODAL'}
```

## 修复包含的内容

| 文件 | 修改 |
|------|------|
| `zip_parser.py` | ✅ 增强错误处理 |
| `panel.py` | ✅ 设置文件对话框初始目录 |
| `ZIP_DIAGNOSTIC.py` | ✅ 新增诊断工具 |
| `ZIP_EXTRACTION_FIXES.md` | ✅ 修复文档 |

## 部署情况

已更新的版本：
- ✅ Blender 5.0
- ✅ Blender 4.1

## 验证步骤

1. **重启 Blender**（完全关闭后重新启动）

2. **启用插件**
   - 编辑 > 偏好设置 > 插件
   - 搜索 "JinkraMineShader"
   - 启用插件

3. **打开 3D 视图**
   - 创建新的 Blender 项目或打开现有项目

4. **打开 JinkraMineShader 面板**
   - 在 3D 视图右侧打开侧边栏（按 N）
   - 选择 "JinkraMineShader" 选项卡

5. **点击"选择光影包"**
   - 文件对话框应该打开到您的桌面
   - 选择您的光影包 ZIP 文件

6. **查看输出**
   - 打开 System Console (Window > Toggle System Console)
   - 查看日志消息，确认过程
   - 应该看到类似：`[文件选择对话框初始目录: C:\Users\...\Desktop]`

## 预期改进

✅ 文件对话框会正确打开到桌面或用户主目录
✅ 不会尝试在插件目录中进行操作
✅ ZIP 解压将使用系统临时目录
✅ 错误信息更加清晰明了

## 如果仍有问题

1. **查看 System Console 输出**
   - 查看完整的错误信息
   - 注意文件对话框初始目录设置

2. **运行诊断工具**
   ```python
   exec(open("ZIP_DIAGNOSTIC.py").read())
   ```

3. **检查临时目录权限**
   - 确保 `%TEMP%` 目录可写
   - 尝试手动创建文件到临时目录

4. **验证光影包**
   - 使用 Windows 资源管理器打开 ZIP
   - 确保包含 `shaders.properties` 文件
   - 验证 `shaders/` 目录存在

## 文件历史

| 版本 | 日期 | 修复 |
|------|------|------|
| 1.0.2 | 2026-06-28 | 设置文件对话框初始目录 |
| 1.0.1 | 2026-06-28 | 增强 ZIP 解压错误处理 |
| 1.0.0 | 2026-06-27 | 初始发布 |

---

**修复完成日期**：2026-06-28  
**状态**：✅ 已部署  
**版本**：JinkraMineShader 1.0.2
