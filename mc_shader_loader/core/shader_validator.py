"""
光影包格式校验和属性验证模块

功能:
  1. 验证 ZIP 包的完整性
  2. 检查必需的配置文件和目录
  3. 验证 shaders.properties 参数格式
  4. 生成详细的验证报告
"""

import os
import re
import json
from typing import Tuple, List, Dict, Optional, Any


class ShaderValidationReport:
    """光影包验证报告"""
    
    def __init__(self):
        """初始化报告"""
        self.is_valid = True
        self.pack_name = ""
        self.pack_version = ""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        
        # 统计信息
        self.shader_count = 0
        self.texture_count = 0
        self.config_params = 0
    
    def add_error(self, msg: str):
        """添加错误"""
        self.errors.append(msg)
        self.is_valid = False
    
    def add_warning(self, msg: str):
        """添加警告"""
        self.warnings.append(msg)
    
    def add_info(self, msg: str):
        """添加信息"""
        self.info.append(msg)
    
    def get_summary(self) -> str:
        """获取总结字符串"""
        status = "✓ 有效" if self.is_valid else "✗ 无效"
        summary = f"\n=== 光影包验证报告 ===\n"
        summary += f"状态: {status}\n"
        
        if self.pack_name:
            summary += f"包名: {self.pack_name}\n"
        
        if self.pack_version:
            summary += f"版本: {self.pack_version}\n"
        
        if self.errors:
            summary += f"\n【错误】({len(self.errors)})\n"
            for i, err in enumerate(self.errors, 1):
                summary += f"  {i}. {err}\n"
        
        if self.warnings:
            summary += f"\n【警告】({len(self.warnings)})\n"
            for i, warn in enumerate(self.warnings, 1):
                summary += f"  {i}. {warn}\n"
        
        if self.info:
            summary += f"\n【信息】\n"
            for info in self.info:
                summary += f"  • {info}\n"
        
        return summary


