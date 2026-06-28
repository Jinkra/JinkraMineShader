# JinkraMineShader for Blender - 使用教程

## 概述

JinkraMineShader 是一个 Blender 插件，用于加载 Minecraft OptiFine/Iris 光影包，并通过 EEVEE 节点系统进行视觉还原。

**注意**: 本插件不直接编译原生 GLSL 代码，而是通过 Blender EEVEE 的合成节点系统复刻光影效果。

## 系统要求

- **Blender**: 4.0 或更高版本
- **渲染器**: EEVEE（推荐）
- **操作系统**: Windows, macOS, Linux
- **Python**: 3.10+ (Blender 内置)

## 安装

### 方式 1：从文件夹安装

1. 下载或克隆此项目
2. 打开 Blender，进入 编辑 > 偏好设置 > 插件
3. 点击 "从文件夹安装" 或手动复制 jinkra_mine_shader 文件夹到 Blender 的插件目录

### 方式 2：直接复制到插件目录

**Windows**:
`
C:\Users\<用户名>\AppData\Roaming\Blender Foundation\Blender\<版本>\scripts\addons\
`

**macOS**:
`
/Users/<用户名>/Library/Application Support/Blender/<版本>/scripts/addons/
`

**Linux**:
`
~/.config/blender/<版本>/scripts/addons/
`

## 快速开始

### 1. 启用插件

1. 打开 Blender 偏好设置 > 插件
2. 搜索 "JinkraMineShader"
3. 勾选启用

### 2. 打开面板

1. 在 3D 视图侧边栏找到 **"JinkraMineShader"** 选项卡
2. 如果看不到，按 N 打开侧边栏

### 3. 加载光影包

1. 点击 **"选择光影包"** 按钮
2. 选择一个 .zip 光影包文件（OptiFine 或 Iris 格式）
3. 等待加载完成

### 4. 创建环境

1. 点击 **"创建 MC 环境"** 按钮
2. 插件会自动创建：
   - MC 天空背景
   - 太阳光源
   - 环保光

### 5. 应用材质

1. 在 3D 视图中选中一个或多个模型
2. 点击 **"创建 MC 材质"** 按钮
3. 模型会应用标准的 MC PBR 材质

## 参数说明

### 核心参数

| 参数名 | 类型 | 默认值 | 范围 | 说明 |
|--------|------|--------|------|------|
| exposure | Float | 1.0 | 0.1 - 3.0 | 曝光度（影响整体亮度） |
| rightness | Float | 1.0 | 0.0 - 2.0 | 亮度调整 |
| contrast | Float | 1.0 | 0.0 - 2.0 | 对比度 |
| saturation | Float | 1.0 | 0.0 - 2.0 | 饱和度 |
| ogDensity | Float | 0.5 | 0.0 - 1.0 | 雾浓度 |
| loomStrength | Float | 0.8 | 0.0 - 1.0 | 泛光强度 |
| 
ainStrength | Float | 0.0 | 0.0 - 1.0 | 降雨强度 |
| daylightCycleMix | Float | 0.0 | 0.0 - 1.0 | 昼夜循环混合 |

### 昼夜系统

使用时间滑块（0-24小时）自动调整：
- 太阳角度和强度
- 天空颜色
- 环保光参数
- 整体曝光

### 天气模式

三种预设模式可快速切换：

- **晴天 (Clear)**: 清晰天空，低雾浓度
- **雨天 (Rain)**: 增加雾，降低曝光，启用降雨效果
- **雾天 (Fog)**: 高雾浓度，柔和光照

## 高级功能

### 导出/导入预设

1. 调整好所有参数后，点击 **"导出预设"**
2. 选择保存位置，生成 .json 配置文件
3. 下次可点击 **"导入预设"** 快速恢复设置

### 批量材质应用

选中多个物体后，点击 **"创建 MC 材质"** 可以一次性为所有物体应用材质。

### 参数重置

点击 **"重置参数"** 恢复到光影包的默认值。

## 已知限制

1. **GLSL 编译**: 本插件不支持直接编译原生光影 .vsh/.fsh 文件，仅通过节点进行视觉复刻
2. **高级效果**: 某些高级 Minecraft 光影效果（如水体折射、体积光等）在 EEVEE 中效果可能有差异
3. **性能**: 大量复杂材质可能会影响实时预览性能
4. **纹理上限**: Cycles 渲染器不支持某些 EEVEE 特定效果

## 故障排除

### 问题：插件加载失败

**解决**: 检查 Blender 控制台（Window > Toggle System Console）查看错误信息

### 问题：ZIP 解压错误

**解决**: 确保：
1. ZIP 文件没有损坏
2. 有足够的磁盘空间
3. 文件权限正确

### 问题：参数没有显示

**解决**: 
1. 确保光影包包含有效的 shaders.properties 文件
2. 检查控制台的验证报告

### 问题：材质看起来不对

**解决**:
1. 确保切换到 EEVEE 渲染器
2. 调整参数以获得理想效果
3. 检查模型法线方向

## 开发者信息

### 项目结构

\\\
jinkra_mine_shader/
├── __init__.py              # 插件入口
├── core/                    # 核心解析模块
│   ├── zip_parser.py       # ZIP 包解析
│   ├── shader_validator.py # 光影验证
│   └── properties_parser.py # 参数解析
├── ui/                      # UI 面板
│   └── panel.py            # 侧边栏面板
├── environment/             # 环境和光照
│   └── sky_creator.py      # 天空和时间系统
├── materials/               # 材质模块
│   └── pbr_template.py     # PBR 材质模板
├── config/                  # 配置管理
│   └── preset_manager.py   # 预设管理
└── utils/                   # 工具函数
    └── logger.py           # 日志系统
\\\

### 扩展插件

参考 参数说明 部分，可以修改相应模块来添加新功能。

## 许可证

MIT License

## 反馈与支持

如有问题，请提交 zdbkp@foxmail.com

---

**版本**: 1.0.0  
**最后更新**: 2026-06-27

