# JinkraMineShader - Blender 5.0 设置指南

## 📋 目录
1. [系统要求](#系统要求)
2. [安装步骤](#安装步骤)
3. [启用插件](#启用插件)
4. [首次使用](#首次使用)
5. [版本适配](#版本适配)
6. [故障排查](#故障排查)

---

## ✅ 系统要求

### 最低要求
- **Blender**: 4.0.0 及以上
- **Python**: 3.10+（Blender 内置）
- **内存**: 4GB（推荐 8GB+）
- **GPU**: NVIDIA/AMD/Intel（用于 EEVEE）

### 推荐配置
- **Blender**: 5.0.0 或更新（完整功能支持）
- **Python**: 3.11+
- **内存**: 16GB
- **GPU**: NVIDIA RTX 系列（最佳性能）

---

## 🚀 安装步骤

### 步骤 1: 确认安装位置

根据你的 Blender 版本，插件应位于：

**Blender 5.0**
```
C:\Users\<用户名>\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\mc_shader_loader\
```

**Blender 4.1**
```
C:\Users\<用户名>\AppData\Roaming\Blender Foundation\Blender\4.1\scripts\addons\mc_shader_loader\
```

**Blender 4.0**
```
C:\Users\<用户名>\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\mc_shader_loader\
```

### 步骤 2: 验证文件结构

确保文件夹包含以下内容：

```
mc_shader_loader/
├── __init__.py              # 插件主文件
├── core/                    # 核心模块
│   ├── zip_parser.py
│   ├── shader_validator.py
│   ├── properties_parser.py
│   ├── version_compat.py    # ★ 版本兼容性
│   └── shader_version_compat.py  # ★ 光影包适配
├── ui/
│   ├── panel.py
│   └── properties.py
├── environment/
│   └── sky_creator.py
├── materials/
│   └── pbr_template.py
├── config/
├── utils/
│   ├── logger.py
│   └── path_helper.py
└── __pycache__/             # 自动生成
```

---

## 🎯 启用插件

### 步骤 1: 打开 Blender

打开你的 Blender 5.0（或其他支持版本）

### 步骤 2: 打开偏好设置

**方法 1**：菜单
- 点击 `编辑` → `偏好设置`

**方法 2**：快捷键
- Windows/Linux: `Ctrl + ,`
- macOS: `Cmd + ,`

### 步骤 3: 进入插件页面

1. 左侧菜单找到 `插件` (Add-ons)
2. 在搜索框输入：`JinkraMineShader`

### 步骤 4: 启用插件

1. 找到 `JinkraMineShader` 条目
2. 点击左侧的复选框启用
3. 看到 ✓ 表示启用成功

### 步骤 5: 查看版本信息

启用后，你会看到：
```
JinkraMineShader v1.0.0
作者：Jinkra
支持版本：Blender 4.0+
```

---

## 🎮 首次使用

### 打开侧边栏

1. 在 3D 视图中按 `N` 打开侧边栏
2. 右上角是选项卡列表
3. 找到 `JinkraMineShader` 选项卡

### 快速操作面板

侧边栏中将显示以下部分：

**📦 光影包管理**
- 选择光影包 ZIP 文件
- 查看加载状态

**⚙️ 快速操作**
- 创建 MC 环境
- 创建 MC 材质
- 应用光影参数

**🔧 设置**
- 时间/天气控制
- 参数调整
- 预设管理

---

## 🔄 版本适配

### Blender 版本功能对比

| 功能 | 4.0 | 4.1 | 5.0 |
|------|-----|-----|-----|
| ZIP 解析 | ✅ | ✅ | ✅ |
| 基础材质 | ✅ | ✅ | ✅ |
| 昼夜系统 | ✅ | ✅ | ✅ |
| 天气模式 | ✅ | ✅ | ✅ |
| 高级修改器 | ❌ | ✅ | ✅ |
| 新型着色器 | ❌ | ❌ | ✅ |

### 自动版本检测

插件会自动检测你的 Blender 版本：

```
启动日志示例：
[JinkraMineShader] 检测到 Blender 5.0.0
[JinkraMineShader] 兼容性检查：✓ 通过
[JinkraMineShader] 已启用所有功能
```

### 光影包兼容性

插件也会自动检测光影包格式：

```
加载光影包时：
[JinkraMineShader] 检测到光影包类型：OptiFine
[JinkraMineShader] 支持的特性：PBR, 昼夜, 天气
```

---

## 🔧 故障排查

### 问题 1：插件未显示在列表中

**可能原因**：
1. 文件未正确放置
2. Python 版本不兼容

**解决方案**：
```
1. 打开 System Console (Window > Toggle System Console)
2. 查看错误信息
3. 确认文件路径正确
4. 重启 Blender
```

### 问题 2：启用后插件无反应

**可能原因**：
1. 版本不兼容
2. 依赖缺失

**解决方案**：
```
1. 打开 System Console
2. 查看错误日志
3. 尝试重新启用
4. 检查 Blender 版本是否为 4.0+
```

### 问题 3：光影包加载失败

**可能原因**：
1. ZIP 文件损坏
2. 光影包格式不支持
3. Blender 版本功能限制

**解决方案**：
```
1. 验证 ZIP 文件完整性
2. 尝试其他光影包
3. 查看 System Console 中的具体错误
4. 升级 Blender 版本（如果需要）
```

### 问题 4：渲染效果不理想

**可能原因**：
1. 材质未正确应用
2. 参数未正确设置
3. 渲染器不是 EEVEE

**解决方案**：
```
1. 确认场景渲染器为 EEVEE
2. 重新应用材质
3. 检查所有参数
4. 尝试重启插件
```

### 问题 5：Blender 4.0 某些功能不可用

**这是预期行为**。某些功能仅在 Blender 4.1+ 中可用。

**解决方案**：
```
升级到 Blender 4.1 或 5.0
```

---

## 📚 详细文档

更多信息请参考：

- **版本适配详情**: [`VERSION_COMPATIBILITY.md`](../docs/VERSION_COMPATIBILITY.md)
- **光影包格式**: [`SHADER_FORMAT_GUIDE.md`](../docs/SHADER_FORMAT_GUIDE.md)
- **使用教程**: [`USAGE.md`](../docs/USAGE.md)
- **系统架构**: [`ARCHITECTURE.md`](../docs/ARCHITECTURE.md)
- **参数参考**: [`PARAMETERS.md`](../docs/PARAMETERS.md)

---

## 💡 最佳实践

### 首次使用建议

1. **使用 OptiFine 光影包**
   - 最广泛支持
   - 功能最完整

2. **从简单项目开始**
   - 单个 MC 方块模型
   - 逐步增加复杂度

3. **使用新 Blender 版本**
   - Blender 5.0 获得最佳性能
   - 所有特性都可用

4. **参考示例预设**
   - 内置预设可以快速开始
   - 适合学习参数用法

### 性能优化

**GPU 选择**：
```
推荐顺序：
1. NVIDIA RTX （最快）
2. AMD RDNA （快速）
3. Intel Arc （中等）
4. CPU 模式 （最慢）
```

**场景优化**：
```
• 降低分辨率进行预览
• 使用更少的采样
• 简化材质复杂度
```

---

## 🎨 下一步

1. ✅ 启用插件
2. ✅ 选择光影包
3. ✅ 创建 MC 环境
4. ✅ 应用材质
5. 🎬 开始创作！

---

**支持的 Blender 版本**：4.0, 4.1, 5.0+  
**当前推荐版本**：Blender 5.0  
**光影包支持**：OptiFine, Iris, 自定义格式

**祝你使用愉快！**🎨
