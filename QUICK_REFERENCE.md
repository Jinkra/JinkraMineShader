# 快速参考卡 - JinkraMineShader 插件

## 版本支持
✅ Blender 5.1
✅ Blender 5.0  
✅ Blender 4.1

## 插件部署位置

### Blender 5.1
```
C:\Users\duban\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\mc_shader_loader
```

### Blender 5.0
```
C:\Users\duban\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\mc_shader_loader
```

### Blender 4.1
```
C:\Users\duban\AppData\Roaming\Blender Foundation\Blender\4.1\scripts\addons\mc_shader_loader
```

## 快速启用步骤

### 在 Blender UI 中
1. 编辑 > 偏好设置 (Preferences)
2. 左侧选择"插件"(Add-ons)
3. 搜索"JinkraMineShader"
4. 点击复选框启用

### 在 Python Console 中
```python
import bpy
bpy.ops.preferences.addon_enable(module='mc_shader_loader')
```

## 打开面板

1. 在 3D 视图中按 **N** 键打开侧边栏
2. 找到 "JinkraMineShader" 选项卡
3. 点击打开

## 加载光影包

1. 点击"选择光影包"按钮
2. 选择您的 .zip 光影文件
3. 等待加载完成
4. 在 System Console 查看日志

## 常用快捷键

| 快捷键 | 功能 |
|--------|------|
| N | 打开/关闭侧边栏 |
| F4 | 打开偏好设置 |
| F12 | 渲染预览 |

## System Console 位置

菜单：**Window > Toggle System Console**

用途：查看详细的日志和错误信息

## Python Console 代码片段

### 检查插件是否启用
```python
import bpy
addon = 'mc_shader_loader'
print(addon in bpy.context.preferences.addons)
```

### 运行诊断
```python
exec(open("C:/Users/duban/Desktop/JinkraMineShader/ZIP_DIAGNOSTIC.py").read())
```

### 切换到 EEVEE 渲染器
```python
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
```

## 常见文件位置

| 文件 | 位置 |
|------|------|
| 插件源代码 | `C:\Users\duban\Desktop\JinkraMineShader\mc_shader_loader` |
| 诊断工具 | `C:\Users\duban\Desktop\JinkraMineShader\ZIP_DIAGNOSTIC.py` |
| 使用指南 | `C:\Users\duban\Desktop\JinkraMineShader\BLENDER_USAGE_GUIDE.md` |
| 修复说明 | `C:\Users\duban\Desktop\JinkraMineShader\FINAL_FIX_SUMMARY.md` |

## 光影包格式要求

有效的光影包必须包含：
- `shaders.properties` - 全局配置
- `shaders/` - 着色器目录
- 各种 `.fsh` / `.vsh` 文件

## 支持的光影包

- OptiFine 光影
- Iris 光影
- Complementary 光影
- SEUS 光影
- 其他 MC 标准光影包

## 插件功能

- 📦 加载和解析 MC 光影包 ZIP 文件
- ⚙️ 创建 MC 风格的天空和光照环境
- 🎨 应用 MC 标准 PBR 材质
- 🔧 实时参数调整
- 📊 诊断和日志工具

## 推荐设置

- **渲染器**：EEVEE（推荐）
- **性能**：启用 TAA 抗锯齿
- **精度**：使用浮点精度纹理

---

**最后更新**：2026-06-28
**版本**：1.0.2
