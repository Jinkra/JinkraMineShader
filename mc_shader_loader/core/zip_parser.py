"""
Minecraft 光影包 ZIP 文件解析模块

功能：
- ZIP 文件解压和验证
- 光影包结构检查
- 配置文件读取
- 纹理资源收集
"""

import os
import sys
import shutil
import zipfile
import tempfile
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


class MCShaderZipParser:
    """Minecraft 光影包 ZIP 解析器"""
    
    def __init__(self, zip_path: str, temp_base_dir: Optional[str] = None):
        """
        初始化 ZIP 解析器
        
        Args:
            zip_path: 光影 ZIP 文件完整路径
            temp_base_dir: 临时目录基础路径，若不指定则使用系统临时目录
        """
        self.zip_path = zip_path
        self.temp_base_dir = temp_base_dir or tempfile.gettempdir()
        self.extract_dir = None
        self.zip_name = Path(zip_path).stem  # 不含扩展名的文件名
        
        # 预期的光影包目录结构
        self.required_structure = {
            "shaders.properties": "全局光影配置文件（必需）",
        }
    
    def extract_zip(self) -> Tuple[bool, str]:
        """
        解压 ZIP 文件到临时目录
        
        Returns:
            (成功标记, 提取目录路径或错误信息)
        """
        try:
            # 验证 ZIP 文件存在且有效
            if not os.path.exists(self.zip_path):
                return False, f"ZIP 文件不存在: {self.zip_path}"
            
            if not zipfile.is_zipfile(self.zip_path):
                return False, f"不是有效的 ZIP 文件: {self.zip_path}"
            
            # 确保临时基础目录存在
            if not os.path.exists(self.temp_base_dir):
                try:
                    os.makedirs(self.temp_base_dir, exist_ok=True)
                except Exception as e:
                    return False, f"无法创建临时目录 {self.temp_base_dir}: {str(e)}"
            
            # 创建唯一的解压目录
            self.extract_dir = os.path.join(
                self.temp_base_dir,
                f"jinkra_mine_shader_{self.zip_name}_{id(self)}"
            )
            
            print(f"[MCShaderZipParser] 创建提取目录: {self.extract_dir}")
            
            # 清理旧的提取目录（如果存在）
            if os.path.exists(self.extract_dir):
                try:
                    shutil.rmtree(self.extract_dir, ignore_errors=True)
                    print(f"[MCShaderZipParser] 已清理旧的提取目录")
                except Exception as e:
                    print(f"[MCShaderZipParser] 警告：无法清理旧目录: {e}")
            
            # 创建新的解压目录
            try:
                os.makedirs(self.extract_dir, exist_ok=True)
                print(f"[MCShaderZipParser] 解压目录创建成功")
            except Exception as e:
                return False, f"无法创建解压目录 {self.extract_dir}: {str(e)}"
            
            # 解压 ZIP
            try:
                print(f"[MCShaderZipParser] 开始解压: {self.zip_path}")
                with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.extract_dir)
                print(f"[MCShaderZipParser] 解压完成")
            except Exception as e:
                return False, f"ZIP 解压失败: {str(e)}"
            
            # 验证解压是否成功
            if not os.path.exists(self.extract_dir):
                return False, f"解压目录验证失败: {self.extract_dir} 不存在"
            
            if os.listdir(self.extract_dir) == []:
                return False, f"解压目录为空"
            
            return True, self.extract_dir
            
        except Exception as e:
            return False, f"解压 ZIP 失败: {str(e)}"
    
    def validate_structure(self) -> Tuple[bool, str]:
        """
        验证光影包结构
        
        Returns:
            (是否有效, 验证信息)
        """
        try:
            if not self.extract_dir or not os.path.exists(self.extract_dir):
                return False, "提取目录不存在，请先调用 extract_zip()"
            
            # 检查必需的配置文件
            shaders_props_path = os.path.join(self.extract_dir, "shaders.properties")
            if not os.path.exists(shaders_props_path):
                return False, "缺少 shaders.properties 配置文件（必需）"
            
            # 检查 shaders 目录
            shaders_dir = os.path.join(self.extract_dir, "shaders")
            if not os.path.isdir(shaders_dir):
                return False, "缺少 shaders/ 目录（必需）"
            
            return True, "光影包结构验证通过"
        
        except Exception as e:
            return False, f"结构验证失败: {str(e)}"
    
    def get_shaders_properties(self) -> Tuple[bool, Dict[str, Any] | str]:
        """
        读取光影配置文件（支持多种格式）
        
        尝试顺序：
        1. shaders.properties (OptiFine 标准)
        2. shaders/block.properties (Iris 格式)
        3. shaders/*.properties 中的其他文件
        
        Returns:
            (成功标记, 配置字典或错误信息)
        """
        try:
            if not self.extract_dir:
                return False, "提取目录不存在"
            
            config = {}
            found_file = None
            
            # 1. 尝试读取根级 shaders.properties
            root_props = os.path.join(self.extract_dir, "shaders.properties")
            if os.path.exists(root_props):
                found_file = root_props
                print(f'[MCShaderZipParser] 找到根级 shaders.properties')
            else:
                # 2. 尝试读取 shaders/shaders.properties (Iris 标准格式)
                iris_props = os.path.join(self.extract_dir, "shaders", "shaders.properties")
                if os.path.exists(iris_props):
                    found_file = iris_props
                    print(f'[MCShaderZipParser] 找到 shaders/shaders.properties，参数数量：')
                else:
                    # 3. 尝试读取 shaders/block.properties
                    block_props = os.path.join(self.extract_dir, "shaders", "block.properties")
                    if os.path.exists(block_props):
                        found_file = block_props
                    else:
                        # 4. 尝试读取 shaders/ 目录中的任何 .properties 文件
                        shaders_dir = os.path.join(self.extract_dir, "shaders")
                        if os.path.isdir(shaders_dir):
                            for file in os.listdir(shaders_dir):
                                if file.endswith('.properties') and file != 'block.properties':
                                    found_file = os.path.join(shaders_dir, file)
                                    break
            
            # 如果找到配置文件，读取它
            if found_file and os.path.exists(found_file):
                try:
                    with open(found_file, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            line = line.strip()
                            if not line or line.startswith('#'):
                                continue
                            
                            if '=' in line:
                                key, value = line.split('=', 1)
                                config[key.strip()] = value.strip()
                except Exception as e:
                    return False, f"读取配置文件失败: {str(e)}"
            
            # 返回找到的配置（即使为空也不是错误）
            return True, config
        
        except Exception as e:
            return False, f"获取配置失败: {str(e)}"
    
    def get_preset_files(self) -> List[str]:
        """
        获取所有预设 JSON 文件列表
        
        Returns:
            相对路径列表
        """
        preset_files = []
        
        if not self.extract_dir:
            return preset_files
        
        try:
            for root, dirs, files in os.walk(self.extract_dir):
                for f in files:
                    if f.endswith('.json'):
                        full_path = os.path.join(root, f)
                        # 相对于提取目录的相对路径
                        rel_path = os.path.relpath(full_path, self.extract_dir)
                        preset_files.append(rel_path)
        except Exception as e:
            print(f"[MCShaderZipParser] 获取预设文件失败: {e}")
        
        return preset_files
    
    def get_texture_files(self) -> Dict[str, List[str]]:
        """
        获取纹理文件分类列表
        
        Returns:
            分类的纹理文件字典
        """
        texture_files = {
            "noise": [],
            "lut": [],
            "sky": [],
            "other": [],
        }
        
        if not self.extract_dir:
            return texture_files
        
        try:
            texture_extensions = {'.png', '.jpg', '.jpeg', '.tga', '.bmp'}
            
            for root, dirs, files in os.walk(self.extract_dir):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext not in texture_extensions:
                        continue
                    
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, self.extract_dir)
                    
                    # 根据路径和文件名分类
                    path_lower = rel_path.lower()
                    
                    if 'noise' in path_lower:
                        texture_files["noise"].append(rel_path)
                    elif 'lut' in path_lower or 'colormap' in path_lower:
                        texture_files["lut"].append(rel_path)
                    elif 'sky' in path_lower:
                        texture_files["sky"].append(rel_path)
                    else:
                        texture_files["other"].append(rel_path)
        
        except Exception as e:
            print(f"[MCShaderZipParser] 获取纹理文件失败: {e}")
        
        return texture_files
    
    def get_texture_path(self, relative_path: str) -> str:
        """
        获取纹理文件的完整路径
        
        Args:
            relative_path: 相对于提取目录的路径
        
        Returns:
            完整的绝对路径
        """
        if not self.extract_dir:
            return ""
        
        full_path = os.path.join(self.extract_dir, relative_path)
        
        if os.path.exists(full_path):
            return full_path
        
        return ""
    
    def cleanup(self) -> bool:
        """
        清理临时提取的文件
        
        Returns:
            清理是否成功
        """
        if self.extract_dir and os.path.exists(self.extract_dir):
            try:
                shutil.rmtree(self.extract_dir, ignore_errors=True)
                print(f"✓ 已清理临时目录: {self.extract_dir}")
                return True
            except Exception as e:
                print(f"⚠ 清理临时目录失败: {str(e)}")
        
        return False


# 测试代码
if __name__ == "__main__":
    # 示例使用
    zip_path = "example_shader.zip"
    parser = MCShaderZipParser(zip_path)
    
    # 1. 解压
    success, msg = parser.extract_zip()
    print(f"解压结果: {msg}")
    
    if not success:
        sys.exit(1)
    
    # 2. 验证
    success, msg = parser.validate_structure()
    print(f"验证结果: {msg}")
    
    if not success:
        parser.cleanup()
        sys.exit(1)
    
    # 3. 读取配置
    success, config_or_msg = parser.get_shaders_properties()
    if success:
        print(f"✓ 配置读取成功，包含 {len(config_or_msg)} 个参数")
    else:
        print(f"✗ 配置读取失败: {config_or_msg}")
    
    # 4. 获取预设
    presets = parser.get_preset_files()
    print(f"✓ 找到 {len(presets)} 个预设文件")
    
    # 5. 获取纹理
    textures = parser.get_texture_files()
    print(f"✓ 找到纹理: noise={len(textures['noise'])}, lut={len(textures['lut'])}, sky={len(textures['sky'])}")
    
    # 清理
    parser.cleanup()
