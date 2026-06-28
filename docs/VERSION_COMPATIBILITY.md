# JinkraMineShader - 版本适配文档

## 📋 目录
1. [Blender 版本支持](#blender-版本支持)
2. [光影包版本支持](#光影包版本支持)
3. [版本兼容性矩阵](#版本兼容性矩阵)
4. [已知问题和限制](#已知问题和限制)
5. [升级指南](#升级指南)

---

## 🎯 Blender 版本支持

### 官方支持版本

| 版本 | 状态 | 功能完整性 | 备注 |
|------|------|----------|------|
| **Blender 4.0** | ✅ 完全支持 | 100% | 基础版本，所有核心功能可用 |
| **Blender 4.1** | ✅ 完全支持 | 100% | 推荐版本，包含高级修改器支持 |
| **Blender 5.0** | ✅ 完全支持 | 100% | 最新版本，新型着色器系统支持 |

### 功能支持对比

#### Blender 4.0
```
✓ ZIP 光影包解析
✓ 基础 PBR 材质
✓ EEVEE 环保光系统
✓ 昼夜时间系统
✓ 天气模式切换
✓ 自发光模拟
✗ 高级修改器（4.1+ 功能）
✗ 新型着色器系统（5.0+ 功能）
```

#### Blender 4.1
```
✓ ZIP 光影包解析
✓ 基础 PBR 材质
✓ EEVEE 环保光系统
✓ 昼夜时间系统
✓ 天气模式切换
✓ 自发光模拟
✓ 高级修改器支持
✓ 节点组优化
✗ 新型着色器系统（5.0+ 功能）
```

#### Blender 5.0
```
✓ ZIP 光影包解析
✓ 基础 PBR 材质
✓ EEVEE 环保光系统
✓ 昼夜时间系统
✓ 天气模式切换
✓ 自发光模拟
✓ 高级修改器支持
✓ 节点组优化
✓ 新型着色器系统
✓ 自定义 BSDF 节点
✓ 高级照明计算
```

### 最低要求

- **Blender 4.0.0** 及以上
- **Python 3.10+**（Blender 内置）
- **64 位操作系统**

---

## 🎨 光影包版本支持

### 支持的光影包格式

#### OptiFine 光影包
```
特性：
  • 标准的 shaders.properties 配置
  • 兼容 MC 1.12.2 - 最新版本
  • 广泛使用的格式

支持版本：
  Blender 4.0+: 完全支持
  Blender 4.1+: 完全支持 + 高级特性
  Blender 5.0+: 完全支持 + 新型系统
```

#### Iris 着色器包
```
特性：
  • iris.properties 配置格式
  • 现代 Minecraft 版本优化
  • 更好的性能和视觉效果

支持版本：
  Blender 4.0: 基础支持（功能受限）
  Blender 4.1+: 完全支持
  Blender 5.0+: 完全支持 + 优化
```

### 功能对比表

| 光影格式 | 4.0 | 4.1 | 5.0 | 推荐版本 |
|---------|-----|-----|-----|---------|
| OptiFine | ✅ | ✅ | ✅ | 4.1+ |
| Iris | ⚠️ | ✅ | ✅ | 5.0 |
| 自定义 | ✅ | ✅ | ✅ | 5.0 |

---

## 📊 版本兼容性矩阵

### Blender × 光影包兼容性

```
                OptiFine  Iris  自定义
Blender 4.0      ✅       ⚠️     ✅
Blender 4.1      ✅       ✅     ✅
Blender 5.0      ✅       ✅     ✅

✅ 完全支持
⚠️ 部分支持（功能可能受限）
❌ 不支持
```

### 特性可用性矩阵

```
特性\版本           4.0    4.1    5.0
───────────────────────────────────
ZIP 解析            ✅     ✅     ✅
基础材质            ✅     ✅     ✅
昼夜系统            ✅     ✅     ✅
天气模式            ✅     ✅     ✅
高级修改器          ❌     ✅     ✅
自定义节点          ❌     ⚠️     ✅
新型着色器          ❌     ❌     ✅
```

---

## ⚠️ 已知问题和限制

### Blender 4.0 的限制

```
• 不支持某些高级修改器
• 节点组性能略低
• 某些材质预设在高复杂度下可能卡顿
```

**解决方案**：升级到 Blender 4.1 或更新

### Iris 着色器在 Blender 4.0 中的限制

```
• 某些 GLSL 特性无法完全复现
• 高级采样可能导致性能问题
• 某些视觉效果可能不准确
```

**解决方案**：使用 Blender 4.1+ 或选择 OptiFine 光影包

### Blender 5.0 的已知问题

```
• 某些旧式节点在新系统中行为不同
• 需要重新烘焙某些贴图
```

**解决方案**：按照下方升级指南进行操作

---

## 🚀 升级指南

### 从 Blender 4.0 升级到 4.1

#### 步骤 1：备份
```
1. 导出当前的光影配置预设
   侧边栏 > JinkraMineShader > 导出预设
2. 保存当前项目文件
```

#### 步骤 2：安装 Blender 4.1
```
1. 下载 Blender 4.1
2. 安装到系统中
```

#### 步骤 3：迁移插件
```
1. 将 mc_shader_loader 复制到 Blender 4.1 的 addons 目录
2. 重启 Blender 4.1
3. 启用插件
```

#### 步骤 4：恢复配置
```
1. 打开 Blender 4.1 项目
2. 侧边栏 > JinkraMineShader > 导入预设
3. 选择之前导出的预设文件
```

### 从 Blender 4.1 升级到 5.0

#### 步骤 1：备份
```
1. 导出预设文件
2. 保存所有项目
```

#### 步骤 2：安装 Blender 5.0
```
1. 下载 Blender 5.0
2. 安装到系统中
```

#### 步骤 3：迁移
```
1. 复制插件
2. 重启 Blender 5.0
3. 启用插件
4. 恢复预设
```

#### 步骤 4：验证
```
1. 打开测试项目
2. 应用光影包
3. 检查渲染效果
4. 验证所有功能可用
```

### 自动版本检测

插件会自动检测你的 Blender 版本并调整功能：

```python
# 自动进行
from mc_shader_loader.core.version_compat import get_blender_version

version = get_blender_version()
# 返回：(4, 1, 0) 对于 Blender 4.1
```

---

## 📚 高级：版本检查 API

### 检查 Blender 版本

```python
from mc_shader_loader.core.version_compat import (
    is_blender_version,
    is_blender_version_or_newer,
    get_blender_version,
)

# 检查特定版本
if is_blender_version(5, 0):
    print("运行在 Blender 5.0")

# 检查版本或更新
if is_blender_version_or_newer(4, 1):
    # 使用 Blender 4.1+ 特性
    pass

# 获取完整版本
version = get_blender_version()
print(f"Blender {version[0]}.{version[1]}.{version[2]}")
```

### 检查光影包兼容性

```python
from mc_shader_loader.core.shader_version_compat import (
    detect_shader_type,
    get_shader_info,
)

# 检测光影包类型
shader_type = detect_shader_type("/path/to/shader.zip")
# 返回：'optifine' 或 'iris' 或 'generic'

# 获取详细信息
info = get_shader_info("/path/to/shader.zip")
print(info["type"])  # 光影包类型
print(info["supported_features"])  # 支持的特性列表
```

---

## 🔧 故障排查

### 问题：插件在 Blender 5.0 中不工作

**解决方案**：
1. 打开 System Console（Window > Toggle System Console）
2. 查看是否有错误信息
3. 确认插件已启用
4. 尝试重新启用插件

### 问题：Iris 光影包在 Blender 4.0 中加载失败

**解决方案**：
1. 升级到 Blender 4.1+
2. 或使用 OptiFine 光影包替代

### 问题：升级后某些节点不工作

**解决方案**：
1. 清除缓存（菜单 > 编辑 > 清除缓存）
2. 重新加载光影包
3. 重新应用材质

---

## 📞 支持和反馈

- 遇到版本问题？查看此文档的"故障排查"部分
- 需要功能请求？考虑升级到 Blender 5.0
- 发现 Bug？检查 System Console 中的错误日志

---

**最后更新**：2026-06-27  
**版本**：JinkraMineShader 1.0.0  
**Blender 支持**：4.0 - 5.0+
