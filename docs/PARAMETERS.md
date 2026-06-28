# JinkraMineShader - 参数和配置参考

## 常见的 Minecraft 光影参数

### 曝光和颜色空间

| 参数 | 类型 | 范围 | 默认 | 说明 |
|------|------|------|------|------|
| exposure | float | 0.1 - 3.0 | 1.0 | 整体曝光度 |
| contrast | float | 0.0 - 2.0 | 1.0 | 对比度调整 |
| saturation | float | 0.0 - 2.0 | 1.0 | 颜色饱和度 |
| rightness | float | 0.0 - 2.0 | 1.0 | 亮度 |
| ibrance | float | 0.0 - 2.0 | 1.0 | 活力（低饱和度区域优先） |

### 雾和大气

| 参数 | 类型 | 范围 | 默认 | 说明 |
|------|------|------|------|------|
| ogDensity | float | 0.0 - 1.0 | 0.5 | 雾浓度 |
| ogEnd | float | 1 - 256 | 64 | 雾消散距离 |
| ogStart | float | 0 - 128 | 0 | 雾开始距离 |
| tmosphericDensity | float | 0.0 - 1.0 | 0.1 | 大气密度 |

### 天空和照明

| 参数 | 类型 | 范围 | 默认 | 说明 |
|------|------|------|------|------|
| skyColorR | float | 0.0 - 1.0 | 0.1 | 天空红色分量 |
| skyColorG | float | 0.0 - 1.0 | 0.5 | 天空绿色分量 |
| skyColorB | float | 0.0 - 1.0 | 1.0 | 天空蓝色分量 |
| sunBrightness | float | 0.0 - 2.0 | 1.0 | 太阳亮度 |
| moonBrightness | float | 0.0 - 1.0 | 0.2 | 月亮亮度 |

### 泛光（Bloom）

| 参数 | 类型 | 范围 | 默认 | 说明 |
|------|------|------|------|------|
| loomStrength | float | 0.0 - 1.0 | 0.8 | 泛光强度 |
| loomThreshold | float | 0.0 - 1.0 | 0.75 | 泛光阈值 |
| loomRadius | float | 0.5 - 5.0 | 2.0 | 泛光半径 |

### 水体

| 参数 | 类型 | 范围 | 默认 | 说明 |
|------|------|------|------|------|
| waterWave | float | 0.0 - 1.0 | 0.5 | 水波强度 |
| waterFrequency | float | 0.1 - 2.0 | 1.0 | 水波频率 |
| waterNormalMapScale | float | 0.1 - 10.0 | 1.0 | 水法线贴图缩放 |
| waterDepth | float | 1 - 64 | 16 | 水深影响 |

### 时间和天气

| 参数 | 类型 | 范围 | 默认 | 说明 |
|------|------|------|------|------|
| daylightCycleMix | float | 0.0 - 1.0 | 0.0 | 昼夜混合（0=使用系统时间） |
| ainStrength | float | 0.0 - 1.0 | 0.0 | 降雨强度 |
| ainDropsSize | float | 0.1 - 2.0 | 1.0 | 雨滴大小 |
| 	hunderStrength | float | 0.0 - 1.0 | 0.0 | 雷电强度 |

### 环保遮蔽（GTAO）

| 参数 | 类型 | 范围 | 默认 | 说明 |
|------|------|------|------|------|
| mbientOcclusionStrength | float | 0.0 - 1.0 | 0.8 | AO 强度 |
| mbientOcclusionDistance | float | 0.1 - 5.0 | 1.0 | AO 距离 |

## EEVEE 兼容的参数映射

在 EEVEE 中，以下 Minecraft 光影参数会被映射到相应的渲染设置：

### 曝光映射

\\\
Minecraft exposure → Blender Scene.render.gamma
\\\

### 泛光映射

\\\
Minecraft bloomStrength → EEVEE.bloom_intensity
Minecraft bloomThreshold → EEVEE.bloom_threshold
Minecraft bloomRadius → EEVEE.bloom_radius
\\\

