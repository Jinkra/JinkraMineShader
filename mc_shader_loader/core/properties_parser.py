"""
.properties 配置文件解析和参数提取模块

功能:
  1. 解析 shaders.properties 配置文件
  2. 提取可调整的参数（滑块、下拉框等）
  3. 生成 Blender 属性定义
  4. 支持参数预设和默认值
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Any, Union


class ShaderProperty:
    """单个着色器参数的定义"""
    
    def __init__(self, key: str, value: str):
        """
        初始化参数
        
        Args:
            key: 参数键名
            value: 参数值（字符串）
        """
        self.key = key
        self.raw_value = value
        
        # 参数的元信息
        self.display_name = self._make_display_name(key)
        self.param_type = "unknown"  # float, int, bool, enum, string
        self.default_value = None
        self.min_value = 0.0
        self.max_value = 1.0
        self.step = 0.01
        self.options = []  # 用于 enum 类型
        self.description = ""
    
    @staticmethod
    def _make_display_name(key: str) -> str:
        """
        将驼峰命名转换为可读的显示名称
        
        例: "fogDensity" -> "Fog Density"
        """
        # 在大写字母前插入空格
        result = re.sub(r'([a-z])([A-Z])', r'\1 \2', key)
        # 首字母大写
        return result[0].upper() + result[1:] if result else key
    
    def parse_value(self):
        """解析原始值并确定参数类型"""
        value = self.raw_value.strip()
        
        # 尝试解析为数字
        try:
            if '.' in value:
                self.default_value = float(value)
                self.param_type = "float"
            else:
                self.default_value = int(value)
                self.param_type = "int"
            return
        except ValueError:
            pass
        
        # 检查布尔值
        if value.lower() in ['true', 'false', 'yes', 'no', 'on', 'off']:
            self.default_value = value.lower() in ['true', 'yes', 'on']
            self.param_type = "bool"
            return
        
        # 字符串
        self.default_value = value
        self.param_type = "string"
    
    def guess_ranges(self):
        """根据参数值推断范围和类型"""
        # 1. 尝试转换为浮点数
        try:
            val = float(self.raw_value)
            self.param_type = "float"
            if val < 0:
                self.min_val = val * 2
                self.max_val = abs(val) * 0.1
            elif val == 0:
                self.min_val = 0.0
                self.max_val = 1.0
            elif val <= 1:
                self.min_val = 0.0
                self.max_val = 2.0
            elif val <= 10:
                self.min_val = 0.0
                self.max_val = val * 2
            else:
                self.min_val = 0.0
                self.max_val = val * 1.5
            return
        except (ValueError, TypeError):
            pass
        
        # 2. 检查布尔值
        if self.raw_value.lower() in ("true", "false", "yes", "no", "0", "1", "-1"):
            self.param_type = "bool"
            return
        
        # 3. 检查列表/枚举
        values = self.raw_value.split()
        if len(values) > 1:
            self.param_type = "enum"
            return
        
        self.param_type = "string"
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于序列化）"""
        return {
            "key": self.key,
            "display_name": self.display_name,
            "type": self.param_type,
            "default": self.default_value,
            "min": self.min_value,
            "max": self.max_value,
            "step": self.step,
            "options": self.options,
            "description": self.description,
        }


