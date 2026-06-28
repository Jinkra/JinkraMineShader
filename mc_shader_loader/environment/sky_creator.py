"""
环境和光照创建模块

功能:
  1. 创建 MC 日光天空环境
  2. 设置太阳光和环保光
  3. 昼夜时间系统
  4. 天气模式切换
"""

import bpy
import math
from typing import Optional, Tuple


class MCEnvironmentCreator:
    """MC 环境创建器"""
    
    PREFIX = "jinkra_mine_shader_"
    
    @staticmethod
    def create_world_environment() -> Optional[bpy.types.World]:
        """
        创建或获取 MC 光影世界环境
        
        Returns:
            创建的世界对象
        """
        # 创建新世界
        world = bpy.data.worlds.new(name=f"{MCEnvironmentCreator.PREFIX}World")
        
        # 设置为 EEVEE 兼容的蓝天
        world.use_nodes = True
        nodes = world.node_tree.nodes
        links = world.node_tree.links
        
        # 清空默认节点
        nodes.clear()
        
        # 创建节点
        output_node = nodes.new(type='ShaderNodeOutputWorld')
        background_node = nodes.new(type='ShaderNodeBackground')
        color_ramp = nodes.new(type='ShaderNodeValRamp')
        mapping = nodes.new(type='ShaderNodeMapping')
        coord = nodes.new(type='ShaderNodeTexCoord')
        
        # 连接节点
        links.new(background_node.outputs['Background'], output_node.inputs['Surface'])
        
        # 配置背景颜色（天蓝色）
        background_node.inputs['Color'].default_value = (0.1, 0.5, 1.0, 1.0)  # 蓝色
        background_node.inputs['Strength'].default_value = 1.0
        
        return world
    
    @staticmethod
    def create_sun_light() -> Optional[bpy.types.Object]:
        """
        创建太阳光
        
        Returns:
            太阳光对象
        """
        # 创建太阳光（平行光）
        sun_data = bpy.data.lights.new(
            name=f"{MCEnvironmentCreator.PREFIX}Sun",
            type='SUN'
        )
        
        sun_obj = bpy.data.objects.new(
            name=f"{MCEnvironmentCreator.PREFIX}Sun",
            object_data=sun_data
        )
        
        # 添加到场景
        bpy.context.collection.objects.link(sun_obj)
        
        # 配置太阳光
        sun_data.angle = math.radians(0.5)  # 太阳角度 0.5 度
        sun_data.energy = 2.0  # 强度
        sun_data.color = (1.0, 1.0, 1.0)  # 白色
        
        # 位置和方向
        sun_obj.location = (0, 0, 10)
        sun_obj.rotation_euler = (math.radians(45), 0, 0)
        
        return sun_obj
    
    @staticmethod
    def create_ambient_light() -> Optional[bpy.types.Object]:
        """
        创建环保光（Area Light，模拟漫反射）
        
        Returns:
            环保光对象
        """
        # 创建面光源
        light_data = bpy.data.lights.new(
            name=f"{MCEnvironmentCreator.PREFIX}Ambient",
            type='AREA'
        )
        
        light_obj = bpy.data.objects.new(
            name=f"{MCEnvironmentCreator.PREFIX}Ambient",
            object_data=light_data
        )
        
        # 添加到场景
        bpy.context.collection.objects.link(light_obj)
        
        # 配置环保光
        light_data.energy = 0.5
        light_data.color = (0.8, 0.8, 1.0)  # 冷色调蓝光
        light_data.size = 20  # 大面光源
        
        # 位置
        light_obj.location = (5, 5, 8)
        
        return light_obj
    
    @staticmethod
    def setup_eevee_render_settings():
        """配置 EEVEE 渲染引擎设置"""
        scene = bpy.context.scene
        
        # 切换到 EEVEE
        scene.render.engine = 'BLENDER_EEVEE'
        
        # 获取 EEVEE 设置
        eevee = scene.eevee
        
        # 启用高级功能
        eevee.use_bloom = True
        eevee.bloom_intensity = 0.5
        eevee.bloom_radius = 1.0
        eevee.bloom_threshold = 0.75
        
        eevee.use_volumetric_lights = True
        eevee.volumetric_start = 0.1
        eevee.volumetric_end = 10.0
        
        # 环保遮蔽
        eevee.use_gtao = True
        eevee.gtao_distance = 1.0
        eevee.gtao_factor = 1.0
        
        # 反射
        eevee.use_ssr = True
        eevee.ssr_thickness = 0.2
        eevee.ssr_edge_fadeout = 0.75
        
        # 景深
        eevee.use_dof = False
        
        # 动态模糊
        eevee.use_motion_blur = False
        
        # 阴影
        eevee.shadow_cascade_size = '1024'
        eevee.use_soft_shadows = True
        eevee.light_threshold = 0.0
        
        return True