### 雾映射

\\\
Minecraft fogDensity → World.mist_settings.density
Minecraft fogStart → World.mist_settings.start_distance
Minecraft fogEnd → World.mist_settings.depth
\\\

## 预设 JSON 格式

\\\json
{
  "version": "1.0",
  "metadata": {
    "name": "My Shader Preset",
    "description": "Custom preset for JinkraMineShader",
    "author": "User Name",
    "shader_pack": "Shader Pack Name",
    "created": "2026-06-27T10:30:00",
    "tags": ["bright", "vibrant", "daytime"]
  },
  "rendering": {
    "engine": "EEVEE"
  },
  "parameters": {
    "exposure": 1.2,
    "brightness": 1.1,
    "contrast": 1.0,
    "saturation": 1.1,
    "fogDensity": 0.3,
    "bloomStrength": 0.9,
    "bloomThreshold": 0.7,
    "bloomRadius": 2.5,
    "rainStrength": 0.0,
    "daylightCycleMix": 0.5,
    "skyColorR": 0.1,
    "skyColorG": 0.6,
    "skyColorB": 1.0,
    "sunBrightness": 1.5
  },
  "lighting": {
    "sun_angle": 45,
    "sun_strength": 2.0,
    "ambient_strength": 0.5
  }
}
\\\

## 优化建议

### 性能优化参数

对于低端设备，推荐调整这些参数以提高性能：

- loomStrength: 降低到 0.3-0.5
- ogDensity: 增加到 0.8-1.0（减少需要渲染的距离）
- 禁用或降低 tmosphericDensity
- 禁用或降低 mbientOcclusionStrength

### 视觉质量参数

对于高端设备，推荐这些设置以获得最佳视觉效果：

- loomStrength: 0.8-1.0
- exposure: 1.0-1.5
- saturation: 1.1-1.2
- contrastHigh: 1.2-1.4（如果支持）

## 常见预设模板

### 逼真光影

\\\json
{
  "exposure": 0.9,
  "brightness": 0.95,
  "contrast": 1.1,
  "saturation": 1.0,
  "fogDensity": 0.2,
  "bloomStrength": 0.7,
  "ambientOcclusionStrength": 0.9
}
\\\

### 鲜艳卡通风格

\\\json
{
  "exposure": 1.3,
  "brightness": 1.2,
  "contrast": 1.3,
  "saturation": 1.3,
  "fogDensity": 0.1,
  "bloomStrength": 1.0,
  "ambientOcclusionStrength": 0.3
}
\\\

### 昏暗夜间效果

\\\json
{
  "exposure": 0.5,
  "brightness": 0.4,
  "contrast": 1.2,
  "saturation": 0.9,
  "fogDensity": 0.5,
  "bloomStrength": 0.3,
  "moonBrightness": 0.4
}
\\\

### 阴雨天气

\\\json
{
  "exposure": 0.7,
  "brightness": 0.75,
  "contrast": 1.1,
  "saturation": 0.8,
  "fogDensity": 0.7,
  "rainStrength": 0.8,
  "bloomStrength": 0.4
}
\\\

## 调试参数

启用详细日志后，以下参数将被输出到控制台：

- erbose_logging: 启用详细日志（在偏好设置中配置）
- 所有解析的参数及其识别的类型

## 更新日志

### v1.0.0 (2026-06-27)

- ✓ 初始版本发布
- ✓ 支持 ZIP 包解析和验证
- ✓ 参数自动识别和范围推测
- ✓ EEVEE 环境创建
- ✓ 侧边栏 UI 面板

### 计划功能

- [ ] Cycles 渲染器支持
- [ ] 直接 GLSL 编译支持（可选）
- [ ] 参数预设云同步
- [ ] 高级纹理编辑器
- [ ] 实时参数预览动画

---

**参考文档**: 参考 ARCHITECTURE.md 了解系统设计。

