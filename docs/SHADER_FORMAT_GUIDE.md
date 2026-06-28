# JinkraMineShader - 光影包支持文档

## 📋 目录
1. [支持的光影包格式](#支持的光影包格式)
2. [光影包检测](#光影包检测)
3. [格式详解](#格式详解)
4. [兼容性指南](#兼容性指南)
5. [常见问题](#常见问题)

---

## 🎨 支持的光影包格式

### OptiFine 光影包

**格式标识**：`shaders.properties` 配置文件

**特点**：
- 被广泛使用的标准格式
- 兼容 MC 1.12.2 及以上版本
- 完整的参数配置系统
- 支持多种渲染技术

**在 JinkraMineShader 中的支持**：
```
✅ Blender 4.0: 完全支持
✅ Blender 4.1: 完全支持 + 高级特性
✅ Blender 5.0: 完全支持 + 新型系统优化
```

**推荐的 OptiFine 光影包**：
- Sildur's Vibrant Shaders
- SEUS (Sonic Ether's Unbelievable Shaders)
- Continuum Shaders
- Complementary Shaders
- BSL Shaders

---

### Iris 着色器包

**格式标识**：`iris.properties` 配置文件

**特点**：
- 现代 Minecraft 着色器标准
- 基于 GLSL 的高性能渲染
- 更好的材质支持
- 优化的性能和视觉效果

**在 JinkraMineShader 中的支持**：
```
⚠️ Blender 4.0: 基础支持（部分功能可能不可用）
✅ Blender 4.1: 完全支持
✅ Blender 5.0: 完全支持 + 新特性优化
```

**推荐的 Iris 光影包**：
- Photographic
- Nostalgia
- Prism
- Rethinking Voxels
- Lush Shaders

---

### 自定义/通用格式

**特点**：
- 基本的 `.properties` 配置
- 灵活的参数系统
- 适合实验和自定义光影

**支持**：
```
✅ Blender 4.0: 支持
✅ Blender 4.1: 支持
✅ Blender 5.0: 支持
```

---

## 🔍 光影包检测

### 自动检测机制

插件会自动识别光影包格式：

```python
from mc_shader_loader.core.shader_version_compat import detect_shader_type

shader_type = detect_shader_type("shader_pack.zip")
# 返回值：
#   "optifine"  - OptiFine 格式
#   "iris"      - Iris 格式
#   "generic"   - 通用格式
#   "unknown"   - 未知格式
```

### 检测过程

```
1. 读取 ZIP 文件内容列表
2. 查找特定的配置文件
3. 识别光影包类型
4. 返回类型和支持的特性
```

### 获取光影包信息

```python
from mc_shader_loader.core.shader_version_compat import get_shader_info

info = get_shader_info("shader_pack.zip")
# 返回：
# {
#     "type": "optifine",
#     "type_name": "OptiFine Shader Pack",
#     "supported_features": ["basic_materials", "pbr_rendering", ...],
#     "is_supported": True
# }
```

---

## 📖 格式详解

### OptiFine 格式结构

```
shader_pack.zip
├── shaders/
│   ├── shaders.properties        # 全局配置
│   ├── shadow.properties         # 阴影配置
│   ├── lighting.properties       # 光照配置
│   ├── block.properties          # 方块配置
│   ├── entity.properties         # 实体配置
│   ├── world.properties          # 世界配置
│   ├── post.properties           # 后处理配置
│   └── program/
│       ├── composite.glsl
│       ├── composite1.glsl
│       ├── final.glsl
│       └── ...其他着色器文件
├── lang/
│   └── en_US.lang
└── assets/
    ├── textures/
    ├── lut/
    └── ...其他资源
```

### Iris 格式结构

```
shader_pack.zip
├── iris.properties               # 全局配置
├── shaders/
│   ├── core/
│   │   ├── gbuffers_terrain.glsl
│   │   ├── gbuffers_textured.glsl
│   │   └── ...其他核心着色器
│   ├── post/
│   │   ├── composite.glsl
│   │   └── final.glsl
│   └── ...其他着色器
└── assets/
    ├── textures/
    └── ...其他资源
```

---

## 🔄 兼容性指南

### 版本兼容性矩阵

```
光影格式\Blender版本    4.0     4.1     5.0
─────────────────────────────────────────
OptiFine            ✅      ✅      ✅
Iris                ⚠️      ✅      ✅
自定义/通用          ✅      ✅      ✅
```

### 功能可用性

#### OptiFine + Blender 4.0
```
✅ 基础 PBR 材质
✅ 昼夜系统
✅ 基础天气效果
✅ 自发光
✗ 高级采样
✗ 复杂环境光
```

#### OptiFine + Blender 4.1
```
✅ 完整 PBR 材质
✅ 高级昼夜系统
✅ 完整天气效果
✅ 高级自发光
✅ 改进的采样
✅ 环境光计算
✗ 新型着色器节点
```

#### OptiFine + Blender 5.0
```
✅ 所有 4.1 功能
✅ 新型着色器节点
✅ 自定义 BSDF
✅ 高级照明
✅ 实时预览优化
```

#### Iris + Blender 4.0
```
⚠️ 基础加载
⚠️ 部分材质预设
✗ 许多高级特性
```

#### Iris + Blender 4.1
```
✅ 完整支持
✅ 所有特性
✅ 优化渲染
```

#### Iris + Blender 5.0
```
✅ 完整支持
✅ 所有特性
✅ 新特性优化
✅ 最佳性能
```

---

## 📋 常见问题

### Q: 我的光影包格式无法识别？

**A**：
1. 确保 ZIP 文件包含 `shaders.properties` 或 `iris.properties`
2. 检查 ZIP 文件未损坏
3. 尝试重新下载光影包
4. 查看 System Console 中的错误消息

### Q: Iris 光影包在 Blender 4.0 中加载但功能受限？

**A**：这是预期行为。Iris 光影包需要 Blender 4.1+ 以获得完整支持。

**建议**：
- 升级到 Blender 4.1 或更新版本
- 或使用 OptiFine 光影包替代

### Q: 如何判断光影包是否被正确识别？

**A**：查看日志消息：
1. 打开 System Console（Window > Toggle System Console）
2. 加载光影包
3. 查看输出信息示例：
   ```
   [JinkraMineShader] 检测到光影包类型：optifine
   [JinkraMineShader] 加载光影包参数...
   ```

### Q: 某个光影包与 Blender 不兼容？

**A**：可能原因：
1. 光影包格式为未知类型
2. Blender 版本过旧
3. 光影包文件损坏

**解决方案**：
1. 检查光影包完整性
2. 升级 Blender 版本
3. 尝试其他光影包

### Q: 光影包加载后效果不对？

**A**：
1. 确认 EEVEE 渲染器已选中
2. 检查材质是否正确应用
3. 验证所有参数已加载
4. 重启插件并重新加载光影包

---

## 🔧 高级：自定义光影包

### 创建兼容的光影包

要使自定义光影包被正确识别，需要包含以下之一：

**Option 1: OptiFine 格式**
```
your_pack.zip
└── shaders/
    └── shaders.properties
```

**Option 2: Iris 格式**
```
your_pack.zip
└── iris.properties
```

**Option 3: 通用格式**
```
your_pack.zip
└── <any_folder>/
    └── any_config.properties
```

### 参数配置示例

**shaders.properties**：
```properties
# 曝光参数
uniform int lightLevel;
uniform float exposure;

# 雾参数
uniform float fogDensity;
uniform float fogStart;

# 天空参数
uniform float skyBrightness;
```

---

## 📚 资源

### 下载光影包的地方

- **CurseForge**: https://www.curseforge.com/minecraft/shaders
- **Shadersmods**: https://www.shadersmods.com/
- **Planet Minecraft**: https://www.planetminecraft.com/

### 光影包文档

- **OptiFine**: https://www.optifine.net/
- **Iris**: https://irisshaders.net/

---

**最后更新**：2026-06-27  
**版本**：JinkraMineShader 1.0.0  
**支持格式**：OptiFine, Iris, 自定义
