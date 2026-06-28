# JinkraMineShader - 架构设计文档

## 概述

JinkraMineShader 采用模块化架构，将 Minecraft 光影包的解析、验证、环境创建和材质生成等功能分离为独立模块，便于维护和扩展。

## 核心设计原则

1. **模块化**: 每个功能独立成模块，职责单一
2. **无依赖**: 仅使用 Blender 官方 API，无第三方二进制依赖
3. **资源隔离**: 所有生成资源加 MC_SHADER_ 前缀，避免冲突
4. **错误处理**: 统一的异常处理和用户友好的错误消息
5. **可扩展**: 预留接口便于添加新功能

## 模块架构

### 1. 核心模块 (core/)

负责文件解析、验证和参数提取。

#### zip_parser.py - ZIP 包解析

**职责**:
- 解压 ZIP 光影包到临时目录
- 提取 shaders.properties 配置
- 读取预设和纹理资源

**关键类**:
- MCShaderZipParser: 主解析类
  - extract_zip(): 解压并验证 ZIP
  - get_shaders_properties(): 读取配置文件
  - get_preset_files(): 列出预设文件
  - get_texture_files(): 分类纹理资源

**流程**:
\\\
ZIP 文件
  ↓
[解压] extract_zip()
  ↓
临时目录
  ↓
[验证] validate_shader_pack()
  ↓
[读取配置] get_shaders_properties()
  ↓
配置字典
\\\

#### shader_validator.py - 光影包验证

**职责**:
- 检查 ZIP 包是否为合法光影包
- 验证必需文件和目录
- 生成详细验证报告

**关键类**:
- MCShaderValidator: 验证器
  - alidate_all(): 执行完整验证
  - 返回 ShaderValidationReport

**验证清单**:
- ✓ 必需文件: shaders.properties
- ✓ 必需目录: shaders/
- ✓ 着色器文件: 至少一个 .vsh 或 .fsh
- ✓ 配置格式: 有效的键值对

#### properties_parser.py - 参数解析

**职责**:
- 解析 .properties 格式配置文件
- 识别参数类型（float、int、bool、enum）
- 推测合理的参数范围
- 生成 Blender 属性定义

**关键类**:
- ShaderProperty: 单个参数定义
  - parse_value(): 识别参数类型
  - guess_ranges(): 推测范围
  - 	o_dict(): 序列化为字典

- PropertiesParser: 配置文件解析器
  - parse(): 解析所有参数
  - get_sorted_properties(): 排序输出
  - export_to_json(): JSON 导出

### 2. UI 模块 (ui/)

负责 Blender 侧边栏面板和用户交互。

#### panel.py - 侧边栏面板

**职责**:
- 提供光影包选择 UI
- 显示参数调整控件
- 提供快速操作按钮

**关键类**:
- MC_ShaderPanel: 主面板（VIEW3D_PT_jinkra_mine_shader）
- MC_ShaderLoaderOperator: 文件选择操作符
- MC_ShaderCreateEnvironmentOperator: 环境创建操作符
- MC_ShaderCreateMaterialOperator: 材质创建操作符

**UI 布局**:
\\\
┌─ JinkraMineShader ─────┐
│ 📦 光影包加载           │
│ ├─ [选择光影包] 按钮    │
│ ├─ ✓ 已加载信息          │
│ └─ [重新加载] 按钮      │
├─────────────────────────┤
│ ⚙️ 快速操作              │
│ ├─ [创建 MC 环境] 按钮   │
│ └─ [创建 MC 材质] 按钮   │
├─────────────────────────┤
│ 🎛️ 参数调整             │
│ ├─ 曝光: ━━●━━         │
│ ├─ 亮度: ━━●━━         │
│ ├─ 对比度: ━━●━━       │
│ ├─ 雾浓度: ━━●━━       │
│ └─ ...                  │
├─────────────────────────┤
│ ⚙️ 设置                 │
│ ├─ [✓] 自动切换 EEVEE   │
│ └─ [✓] 详细日志         │
└─────────────────────────┘
\\\

### 3. 环境模块 (environment/)

负责光照、天空、昼夜和天气系统。

#### sky_creator.py - 天空和光照

**职责**:
- 创建 MC 风格的天空世界
- 生成太阳和环保光
- 配置 EEVEE 渲染参数
- 管理昼夜系统
- 控制天气模式

**关键类**:
- MCEnvironmentCreator: 环境创建
  - create_world_environment(): 创建天空
  - create_sun_light(): 创建太阳
  - create_ambient_light(): 创建环保光
  - setup_eevee_render_settings(): 配置 EEVEE

- DayNightController: 昼夜控制
  - set_time(hour): 设置时间（0-24）
  - _update_sky_color(): 更新天空颜色

- WeatherController: 天气控制
  - set_weather(mode): 切换天气模式

**时间系统**:
\\\
时间 (小时)  │ 天空颜色   │ 太阳强度 │ 说明
─────────────┼────────────┼──────────┼─────────
0:00 - 6:00  │ 深蓝/黑色  │ 0.0      │ 夜间
6:00 - 8:00  │ 渐进       │ 递增     │ 日出
8:00 - 18:00 │ 浅蓝       │ 2.0      │ 白天
18:00 - 20:00│ 橙/紫色    │ 递减     │ 日落
20:00 - 24:00│ 深蓝/黑色  │ 0.0      │ 傍晚/夜间
\\\

