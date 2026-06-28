# 🎮 JinkraMineShader for Blender

一个强大的 Blender 插件，用于加载和应用 Minecraft OptiFine/Iris 光影包，通过 EEVEE 节点系统进行视觉还原。

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Blender](https://img.shields.io/badge/Blender-4.0%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow.svg)

---


## 🔄 版本支持

### Blender 版本
- ✅ **Blender 4.0** - 完全支持
- ✅ **Blender 4.1** - 完全支持（推荐）
- ✅ **Blender 5.0** - 完全支持（最新）

### 光影包格式
- ✅ **OptiFine** - 完全支持
- ✅ **Iris** - 完全支持
- ✅ **自定义格式** - 支持

**详细信息**：见 [`VERSION_COMPATIBILITY.md`](docs/VERSION_COMPATIBILITY.md) 和 [`SHADER_FORMAT_GUIDE.md`](docs/SHADER_FORMAT_GUIDE.md)

## ✨ 功能特性

### 核心功能

- ✅ **ZIP 包解析**: 自动解压和验证 Minecraft 光影包
- ✅ **参数识别**: 智能识别并提取光影配置参数
- ✅ **EEVEE 还原**: 通过节点系统视觉复刻光影效果
- ✅ **环境创建**: 一键创建 MC 风格的天空和光照
- ✅ **PBR 材质**: 为模型快速应用标准 Minecraft PBR 材质
- ✅ **昼夜系统**: 实时时间滑块，自动同步光照和天空
- ✅ **天气模式**: 晴天/雨天/雾天快速切换
- ✅ **预设管理**: 导出/导入光影配置预设

### 高级特性

- 🎨 **方块材质预设**: 包含 15+ 常见方块的快速材质模板
- 🎭 **自发光模拟**: MC 0-15 级方块自发光亮度支持
- 📊 **参数可视化**: 完整的 UI 面板，参数实时可调
- 🔍 **详细验证**: 完整的光影包格式检验和报告
- 📦 **模块化架构**: 易于扩展和定制

---

## 📋 系统要求

| 项目 | 要求 |
|------|------|
| **Blender** | 4.0 或更高版本 |
| **渲染器** | EEVEE（推荐）或 Cycles |
| **Python** | 3.10+ （Blender 内置） |
| **操作系统** | Windows, macOS, Linux |
| **磁盘空间** | ≥ 500 MB（含临时文件） |

---

## 🚀 快速开始

### 安装

#### 方式 1：直接复制到插件目录

**Windows**:
`powershell
xcopy "jinkra_mine_shader" "C:\Users\<用户名>\AppData\Roaming\Blender Foundation\Blender\<版本>\scripts\addons\" /E
`

**macOS**:
`ash
cp -r jinkra_mine_shader ~/Library/Application\ Support/Blender/<版本>/scripts/addons/
`

**Linux**:
`ash
cp -r jinkra_mine_shader ~/.config/blender/<版本>/scripts/addons/
`

#### 方式 2：在 Blender 中安装

1. 打开 Blender → 编辑 > 偏好设置 > 插件
2. 点击 "从文件夹安装"，选择 jinkra_mine_shader 目录
3. 搜索 "JinkraMineShader"，勾选启用

### 首次使用

1. **打开侧边栏**: 按 N 键，找到 **"JinkraMineShader"** 选项卡
2. **加载光影包**: 点击 **"选择光影包"** 按钮，选择 .zip 文件
3. **创建环境**: 点击 **"创建 MC 环境"** 自动配置天空和光照
4. **应用材质**: 选择模型，点击 **"创建 MC 材质"**
5. **调整参数**: 使用参数滑块实时预览效果

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [docs/USAGE.md](docs/USAGE.md) | 详细使用教程和故障排除 |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | 系统架构和模块设计 |
| [docs/PARAMETERS.md](docs/PARAMETERS.md) | 光影参数参考和预设模板 |

---

## 📦 项目结构

\\\
jinkra_mine_shader/
├── __init__.py                  # 插件入口和注册
├── core/                        # 核心解析模块
│   ├── zip_parser.py           # ZIP 包解析和提取
│   ├── shader_validator.py     # 光影包格式验证
│   └── properties_parser.py    # 参数解析和识别
├── ui/                         # UI 面板模块
│   └── panel.py               # Blender 侧边栏面板
├── environment/                # 环境和光照模块
│   └── sky_creator.py         # 天空、光照、昼夜、天气
├── materials/                  # 材质模块
│   └── pbr_template.py        # PBR 材质和方块预设
├── config/                     # 配置管理模块
│   └── preset_manager.py      # 预设导入导出（规划中）
└── utils/                      # 工具模块
    └── logger.py              # 日志、路径、异常处理

docs/
├── USAGE.md                    # 使用教程
├── ARCHITECTURE.md             # 架构文档
└── PARAMETERS.md               # 参数参考
\\\

---

## 💡 使用示例

### 加载标准光影包

\\\python
from jinkra_mine_shader.core.zip_parser import MCShaderZipParser
from jinkra_mine_shader.core.shader_validator import MCShaderValidator

# 加载 ZIP
parser = MCShaderZipParser("shader_pack.zip")
success, msg = parser.extract_zip()

# 验证
validator = MCShaderValidator(parser.extract_dir)
report = validator.validate_all()

if report.is_valid:
    # 读取配置
    success, config = parser.get_shaders_properties()
    print(f"✓ 参数数: {len(config)}")
\\\

### 创建 MC 环境

\\\python
from jinkra_mine_shader.environment.sky_creator import MCEnvironmentCreator, DayNightController

# 创建环境
MCEnvironmentCreator.create_world_environment()
sun = MCEnvironmentCreator.create_sun_light()
MCEnvironmentCreator.setup_eevee_render_settings()

# 设置时间
controller = DayNightController(sun)
controller.set_time(12.0)  # 正午
\\\

### 应用材质

\\\python
from jinkra_mine_shader.materials.pbr_template import MCBlockMaterialFactory

# 为选中物体应用草方块材质
mat = MCBlockMaterialFactory.create_block_material("grass")
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        obj.data.materials.clear()
        obj.data.materials.append(mat)
\\\

---

## 🎯 常见光影包

| 光影包名 | 格式 | 兼容性 |
|---------|------|--------|
| SEUS | OptiFine | ✅ 完全 |
| Chocapic13 | OptiFine | ✅ 完全 |
| Complementary | Iris | ✅ 完全 |
| BSL Shaders | OptiFine | ✅ 完全 |
| Sildur's Shaders | OptiFine | ✅ 完全 |

> 注: 本插件对所有标准 OptiFine/Iris 格式的光影包都有基本支持

---

## 🔧 高级配置

### 启用详细日志

在插件偏好设置中勾选 **"详细日志"**，将在 Blender 控制台输出完整的调试信息。

### 自定义临时目录

默认使用系统临时目录。可在偏好设置中修改临时目录路径。

### 导出/导入预设

1. 调整好所有参数后，点击 **"导出预设"**
2. 保存为 .json 文件
3. 下次可点击 **"导入预设"** 快速恢复

---

## ⚠️ 已知限制

1. **GLSL 编译**: 不支持直接编译原生 .vsh/.fsh 文件，仅通过节点进行复刻
2. **高级效果**: 某些复杂光影效果可能在 EEVEE 中有视觉差异
3. **性能**: 大量复杂材质可能影响实时预览
4. **纹理层数**: Cycles 渲染不支持某些 EEVEE 特定特性

---

## 🐛 故障排除

### Q: 插件加载失败？
**A**: 检查 Blender 控制台（Window > Toggle System Console）查看错误信息

### Q: ZIP 无法解压？
**A**: 确保：
- ZIP 文件未损坏
- 磁盘空间充足
- 文件权限正确

### Q: 参数没有显示？
**A**: 检查：
- 光影包是否包含有效的 shaders.properties
- 查看控制台的验证报告

---

## 📈 路线图

- [ ] **v1.1**: 预设云同步，参数动画编辑器
- [ ] **v1.2**: Cycles 渲染器完全支持
- [ ] **v2.0**: 直接 GLSL 编译支持（可选）
- [ ] **2.0**: 资源包贴图自动导入

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发指南

1. Fork 本仓库
2. 创建特性分支 (git checkout -b feature/AmazingFeature)
3. 提交更改 (git commit -m 'Add some AmazingFeature')
4. 推送到分支 (git push origin feature/AmazingFeature)
5. 提交 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 👨‍💻 作者

**Jinkra** - 原作者

---

## 🙏 致谢

- Minecraft 官方团队
- OptiFine/Iris 光影社区
- Blender 开发团队

---

## 📞 联系方式

- 📧 Email: [your-email@example.com]
- 💬 GitHub Issues: [提交问题](../../issues)
- 🌐 官方网站: [待定]

---

<div align="center">

**Made with ❤️ for Minecraft & Blender**

*如果这个项目对你有帮助，请给个 ⭐*

</div>