class PropertiesParser:
    """光影包 properties 文件解析器"""
    
    # 优先级高的参数（应该在 UI 中优先显示）
    PRIORITY_PARAMS = {
        "exposure": 100,
        "brightness": 100,
        "contrast": 90,
        "saturation": 90,
        "fogDensity": 80,
        "bloomStrength": 80,
        "rainStrength": 70,
        "daylightCycleMix": 70,
    }
    
    def __init__(self, properties_dict: Dict[str, str]):
        """
        初始化解析器
        
        Args:
            properties_dict: 从 .properties 文件解析出的字典
        """
        self.raw_properties = properties_dict
        self.properties: Dict[str, ShaderProperty] = {}
        self.parse()
    
    def parse(self):
        """解析所有属性"""
        for key, value in self.raw_properties.items():
            # 过滤掉过长的键或明显不是参数的项
            if len(key) > 100 or key.startswith('_'):
                continue
            
            prop = ShaderProperty(key, value)
            prop.parse_value()
            prop.guess_ranges()
            
            self.properties[key] = prop
    
    def get_sorted_properties(self, filter_type: Optional[str] = None) -> List[ShaderProperty]:
        """
        获取排序后的属性列表
        
        Args:
            filter_type: 只返回指定类型的属性（'float', 'int', 'bool', 'enum', 'string'）
        
        Returns:
            排序后的属性列表（按优先级和字母序）
        """
        props = list(self.properties.values())
        
        # 筛选类型
        if filter_type:
            props = [p for p in props if p.param_type == filter_type]
        
        # 排序：优先级高的在前，同优先级按名称
        def sort_key(prop):
            priority = self.PRIORITY_PARAMS.get(prop.key, 0)
            return (-priority, prop.display_name)
        
        props.sort(key=sort_key)
        return props
    
    def get_float_params(self) -> List[ShaderProperty]:
        """获取所有浮点参数"""
        return self.get_sorted_properties(filter_type='float')
    
    def get_int_params(self) -> List[ShaderProperty]:
        """获取所有整数参数"""
        return self.get_sorted_properties(filter_type='int')
    
    def get_bool_params(self) -> List[ShaderProperty]:
        """获取所有布尔参数"""
        return self.get_sorted_properties(filter_type='bool')
    
    def get_all_params(self) -> List[ShaderProperty]:
        """获取所有参数"""
        return self.get_sorted_properties()
    
    def get_param_by_key(self, key: str) -> Optional[ShaderProperty]:
        """根据键获取参数"""
        return self.properties.get(key)
    
    def export_to_json(self) -> str:
        """将参数导出为 JSON 格式"""
        data = {
            "version": "1.0",
            "param_count": len(self.properties),
            "parameters": [p.to_dict() for p in self.get_all_params()]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def export_to_dict(self) -> Dict[str, Any]:
        """将参数导出为字典"""
        return {
            "version": "1.0",
            "param_count": len(self.properties),
            "parameters": {k: p.to_dict() for k, p in self.properties.items()}
        }
    
    def get_summary(self) -> str:
        """获取解析摘要"""
        all_props = self.get_all_params()
        
        type_counts = {}
        for prop in all_props:
            type_counts[prop.param_type] = type_counts.get(prop.param_type, 0) + 1
        
        summary = f"参数解析摘要\n"
        summary += f"  总参数数: {len(all_props)}\n"
        for ptype, count in sorted(type_counts.items()):
            summary += f"  {ptype}: {count}\n"
        
        # 列出优先级最高的参数
        priority_props = self.get_sorted_properties()[:5]
        if priority_props:
            summary += f"\n 优先显示参数:\n"
            for prop in priority_props:
                summary += f"  • {prop.display_name} ({prop.param_type})\n"
        
        return summary


def demo_parsing():
    """解析演示"""
    # 模拟 properties 文件内容
    props_dict = {
        "exposure": "1.0",
        "brightness": "1.0",
        "contrast": "1.0",
        "saturation": "1.0",
        "fogDensity": "0.5",
        "bloomStrength": "0.8",
        "rainStrength": "0.0",
        "daylightCycleMix": "0.0",
    }
    
    parser = PropertiesParser(props_dict)
    
    print(parser.get_summary())
    
    print("\n浮点参数:")
    for prop in parser.get_float_params():
        print(f"  {prop.display_name}: {prop.default_value} [{prop.min_value}, {prop.max_value}]")
    
    print("\n所有参数 JSON:")
    print(parser.export_to_json()[:200] + "...")


if __name__ == "__main__":
    demo_parsing()