class DayNightController:
    """昼夜系统控制器"""
    
    def __init__(self, sun_obj: Optional[bpy.types.Object] = None):
        """
        初始化昼夜控制器
        
        Args:
            sun_obj: 太阳光对象（可选）
        """
        self.sun_obj = sun_obj
        self.time = 0.0  # 0-24 小时
        self.hour_angle = 360 / 24  # 每小时的旋转角度
    
    def set_time(self, hour: float):
        """
        设置时间（0-24 小时）
        
        Args:
            hour: 小时（0-24）
        """
        self.time = max(0, min(24, hour))
        
        if self.sun_obj:
            # 根据时间旋转太阳
            angle_z = math.radians((self.time - 6) * self.hour_angle)
            angle_x = math.radians(45)  # 固定的仰角
            
            self.sun_obj.rotation_euler = (angle_x, 0, angle_z)
            
            # 更新天空颜色和光照强度
            self._update_sky_color()
    
    def _update_sky_color(self):
        """根据时间更新天空颜色"""
        hour = self.time
        
        # 天空颜色梯度
        # 0:00 - 夜间黑色
        # 6:00 - 日出
        # 12:00 - 正午蓝色
        # 18:00 - 日落
        # 24:00 - 夜间黑色
        
        if hour < 6 or hour >= 22:
            # 夜间
            r, g, b = 0.05, 0.05, 0.1
        elif 6 <= hour < 8:
            # 日出
            t = (hour - 6) / 2
            r = 0.5 + 0.5 * t
            g = 0.3 + 0.2 * t
            b = 0.1 + 0.9 * t
        elif 8 <= hour < 18:
            # 白天
            r = 0.1 + 0.1 * (hour - 8) / 10
            g = 0.5 + 0.2 * (hour - 8) / 10
            b = 1.0
        elif 18 <= hour < 20:
            # 日落
            t = (hour - 18) / 2
            r = 1.0 - 0.7 * t
            g = 0.7 - 0.5 * t
            b = 1.0 - 0.8 * t
        else:
            # 傍晚到夜间
            t = (hour - 20) / 4
            r = 0.3 * (1 - t)
            g = 0.2 * (1 - t)
            b = 0.2 + 0.1 * (1 - t)
        
        # 更新世界背景色
        if bpy.context.scene.world:
            bg = bpy.context.scene.world.node_tree.nodes.get("Background")
            if bg:
                bg.inputs['Color'].default_value = (r, g, b, 1.0)
            
            # 更新灯光
            if self.sun_obj and self.sun_obj.data.type == 'SUN':
                # 根据时间调整灯光强度
                if hour < 6 or hour >= 20:
                    strength = 0.0  # 夜间无阳光
                elif 6 <= hour < 8 or 18 <= hour < 20:
                    # 日出/日落较弱
                    t = (hour - 6) / 2 if hour < 8 else (hour - 18) / 2
                    strength = 2.0 * t
                else:
                    strength = 2.0
                
                self.sun_obj.data.energy = strength


class WeatherController:
    """天气系统控制器"""
    
    WEATHER_MODES = {
        "clear": {
            "fog_density": 0.001,
            "exposure": 1.0,
            "rain_strength": 0.0,
        },
        "rain": {
            "fog_density": 0.01,
            "exposure": 0.7,
            "rain_strength": 1.0,
        },
        "fog": {
            "fog_density": 0.05,
            "exposure": 0.8,
            "rain_strength": 0.0,
        },
    }
    
    def __init__(self):
        """初始化天气控制器"""
        self.current_mode = "clear"
    
    def set_weather(self, mode: str):
        """
        切换天气模式
        
        Args:
            mode: 天气模式 ("clear", "rain", "fog")
        """
        if mode not in self.WEATHER_MODES:
            return False
        
        self.current_mode = mode
        settings = self.WEATHER_MODES[mode]
        
        # 应用设置（这里需要与参数系统集成）
        # TODO: 更新场景参数
        
        return True


def register():
    """注册环境模块"""
    pass


def unregister():
    """注销环境模块"""
    pass

