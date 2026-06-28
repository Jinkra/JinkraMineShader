"""
MC 标准 PBR 材质模板模块

功能:
  1. 为选中物体创建标准 MC PBR 材质
  2. 支持漫反射、法线、粗糙度、金属度、自发光
  3. 模拟 MC 方块 0-15 级自发光亮度
"""

import bpy
from typing import Optional, List


class MCPBRMaterialTemplate:
    """MC 标准 PBR 材质模板"""
    
    PREFIX = "jinkra_mine_shader_"
    
    @staticmethod
    def create_standard_material(material_name: str = "MC_Standard") -> Optional[bpy.types.Material]:
        """
        创建标准的 MC PBR 材质
        
        Args:
            material_name: 材质名称
        
        Returns:
            创建的材质对象
        """
        # 创建材质
        mat = bpy.data.materials.new(name=f"{MCPBRMaterialTemplate.PREFIX}{material_name}")
        mat.use_nodes = True
        
        # 清空默认节点
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # 创建关键节点
        output_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        output_node.name = "Principled BSDF"
        
        # 输出节点
        out_socket = nodes.new(type='ShaderNodeOutputMaterial')
        links.new(output_node.outputs['BSDF'], out_socket.inputs['Surface'])
        
        # 配置基本属性
        output_node.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)  # 白色
        output_node.inputs['Metallic'].default_value = 0.0  # 非金属
        output_node.inputs['Roughness'].default_value = 0.8  # 较粗糙
        output_node.inputs['Coat Weight'].default_value = 0.0  # 无外层涂层
        
        return mat
    
    @staticmethod
    def add_texture_slots(material: bpy.types.Material) -> bool:
        """
        为材质添加纹理槽
        
        创建以下槽位：
        - Image Texture (BaseColor)
        - Normal Map
        - Roughness
        - Metallic
        - Emission
        
        Args:
            material: 目标材质
        
        Returns:
            是否成功
        """
        if not material.use_nodes:
            return False
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        
        # 获取 Principled BSDF 节点
        bsdf_node = None
        for node in nodes:
            if node.type == 'BSDF_PRINCIPLED':
                bsdf_node = node
                break
        
        if not bsdf_node:
            return False
        
        # 创建纹理节点
        # 1. BaseColor 纹理
        base_tex = nodes.new(type='ShaderNodeTexImage')
        base_tex.label = "BaseColor"
        links.new(base_tex.outputs['Color'], bsdf_node.inputs['Base Color'])
        
        # 2. Normal Map
        normal_tex = nodes.new(type='ShaderNodeTexImage')
        normal_tex.label = "Normal"
        normal_map = nodes.new(type='ShaderNodeNormalMap')
        normal_map.inputs['Strength'].default_value = 1.0
        links.new(normal_tex.outputs['Color'], normal_map.inputs['Color'])
        links.new(normal_map.outputs['Normal'], bsdf_node.inputs['Normal'])
        
        # 3. Roughness
        rough_tex = nodes.new(type='ShaderNodeTexImage')
        rough_tex.label = "Roughness"
        links.new(rough_tex.outputs['Color'], bsdf_node.inputs['Roughness'])
        
        # 4. Metallic
        metal_tex = nodes.new(type='ShaderNodeTexImage')
        metal_tex.label = "Metallic"
        links.new(metal_tex.outputs['Color'], bsdf_node.inputs['Metallic'])
        
        # 5. Emission
        emit_tex = nodes.new(type='ShaderNodeTexImage')
        emit_tex.label = "Emission"
        links.new(emit_tex.outputs['Color'], bsdf_node.inputs['Emission Color'])
        
        return True
    
    @staticmethod
    def set_emission_level(material: bpy.types.Material, level: int = 0):
        """
        设置材质的自发光亮度等级（MC 0-15）
        
        Args:
            material: 目标材质
            level: 亮度等级 0-15（0=无发光，15=最亮）
        """
        if not material.use_nodes:
            return
        
        nodes = material.node_tree.nodes
        
        # 获取 Principled BSDF 节点
        bsdf_node = None
        for node in nodes:
            if node.type == 'BSDF_PRINCIPLED':
                bsdf_node = node
                break
        
        if not bsdf_node:
            return
        
        # 转换 MC 等级 (0-15) 到 Blender 发光强度
        # MC 的 15 级对应完全白色发光
        # 转换公式: strength = level / 15 * max_strength
        max_strength = 2.0  # Blender 中的最大发光强度
        strength = (level / 15.0) * max_strength if level > 0 else 0.0
        
        bsdf_node.inputs['Emission Strength'].default_value = strength
    
    @staticmethod
    def apply_to_objects(material: bpy.types.Material, objects: List[bpy.types.Object]) -> int:
        """
        将材质应用到多个物体
        
        Args:
            material: 要应用的材质
            objects: 物体列表
        
        Returns:
            成功应用到的物体数量
        """
        count = 0
        
        for obj in objects:
            if obj.type != 'MESH':
                continue
            
            # 获取或创建材质槽
            if len(obj.data.materials) == 0:
                obj.data.materials.append(material)
            else:
                obj.data.materials[0] = material
            
            count += 1
        
        return count


