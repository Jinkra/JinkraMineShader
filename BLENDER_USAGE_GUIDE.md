# 在 Blender 中启用和使用 JinkraMineShader 插件

## 已支持的 Blender 版本

✅ Blender 5.1（刚部署）
✅ Blender 5.0
✅ Blender 4.1

## 第一步：启用插件

### 方法 1：通过 Blender UI（推荐）

1. **启动 Blender**
   - 打开 Blender 5.1、5.0 或 4.1

2. **打开偏好设置**
   - 菜单：编辑 (Edit) > 偏好设置 (Preferences)
   - 快捷键：在 Blender 窗口中按 `F4`（某些版本）或使用菜单

3. **找到插件标签页**
   - 左侧菜单选择："插件 (Add-ons)"

4. **搜索插件**
   - 搜索框输入："JinkraMineShader" 或 "jinkra"
   - 或输入："MC Shader" 查找 Minecraft 相关插件

5. **启用插件**
   - 找到 "JinkraMineShader" 插件
   - 点击左侧的复选框 ☑️ 启用
   - 应该看到勾选标记和插件详情

### 方法 2：通过 Python Console（备选）

在 Blender Python Console 中运行：

```python
import bpy

# 启用插件
bpy.ops.preferences.addon_enable(module='mc_shader_loader')

# 验证是否启用
addon_name = 'mc_shader_loader'
if addon_name in bpy.context.preferences.addons:
    print(f"✓ {addon_name} 已启用")
else:
    print(f"✗ {addon_name} 启用失败")
```

## 第二步：打开 JinkraMineShader 面板

1. **切换到 3D 视图**
   - 在 Blender 中打开或创建一个 3D 场景

2. **打开侧边栏**
   - 按 `N` 键（或在 3D 视图右上角找到面板按钮）
   - 或菜单：View > Sidebar

3. **找到 JinkraMineShader 选项卡**
   - 右侧侧边栏应该显示多个选项卡
   - 找到标签为 "JinkraMineShader" 的选项卡
   - 点击打开

4. **面板应该显示**
   - 📦 光影包加载区域
   - ⚙️ 快速操作按钮
   - ⚙️ 设置选项

## 第三步：加载光影包

### 步骤

1. **在 JinkraMineShader 面板中**
   - 看到"选择光影包"按钮

2. **点击"选择光影包"**
   - 文件选择对话框将打开
   - 应该默认打开到您的桌面或下载文件夹

3. **选择光影 ZIP 文件**
   - 找到您的 Minecraft 光影包（.zip 文件）
   - 常见的光影包：
     - OptiFine 光影
     - Iris 光影
     - Complementary 光影
     - SEUS 光影
   - 点击打开

4. **等待加载**
   - 面板会显示进度
   - 查看 System Console 查看详细日志

5. **成功加载**
   - 面板会显示"✓ 已加载"
   - 显示参数数量

### 常见光影包格式

合法的 MC 光影包应该包含：
- `shaders.properties` - 全局配置文件
- `shaders/` - 着色器目录
- 各种 .fsh / .vsh 文件

## 第四步：使用插件功能

### 快速操作

在"⚙️ 快速操作"部分：

1. **创建 MC 环境**
   - 点击按钮创建 MC 风格的天空、太阳光和环保光
   - 适用于 EEVEE 渲染器

2. **创建 MC 材质**
   - 先在 3D 视图中选中一个或多个物体
   - 点击"创建 MC 材质"
   - 将为选中物体应用 MC 标准 PBR 材质

### 参数调整

加载光影包后，可以在面板中看到：
- 参数滑块
- 下拉菜单
- 复选框

直接在 UI 中调整这些参数，实时预览效果。

## 故障排查

### 问题 1：找不到插件

**症状**：偏好设置中搜索不到 JinkraMineShader

**解决**：
1. 确保 Blender 版本是 5.1、5.0 或 4.1
2. 检查插件是否部署到正确的位置：
   ```
   C:\Users\duban\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\mc_shader_loader
   ```
3. 重启 Blender

### 问题 2：启用后面板不显示

**症状**：插件已启用但在 3D 视图中看不到面板

**解决**：
1. 确保在 3D 视图中按 N 打开侧边栏
2. 检查是否有 JinkraMineShader 选项卡
3. 如果没有，重启 Blender

### 问题 3：选择光影包时出错

**症状**：选择 ZIP 文件后出现错误信息

**解决**：
1. 打开 System Console：Window > Toggle System Console
2. 查看详细的错误信息
3. 运行诊断工具：
   ```python
   # 在 Python Console 中
   exec(open("C:/Users/duban/Desktop/JinkraMineShader/ZIP_DIAGNOSTIC.py").read())
   ```

### 问题 4：System Console 在哪

**位置**：
- 菜单：Window > Toggle System Console
- 或 Window > System Console
- 会弹出一个黑色的控制台窗口，显示日志

## 在 Python Console 中运行诊断

### 打开 Python Console

1. 菜单：Scripting > Python Console
2. 或在任何编辑器中找到"Python Console"选项卡

### 运行诊断工具

```python
# 方式 1：运行诊断脚本
exec(open("C:/Users/duban/Desktop/JinkraMineShader/ZIP_DIAGNOSTIC.py").read())

# 方式 2：手动测试 ZIP 功能
import tempfile
import os
import zipfile

temp_dir = tempfile.gettempdir()
print(f"✓ 临时目录: {temp_dir}")
print(f"✓ 可写: {os.access(temp_dir, os.W_OK)}")

# 方式 3：验证插件加载
import bpy
if 'mc_shader_loader' in bpy.context.preferences.addons:
    print("✓ JinkraMineShader 插件已启用")
else:
    print("✗ JinkraMineShader 插件未启用")
```

## 重要提示

### 备份

启用插件前建议备份 Blender 项目文件。

### 渲染器要求

- 推荐使用 **EEVEE** 渲染器
- Cycles 渲染器仅部分功能支持
- 插件会自动检测并提示切换

### 性能

- 加载大型光影包可能需要几秒钟
- 第一次解压会稍慢，之后会缓存
- 使用 EEVEE 渲染性能更好

---

**版本**：JinkraMineShader 1.0.2
**支持版本**：Blender 5.1, 5.0, 4.1
**最后更新**：2026-06-28