class MCShaderValidator:
    """Minecraft 光影包格式校验器"""
    
    # OptiFine 已知的配置参数模式
    KNOWN_PARAMS = {
        # 曝光和色调
        "exposure": float,
        "contrast": float,
        "saturation": float,
        "brightness": float,
        
        # 雾和大气
        "fogDensity": float,
        "fogEnd": float,
        "fogStart": float,
        "atmosphericDensity": float,
        
        # 昼夜
        "daylightCycleMix": float,
        "daylight": float,
        "twilight": float,
        "moonlight": float,
        
        # 天空
        "skyColorR": float,
        "skyColorG": float,
        "skyColorB": float,
        
        # 水
        "waterWave": float,
        "waterFrequency": float,
        "waterNormalMapScale": float,
        
        # 泛光
        "bloomStrength": float,
        "bloomRadius": float,
        "bloomThreshold": float,
        
        # 下雨
        "rainStrength": float,
        "rainDropsSize": float,
    }
    
    def __init__(self, extract_dir: str):
        """
        初始化验证器
        
        Args:
            extract_dir: 已解压光影包的目录
        """
        self.extract_dir = extract_dir
        self.report = ShaderValidationReport()
    
    def validate_all(self) -> ShaderValidationReport:
        """
        执行完整的验证流程
        
        Returns:
            验证报告
        """
        self.report = ShaderValidationReport()
        
        # 1. 检查目录存在性
        if not os.path.isdir(self.extract_dir):
            self.report.add_error(f"提取目录不存在或不是文件夹: {self.extract_dir}")
            return self.report
        
        self.report.add_info(f"检查目录: {self.extract_dir}")
        
        # 2. 验证必需的文件和目录
        self._validate_structure()
        
        if self.report.errors:
            # 如果有严重错误，提前退出
            return self.report
        
        # 3. 验证配置文件
        self._validate_properties_file()
        
        # 4. 验证着色器文件
        self._validate_shaders()
        
        # 5. 验证纹理资源
        self._validate_textures()
        
        # 6. 检查特殊文件
        self._check_optional_files()
        
        return self.report
    
    def _validate_structure(self):
        """验证基础目录结构"""
        # 检查 shaders/ 目录（必需）
        shaders_dir = os.path.join(self.extract_dir, "shaders")
        if not os.path.isdir(shaders_dir):
            self.report.add_error("缺少必需目录: shaders/")
            return
        
        self.report.add_info("✓ 找到 shaders/ 目录")
        
        # 检查是否有着色器文件（递归搜索）
        shader_files = []
        for root, dirs, files in os.walk(shaders_dir):
            for f in files:
                if f.endswith(('.fsh', '.vsh')):
                    shader_files.append(f)
        
        if not shader_files:
            self.report.add_error("shaders/ 目录中没有 .fsh 或 .vsh 文件")
            return
        
        self.report.add_info(f"✓ 找到 {len(shader_files)} 个着色器文件")
        
        # shaders.properties 现在是可选的
        props_path = os.path.join(self.extract_dir, "shaders.properties")
        if os.path.exists(props_path):
            self.report.add_info("✓ 找到 shaders.properties")
        else:
            self.report.add_warning("未找到 shaders.properties - 某些 Iris 光影不需要此文件")
    
    def _validate_properties_file(self):
        """验证配置文件（支持多种格式）"""
        # 尝试多个位置查找配置文件
        candidates = [
            os.path.join(self.extract_dir, "shaders.properties"),  # OptiFine 根级
            os.path.join(self.extract_dir, "shaders", "shaders.properties"),  # Iris 标准
            os.path.join(self.extract_dir, "shaders", "block.properties"),  # 备选
        ]
        
        props_path = None
        for candidate in candidates:
            if os.path.exists(candidate):
                props_path = candidate
                break
        
        # 如果没找到任何配置文件，这不是错误（某些光影可能不需要）
        if not props_path:
            self.report.add_warning("未找到配置文件 - 某些光影包不需要此文件")
            return
        
        try:
            with open(props_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            valid_lines = 0
            invalid_lines = []
            
            param_count = 0
            
            for line_num, line in enumerate(lines, 1):
                # 跳过注释和空行
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    continue
                
                valid_lines += 1
                
                # 检查是否是有效的键值对
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key and value:
                        param_count += 1
                        
                        # 尝试识别参数类型
                        self._validate_param(key, value)
                else:
                    invalid_lines.append(f"第 {line_num} 行: 无效的格式 '{line[:50]}'")
            
            self.report.add_info(f"✓ 有效的参数行: {param_count}")
            self.report.config_params = param_count
            
            if invalid_lines and len(invalid_lines) < 10:
                for inv in invalid_lines:
                    self.report.add_warning(inv)
            elif invalid_lines:
                self.report.add_warning(f"检测到 {len(invalid_lines)} 行无效的参数格式")
        
        except Exception as e:
            self.report.add_warning(f"读取 shaders.properties 失败: {str(e)}")
    
    def _validate_param(self, key: str, value: str):
        """验证单个参数"""
        # 检查参数名格式（驼峰命名）
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
            self.report.add_warning(f"参数名格式可疑: '{key}'")
        
        # 尝试类型转换
        try:
            float(value)  # 尝试转为浮点数
        except ValueError:
            # 可能是其他类型（字符串、布尔值等）
            if value.lower() not in ['true', 'false', 'yes', 'no']:
                # 可能是字符串，不报错
                pass
    
    def _validate_shaders(self):
        """验证着色器文件"""
        shaders_dir = os.path.join(self.extract_dir, "shaders")
        
        vsh_files = []
        fsh_files = []
        glsl_files = []
        
        for root, dirs, files in os.walk(shaders_dir):
            for f in files:
                if f.endswith('.vsh'):
                    vsh_files.append(os.path.join(root, f))
                elif f.endswith('.fsh'):
                    fsh_files.append(os.path.join(root, f))
                elif f.endswith('.glsl'):
                    glsl_files.append(os.path.join(root, f))
        
        self.report.shader_count = len(vsh_files) + len(fsh_files)
        
        if not vsh_files and not fsh_files:
            self.report.add_error("未找到任何着色器文件（需要 .vsh 或 .fsh）")
        else:
            info_str = "✓ 着色器文件:"
            if vsh_files:
                info_str += f" {len(vsh_files)}× .vsh"
            if fsh_files:
                info_str += f" {len(fsh_files)}× .fsh"
            if glsl_files:
                info_str += f" {len(glsl_files)}× .glsl"
            
            self.report.add_info(info_str)
    
    def _validate_textures(self):
        """验证纹理资源"""
        texture_extensions = {'.png', '.jpg', '.jpeg', '.tga', '.bmp'}
        
        texture_count = 0
        lut_count = 0
        noise_count = 0
        sky_count = 0
        
        for root, dirs, files in os.walk(self.extract_dir):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in texture_extensions:
                    texture_count += 1
                    
                    rel_path = os.path.relpath(os.path.join(root, f), self.extract_dir).lower()
                    if 'lut' in rel_path or 'colortex' in rel_path:
                        lut_count += 1
                    elif 'noise' in rel_path:
                        noise_count += 1
                    elif 'sky' in rel_path:
                        sky_count += 1
        
        self.report.texture_count = texture_count
        
        if texture_count == 0:
            self.report.add_warning("未找到任何纹理资源")
        else:
            self.report.add_info(f"✓ 纹理资源: {texture_count} 个（LUT: {lut_count}, 噪声: {noise_count}, 天空: {sky_count}）")
    
    def _check_optional_files(self):
        """检查可选文件"""
        optional_dirs = ["shaders/lang", "assets", "optifine"]
        optional_files = ["pack.mcmeta", "pack.png"]
        
        for dir_name in optional_dirs:
            dir_path = os.path.join(self.extract_dir, dir_name)
            if os.path.isdir(dir_path):
                self.report.add_info(f"✓ 找到可选目录: {dir_name}")
        
        for file_name in optional_files:
            file_path = os.path.join(self.extract_dir, file_name)
            if os.path.exists(file_path):
                self.report.add_info(f"✓ 找到可选文件: {file_name}")


def demo_validation():
    """验证演示"""
    # 假设解压后的目录路径
    extract_dir = "path/to/extracted/shader_pack"
    
    validator = MCShaderValidator(extract_dir)
    report = validator.validate_all()
    
    print(report.get_summary())
    
    return report


if __name__ == "__main__":
    demo_validation()