class MCBlockMaterialFactory:
    """MC 方块材质工厂 - 快速生成常见方块材质"""
    
    PREFIX = "jinkra_mine_shader_"
    
    # 常见 MC 方块的预定义属性
    BLOCK_PRESETS = {
        "stone": {
            "color": (0.55, 0.55, 0.55, 1.0),
            "roughness": 0.9,
            "metallic": 0.0,
            "emission": 0,
            "description": "石头",
        },
        "dirt": {
            "color": (0.52, 0.39, 0.26, 1.0),
            "roughness": 1.0,
            "metallic": 0.0,
            "emission": 0,
            "description": "泥土",
        },
        "grass": {
            "color": (0.4, 0.6, 0.2, 1.0),
            "roughness": 1.0,
            "metallic": 0.0,
            "emission": 0,
            "description": "草方块",
        },
        "sand": {
            "color": (0.9, 0.85, 0.7, 1.0),
            "roughness": 1.0,
            "metallic": 0.0,
            "emission": 0,
            "description": "沙子",
        },
        "oak_wood": {
            "color": (0.65, 0.5, 0.35, 1.0),
            "roughness": 0.8,
            "metallic": 0.0,
            "emission": 0,
            "description": "橡木",
        },
        "iron_ore": {
            "color": (0.6, 0.55, 0.5, 1.0),
            "roughness": 0.7,
            "metallic": 0.3,
            "emission": 0,
            "description": "铁矿石",
        },
        "gold_ore": {
            "color": (0.8, 0.7, 0.3, 1.0),
            "roughness": 0.6,
            "metallic": 0.5,
            "emission": 0,
            "description": "金矿石",
        },
        "diamond_ore": {
            "color": (0.35, 0.7, 0.8, 1.0),
            "roughness": 0.5,
            "metallic": 0.2,
            "emission": 2,
            "description": "钻石矿石",
        },
        "redstone_ore": {
            "color": (0.4, 0.2, 0.2, 1.0),
            "roughness": 0.8,
            "metallic": 0.1,
            "emission": 3,
            "description": "红石矿石",
        },
        "lapis_ore": {
            "color": (0.2, 0.2, 0.6, 1.0),
            "roughness": 0.7,
            "metallic": 0.1,
            "emission": 1,
            "description": "青金石矿石",
        },
        "glowstone": {
            "color": (0.9, 0.8, 0.4, 1.0),
            "roughness": 0.6,
            "metallic": 0.0,
            "emission": 14,
            "description": "荧石",
        },
        "water": {
            "color": (0.2, 0.5, 0.9, 0.5),
            "roughness": 0.1,
            "metallic": 0.0,
            "emission": 0,
            "description": "水",
        },
        "lava": {
            "color": (1.0, 0.3, 0.0, 1.0),
            "roughness": 0.2,
            "metallic": 0.0,
            "emission": 15,
            "description": "岩浆",
        },
    }
    
    @staticmethod
    def create_block_material(block_type: str) -> Optional[bpy.types.Material]:
        """
        根据方块类型创建材质
        
        Args:
            block_type: 方块类型（如 "stone", "grass", "glowstone"）
        
        Returns:
            创建的材质对象，或 None 如果类型不存在
        """
        if block_type not in MCBlockMaterialFactory.BLOCK_PRESETS:
            return None
        
        preset = MCBlockMaterialFactory.BLOCK_PRESETS[block_type]
        
        # 创建基础材质
        mat = MCPBRMaterialTemplate.create_standard_material(f"{block_type}")
        
        if not mat or not mat.use_nodes:
            return None
        
        # 应用预设
        bsdf_node = None
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                bsdf_node = node
                break
        
        if bsdf_node:
            bsdf_node.inputs['Base Color'].default_value = preset['color']
            bsdf_node.inputs['Roughness'].default_value = preset['roughness']
            bsdf_node.inputs['Metallic'].default_value = preset['metallic']
            
            # 设置自发光
            if preset['emission'] > 0:
                MCPBRMaterialTemplate.set_emission_level(mat, preset['emission'])
        
        return mat
    
    @staticmethod
    def get_available_blocks() -> List[str]:
        """获取所有可用的方块类型"""
        return list(MCBlockMaterialFactory.BLOCK_PRESETS.keys())
    
    @staticmethod
    def get_block_description(block_type: str) -> Optional[str]:
        """获取方块描述"""
        if block_type in MCBlockMaterialFactory.BLOCK_PRESETS:
            return MCBlockMaterialFactory.BLOCK_PRESETS[block_type]['description']
        return None


def demo_create_materials():
    """材质创建演示"""
    # 创建标准材质
    mat = MCPBRMaterialTemplate.create_standard_material("Demo_Material")
    print(f"✓ 创建材质: {mat.name}")
    
    # 添加纹理槽
    MCPBRMaterialTemplate.add_texture_slots(mat)
    print("✓ 纹理槽已添加")
    
    # 设置自发光
    MCPBRMaterialTemplate.set_emission_level(mat, 10)
    print("✓ 自发光已设置")
    
    # 创建预设材质
    for block_type in ["stone", "glowstone", "lava"]:
        block_mat = MCBlockMaterialFactory.create_block_material(block_type)
        if block_mat:
            desc = MCBlockMaterialFactory.get_block_description(block_type)
            print(f"✓ 创建预设材质: {block_type} ({desc})")


if __name__ == "__main__":
    demo_create_materials()