### 4. 材质模块 (materials/)

负责 PBR 材质创建和 EEVEE 节点组。

#### pbr_template.py - PBR 材质模板

**职责**:
- 为 MC 方块创建标准 PBR 材质
- 支持漫反射、法线、粗糙度、金属度
- 模拟 MC 方块自发光亮度（0-15级）

**材质结构**:
\\\
纹理输入
  ├─ BaseColor (漫反射贴图)
  ├─ Normal (法线贴图)
  ├─ Roughness (粗糙度贴图)
  ├─ Metallic (金属度贴图)
  └─ Emission (自发光贴图)
    ↓
[PBR 着色器节点]
    ↓
EEVEE 输出
\\\

#### 
ode_groups.py - EEVEE 合成节点

**职责**:
- 创建可复用的 EEVEE 节点组
- 实现泛光、色彩分级、雾、TAA 等效果

**预定义节点组**:
- MC_SHADER_Bloom: 泛光效果
- MC_SHADER_ColorGrade: 色彩分级
- MC_SHADER_Fog: 体积雾
- MC_SHADER_Atmosphere: 大气层
- MC_SHADER_Vignette: 暗角

### 5. 配置模块 (config/)

负责预设管理和配置序列化。

#### preset_manager.py - 预设管理

**职责**:
- 导出/导入光影配置预设
- 保存参数状态为 JSON
- 管理预设文件

**预设格式** (JSON):
\\\json
{
  "version": "1.0",
  "name": "My Preset",
  "timestamp": "2026-06-27T10:30:00",
  "parameters": {
    "exposure": 1.2,
    "brightness": 1.0,
    "fogDensity": 0.5,
    "rainStrength": 0.0,
    ...
  }
}
\\\

### 6. 工具模块 (utils/)

负责公共工具和日志系统。

#### logger.py - 日志系统

**职责**:
- 统一日志输出
- 跨平台颜色/符号支持
- 异常处理和友好错误消息

**日志级别**:
- DEBUG (◆): 调试信息
- INFO (✓): 正常信息
- WARNING (⚠): 警告
- ERROR (✗): 错误
- CRITICAL (⚡): 关键错误

## 数据流

### 完整的加载流程

\\\
用户选择 ZIP 文件
  ↓
[MC_ShaderLoaderOperator.invoke()]
  ↓
[MC_ShaderZipParser.extract_zip()]
  ↓ 解压到临时目录
  ↓
[MC_ShaderValidator.validate_all()]
  ↓ 生成验证报告
  ↓
[MC_ShaderZipParser.get_shaders_properties()]
  ↓ 读取 shaders.properties
  ↓
[PropertiesParser.parse()]
  ↓ 解析参数
  ↓
[存储到 scene 上下文]
  ↓
[更新 UI 面板]
  ↓
[用户操作: 创建环境/材质]
  ↓
[调用 MCEnvironmentCreator]
  ↓
[生成场景对象]
\\\

## 性能优化

1. **延迟加载**: 纹理和预设只在需要时加载
2. **临时文件**: 自动清理解压文件（插件卸载时）
3. **缓存**: 解析结果存储在内存中
4. **参数优化**: 仅同步必要的参数到 EEVEE

## 扩展点

### 添加新的参数类型

在 properties_parser.py 中修改 ShaderProperty.parse_value():

\\\python
def parse_value(self):
    # ... 现有代码
    # 添加新的类型识别逻辑
\\\

### 添加新的材质节点

在 materials/node_groups.py 中添加新函数：

\\\python
def create_custom_node_group():
    group = bpy.data.node_groups.new("MC_SHADER_Custom", 'CompositorNodeTree')
    # ... 构建节点
    return group
\\\

### 添加新的天气模式

在 environment/sky_creator.py 中修改 WeatherController.WEATHER_MODES:

\\\python
WEATHER_MODES = {
    "custom_weather": {
        "fog_density": 0.02,
        "exposure": 0.9,
        "rain_strength": 0.3,
    }
}
\\\

## 依赖关系图

\\\
panel.py
  ├─→ zip_parser.py
  ├─→ shader_validator.py
  ├─→ properties_parser.py
  ├─→ sky_creator.py
  ├─→ pbr_template.py
  └─→ logger.py
      ├─→ path_helper (utils)
      └─→ exception_handler (utils)
\\\

## 命名规范

- **插件资源前缀**: MC_SHADER_ （世界、灯光、材质、节点组）
- **操作符 ID**: mc_shader.* （如 mc_shader.load_shader_pack）
- **类名**: PascalCase （如 MCShaderZipParser）
- **方法/函数**: snake_case （如 extract_zip）
- **常量**: UPPER_SNAKE_CASE （如 PREFIX）

## 版本控制

- **插件版本**: jinkra_mine_shader/__init__.py 中的 l_info["version"]
- **Blender 最低版本**: 4.0.0
- **API 稳定性**: 使用 Blender 官方 stable API

---

**最后更新**: 2026-06-27

