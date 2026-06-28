# 📚 JinkraMineShader 文档索引

## 快速导航

### 🎯 第一次使用？
1. 阅读 [快速开始](#快速开始)
2. 按照 [立即开始](#立即开始) 的 4 步启用
3. 遇到问题？查看 [故障排查](#故障排查)

### 📖 完整文档

| 文档 | 用途 | 适合对象 |
|------|------|---------|
| BLENDER_USAGE_GUIDE.md | 完整的使用指南 | 初级用户 |
| QUICK_REFERENCE.md | 快速参考卡 | 所有用户 |
| PROJECT_COMPLETION_SUMMARY.md | 项目完成总结 | 管理员/开发者 |
| FINAL_FIX_SUMMARY.md | ZIP 错误修复 | 技术人员 |
| ZIP_EXTRACTION_FIXES.md | 故障排查 | 遇到问题的用户 |
| ZIP_DIAGNOSTIC.py | 诊断工具 | 调试 |

---

## 快速开始

### 系统要求
- Blender 5.1（已部署）
- Blender 5.0 或 4.1（需要手动部署）
- Windows 10 或更高版本
- Python 3.9+（Blender 内置）

### 版本支持

| Blender 版本 | 状态 | 部署位置 |
|------------|------|---------|
| 5.1 | ✅ 已部署 | `%APPDATA%\Blender Foundation\Blender\5.1\scripts\addons\mc_shader_loader` |
| 5.0 | ⚠️ 需要部署 | `%APPDATA%\Blender Foundation\Blender\5.0\scripts\addons\mc_shader_loader` |
| 4.1 | ⚠️ 需要部署 | `%APPDATA%\Blender Foundation\Blender\4.1\scripts\addons\mc_shader_loader` |

---

## 立即开始

### 步骤 1：启动 Blender 5.1
```bash
# Windows
"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"
```

### 步骤 2：启用插件
1. 菜单：编辑 (Edit) > 偏好设置 (Preferences)
2. 左侧：插件 (Add-ons)
3. 搜索框：输入 "JinkraMineShader"
4. 勾选：☑️ 复选框启用

### 步骤 3：打开面板
1. 3D 视图窗口内按 **N** 键
2. 右侧侧边栏会出现选项卡
3. 找到 "JinkraMineShader" 选项卡
4. 点击打开

### 步骤 4：加载光影包
1. 面板中找到 "📦 光影包加载" 区域
2. 点击 "选择光影包" 按钮
3. 文件对话框打开到您的桌面
4. 选择一个 `.zip` 光影文件
5. 等待加载完成
6. 查看 "⚙️ 快速操作" 使用其他功能

✨ **完成！** 现在您可以使用 MC 光影了

---

## 常用功能

### 创建 MC 环境
点击 "创建 MC 环境" 按钮，自动生成：
- MC 风格的天空环境
- 太阳光
- 环保照明
- EEVEE 渲染设置

### 创建 MC 材质
1. 在 3D 视图中选中物体（或多个物体）
2. 点击 "创建 MC 材质"
3. 物体将应用 MC 标准 PBR 材质

### 调整参数
加载光影包后，面板会显示光影的参数：
- 曝光度
- 雾浓度
- 昼夜周期
- 色彩分级
- 等等

直接调整滑块即时预览效果

---

## 故障排查

### 问题 1：插件在偏好设置中不显示

**可能原因**：
- Blender 版本不对
- 插件目录路径不对
- Blender 缓存问题

**解决**：
1. 确保使用 Blender 5.1（或其他已部署的版本）
2. 查看插件文件是否在：
   ```
   C:\Users\duban\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\mc_shader_loader
   ```
3. 重启 Blender
4. 运行诊断工具

### 问题 2：启用后面板不显示

**可能原因**：
- 侧边栏没有打开
- 选项卡在其他位置
- 渲染器设置

**解决**：
1. 确保在 3D 视图中按 N 打开侧边栏
2. 向右滑动查看所有选项卡
3. 查找 "JinkraMineShader" 标签

### 问题 3：选择光影包时出错

**可能原因**：
- ZIP 文件格式不正确
- 临时目录权限问题
- 磁盘空间不足

**解决**：
1. 打开 System Console：Window > Toggle System Console
2. 查看详细错误信息
3. 运行诊断工具：
   ```python
   # 在 Python Console 中
   exec(open("C:/Users/duban/Desktop/JinkraMineShader/ZIP_DIAGNOSTIC.py").read())
   ```

### 问题 4：光影包无法加载

**检查清单**：
- ☑️ ZIP 文件是有效的光影包
- ☑️ 包含 `shaders.properties` 文件
- ☑️ 包含 `shaders/` 目录
- ☑️ 使用 EEVEE 或 Cycles 渲染器
- ☑️ 磁盘空间充足

---

## Python Console 代码片段

### 检查插件是否启用
```python
import bpy
addon_name = 'mc_shader_loader'
if addon_name in bpy.context.preferences.addons:
    print(f"✓ {addon_name} 已启用")
else:
    print(f"✗ {addon_name} 未启用")
```

### 启用插件
```python
import bpy
bpy.ops.preferences.addon_enable(module='mc_shader_loader')
print("✓ 插件已启用")
```

### 运行诊断
```python
exec(open("C:/Users/duban/Desktop/JinkraMineShader/ZIP_DIAGNOSTIC.py").read())
```

### 切换到 EEVEE 渲染器
```python
import bpy
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
print("✓ 已切换到 EEVEE")
```

### 获取插件信息
```python
import bpy
addon = bpy.context.preferences.addons.get('mc_shader_loader')
if addon:
    print(f"插件版本：{addon.module}")
    print(f"插件位置：{addon.module_path}")
```

---

## System Console 位置

在 Blender 菜单中：**Window > Toggle System Console**

用途：查看插件日志和错误信息

---

## 文件位置参考

| 内容 | 位置 |
|------|------|
| 插件源代码 | `C:\Users\duban\Desktop\JinkraMineShader\mc_shader_loader` |
| 已部署到 Blender 5.1 | `C:\Users\duban\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\mc_shader_loader` |
| 诊断工具 | `C:\Users\duban\Desktop\JinkraMineShader\ZIP_DIAGNOSTIC.py` |
| 完整使用指南 | `C:\Users\duban\Desktop\JinkraMineShader\BLENDER_USAGE_GUIDE.md` |
| 快速参考 | `C:\Users\duban\Desktop\JinkraMineShader\QUICK_REFERENCE.md` |

---

## 支持的光影包

- OptiFine 光影包
- Iris 光影包
- Complementary 光影包
- SEUS 光影包
- 其他 MC 标准格式光影包

所有光影包必须包含：
- `shaders.properties` 配置文件
- `shaders/` 目录
- `.fsh` / `.vsh` 着色器文件

---

## 常见问题 (FAQ)

**Q: 如何部署到 Blender 5.0 或 4.1？**

A: 复制插件文件夹到对应版本：
```
源：C:\Users\duban\Desktop\JinkraMineShader\mc_shader_loader
目标：C:\Users\duban\AppData\Roaming\Blender Foundation\Blender\{VERSION}\scripts\addons\
```

**Q: 为什么 System Console 没有输出？**

A: 确保：
1. System Console 已打开（Window > Toggle System Console）
2. 插件日志已启用
3. 操作确实触发了插件代码

**Q: 如何卸载插件？**

A: 
1. 编辑 > 偏好设置 > 插件
2. 搜索 JinkraMineShader
3. 取消勾选 ☐ 禁用
4. 保存偏好设置

**Q: 支持 Cycles 渲染器吗？**

A: 部分支持。推荐使用 EEVEE 获得最佳效果。

---

## 版本信息

- **版本**：1.0.2
- **发布日期**：2026-06-28
- **维护者**：Jinkra
- **状态**：✅ 生产就绪

---

## 需要帮助？

1. **快速查找** → QUICK_REFERENCE.md
2. **详细指南** → BLENDER_USAGE_GUIDE.md
3. **遇到错误** → ZIP_EXTRACTION_FIXES.md
4. **技术问题** → FINAL_FIX_SUMMARY.md
5. **运行诊断** → ZIP_DIAGNOSTIC.py

---

**最后更新**：2026-06-28  
**所有文件位置**：`C:\Users\duban\Desktop\JinkraMineShader\`
