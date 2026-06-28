"""
UI 面板模块 - Blender 3D 视图侧边栏

功能:
  1. 添加侧边栏面板 "JinkraMineShader"
  2. 光影包选择和加载
  3. 参数调整 UI
  4. 快速操作按钮
"""

import bpy
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, EnumProperty, BoolProperty, FloatProperty, IntProperty

# 相对导入核心模块
import sys
import os

# 添加核心模块到路径
addon_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addon_path not in sys.path:
    sys.path.insert(0, addon_path)

try:
    from jinkra_mine_shader.core.zip_parser import MCShaderZipParser
    from jinkra_mine_shader.core.shader_validator import MCShaderValidator
    from jinkra_mine_shader.core.properties_parser import PropertiesParser
    from jinkra_mine_shader.utils.logger import logger, PathHelper
except ImportError:
    # 备用：直接导入
    from core.zip_parser import MCShaderZipParser
    from core.shader_validator import MCShaderValidator
    from core.properties_parser import PropertiesParser
    from utils.logger import logger, PathHelper



class jinkra_mine_shaderParamPrevPageOperator(Operator):
    """上一页"""
    bl_idname = "jinkra_mine_shader.param_prev_page"
    bl_label = "Previous Page"
    
    def execute(self, context):
        global _shader_param_page
        _shader_param_page = max(0, _shader_param_page - 1)
        return {'FINISHED'}


class jinkra_mine_shaderParamNextPageOperator(Operator):
    """下一页"""
    bl_idname = "jinkra_mine_shader.param_next_page"
    bl_label = "Next Page"
    
    def execute(self, context):
        global _shader_param_page, _current_shader_params
        params_per_page = 8
        total_pages = (len(_current_shader_params) + params_per_page - 1) // params_per_page
        _shader_param_page = min(_shader_param_page + 1, total_pages - 1)
        return {'FINISHED'}

class jinkra_mine_shaderLoaderOperator(Operator):
    """光影包加载操作符"""
    bl_idname = "jinkra_mine_shader.load_shader_pack"
    bl_label = "Load Minecraft Shader Pack"
    
    # 文件选择对话框
    filepath: StringProperty(
        name="Shader Pack",
        description="选择 Minecraft 光影 ZIP 包",
        subtype='FILE_PATH',
        default=""
    )
    
    filter_glob: StringProperty(
        default="*.zip",
        options={'HIDDEN'}
    )
    def invoke(self, context, event):
        """打开文件选择对话框"""
        import os
        
        # 设置初始目录为桌面
        home = os.path.expanduser("~")
        desktop = os.path.join(home, "Desktop")
        downloads = os.path.join(home, "Downloads")
        
        if os.path.exists(desktop):
            self.directory = desktop
        elif os.path.exists(downloads):
            self.directory = downloads
        else:
            self.directory = home
        
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


    
    def execute(self, context):
        """执行加载操作"""
        if not self.filepath:
            self.report({'ERROR'}, "请选择一个 ZIP 文件")
            return {'CANCELLED'}
        
        try:
            logger.info(f"正在加载光影包: {self.filepath}")
            
            # 1. 解压
            parser = MCShaderZipParser(self.filepath)
            success, msg = parser.extract_zip()
            
            if not success:
                self.report({'ERROR'}, msg)
                return {'CANCELLED'}
            
            logger.info(msg)
            
            # 2. 验证
            validator = MCShaderValidator(parser.extract_dir)
            report = validator.validate_all()
            
            if not report.is_valid:
                self.report({'ERROR'}, "光影包验证失败")
                return {'CANCELLED'}
            
            logger.info(report.get_summary())
            
            # 3. 读取配置
            success, config_or_msg = parser.get_shaders_properties()
            
            if not success:
                self.report({'ERROR'}, config_or_msg)
                return {'CANCELLED'}
            
            # 4. 解析参数
            prop_parser = PropertiesParser(config_or_msg)
            
            # 保存到场景上下文
            # None = prop_parser # 属性暂不支持
            # None = parser # 属性暂不支持
            
            # 更新 UI
            context.scene.jinkra_mine_shader_loaded = True
            context.scene.jinkra_mine_shader_path = self.filepath
            context.scene.jinkra_mine_shader_param_count = len(config_or_msg)
            
            # 存储参数字典到全局变量
            global _current_shader_params
            _current_shader_params = config_or_msg if isinstance(config_or_msg, dict) else {}
            
            # 为每个参数创建 Scene 属性，以便在 UI 中显示滑块
            prop_count = 0
            failed_count = 0
            skip_count = 0
            
            print(f'[JinkraMineShader] 开始创建参数属性，总数: {len(_current_shader_params)}')
            
            for param_name, param_value in _current_shader_params.items():
                try:
                    # 清理参数名：删除/替换不合法字符
                    safe_param_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in param_name)
                    prop_key = f'shader_param_{safe_param_name}'
                    
                    # 提取可用的数值范围
                    try:
                        value = float(param_value)
                        
                        # 推断范围
                        min_val = 0.0
                        max_val = 2.0
                        if value < 0:
                            min_val = value * 2
                            max_val = max(abs(value), 1.0)
                        elif value > 1:
                            max_val = max(value * 2, 10.0)
                        
                        # 为参数创建 FloatProperty
                        if not hasattr(bpy.types.Scene, prop_key):
                            setattr(bpy.types.Scene, prop_key, 
                                   FloatProperty(
                                       name=param_name[:50], 
                                       default=value, 
                                       min=min_val, 
                                       max=max_val,
                                       step=0.01
                                   ))
                            prop_count += 1
                        
                    except (ValueError, TypeError) as ve:
                        # 无法转换为浮点数，尝试作为布尔值
                        if param_value.lower() in ('true', 'false', 'yes', 'no', '0', '1'):
                            if not hasattr(bpy.types.Scene, prop_key):
                                default_bool = param_value.lower() in ('true', 'yes', '1')
                                setattr(bpy.types.Scene, prop_key, BoolProperty(name=param_name[:50], default=default_bool))
                                prop_count += 1
                        else:
                            skip_count += 1
                            
                except Exception as e:
                    failed_count += 1
                    print(f'[JinkraMineShader] 创建属性失败 {param_name}: {str(e)[:100]}')
            
            print(f'[JinkraMineShader] 参数属性创建完成: 成功={prop_count}, 跳过={skip_count}, 失败={failed_count}')
            
            self.report({'INFO'}, f"✓ 光影包加载成功！包含 {len(config_or_msg)} 个参数")
            logger.info("光影包加载完成")
            
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"加载失败: {str(e)}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        """调用文件选择对话框"""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class jinkra_mine_shaderCreateEnvironmentOperator(Operator):
    """创建 MC 环境操作符"""
    bl_idname = "jinkra_mine_shader.create_environment"
    bl_label = "Create MC Environment"

    
    def execute(self, context):
        """创建 MC 环保光照环境"""
        try:
            import bpy
            import math
            
            logger.info("创建 MC 环境...")
            
            # 1. 设置渲染引擎为 EEVEE
            context.scene.render.engine = 'BLENDER_EEVEE'
            # Blender 5.1+ 的 EEVEE 配置已移至其他位置，跳过
            
            # 2. 创建世界环境
            world = context.scene.world
            world.use_nodes = True
            bg_node = world.node_tree.nodes['Background']
            bg_node.inputs['Strength'].default_value = 1.5
            
            # 设置天空颜色（蓝天）
            bg_node.inputs['Color'].default_value = (0.53, 0.81, 0.92, 1.0)
            
            # 3. 创建太阳光
            sun_data = bpy.data.lights.new('MC_SHADER_Sun', type='SUN')
            sun_data.energy = 2.0
            sun_data.color = (1.0, 0.98, 0.8)
            
            sun_obj = bpy.data.objects.new('MC_SHADER_Sun', sun_data)
            context.collection.objects.link(sun_obj)
            sun_obj.location = (50, 50, 50)
            sun_obj.rotation_euler = (math.radians(45), math.radians(45), 0)
            
            # 4. 创建环境光
            sky_data = bpy.data.lights.new('MC_SHADER_Sky', type='SUN')
            sky_data.energy = 0.3
            sky_data.color = (0.3, 0.5, 1.0)
            
            sky_obj = bpy.data.objects.new('MC_SHADER_Sky', sky_data)
            context.collection.objects.link(sky_obj)
            sky_obj.location = (-50, -50, 50)
            sky_obj.rotation_euler = (math.radians(135), math.radians(225), 0)
            
            logger.info("✓ MC 环境创建成功")
            self.report({'INFO'}, "✓ MC 环境创建成功")
            return {'FINISHED'}
        
        except Exception as e:
            logger.error(f"创建 MC 环境失败: {e}")
            self.report({'ERROR'}, f"创建失败: {e}")
            return {'CANCELLED'}
            
            self.report({'INFO'}, "✓ 环境创建成功")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"环境创建失败: {str(e)}")
            return {'CANCELLED'}


class jinkra_mine_shaderCreateMaterialOperator(Operator):
    """给选中物体创建 MC 材质"""
    bl_idname = "jinkra_mine_shader.create_material"
    bl_label = "Create MC Material"

    
    def execute(self, context):
        """为选中物体创建标准 MC PBR 材质"""
        if not context.selected_objects:
            self.report({'WARNING'}, "请先选中一个或多个物体")
            return {'CANCELLED'}
        
        try:
            logger.info(f"为 {len(context.selected_objects)} 个物体创建材质...")
            
            # 动态导入材质模块
            try:
                from jinkra_mine_shader.materials.pbr_template import MCBlockMaterialFactory
            except ImportError:
                from materials.pbr_template import MCBlockMaterialFactory
            
            # 创建草方块材质作为默认
            mat = MCBlockMaterialFactory.create_block_material("grass")
            
            if not mat:
                self.report({'ERROR'}, "材质创建失败")
                return {'CANCELLED'}
            
            # 应用到选中物体
            count = 0
            for obj in context.selected_objects:
                if obj.type == 'MESH':
                    if len(obj.data.materials) == 0:
                        obj.data.materials.append(mat)
                    else:
                        obj.data.materials[0] = mat
                    count += 1
            
            self.report({'INFO'}, f"✓ 为 {count} 个物体创建材质成功")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"材质创建失败: {str(e)}")
            return {'CANCELLED'}


class JinkraMineShaderPanel(Panel):
    """JinkraMineShader 侧边栏面板"""
    bl_label = "JinkraMineShader"
    bl_idname = "VIEW3D_PT_jinkra_mine_shader"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JinkraMineShader"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        """绘制面板内容"""
        layout = self.layout
        scene = context.scene
        
        # ===== 第一部分：光影包加载 =====
        box = layout.box()
        box.label(text="📦 光影包加载", icon='PACKAGE')
        
        if not scene.jinkra_mine_shader_loaded:
            # 未加载状态
            box.operator(
                "jinkra_mine_shader.load_shader_pack",
                text="选择光影包",
                icon='FILE_FOLDER'
            )
        else:
            # 已加载状态
            box.label(text=f"✓ 已加载", icon='CHECKMARK')
            box.label(text=f"参数数量: {scene.jinkra_mine_shader_param_count}", icon='PROPERTIES')
            
            # 重新加载按钮
            box.operator(
                "jinkra_mine_shader.load_shader_pack",
                text="重新加载",
                icon='FILE_REFRESH'
            )
        
        layout.separator()
        
        # ===== 第二部分：快速操作 =====
        box = layout.box()
        box.label(text="⚙️ 快速操作", icon='TOOL_SETTINGS')
        
        box.operator(
            "jinkra_mine_shader.create_environment",
            text="创建 MC 环境",
            icon='WORLD'
        )
        
        box.operator(
            "jinkra_mine_shader.create_material",
            text="创建 MC 材质",
            icon='MATERIAL'
        )
        
        layout.separator()
        
        # ===== 第三部分：光影参数 =====
        box = layout.box()
        box.label(text="⚙️ 光影参数", icon='PROPERTIES')
        
        scene = context.scene
        param_count = getattr(scene, 'jinkra_mine_shader_param_count', 0)
        
        if param_count > 0:
            box.label(text=f"已加载 {param_count} 个参数", icon='INFO')
            
            # 获取全局参数数据
            global _current_shader_params, _shader_param_page
            param_data = _current_shader_params
            
            # 确保 _shader_param_page 已初始化
            if '_shader_param_page' not in globals():
                _shader_param_page = 0
            
            if isinstance(param_data, dict):
                # 每页显示 8 个参数
                params_per_page = 8
                all_params = list(param_data.items())
                total_pages = (len(all_params) + params_per_page - 1) // params_per_page
                
                # 确保页码有效
                _shader_param_page = max(0, min(_shader_param_page, total_pages - 1))
                
                # 计算当前页的参数范围
                start_idx = _shader_param_page * params_per_page
                end_idx = start_idx + params_per_page
                page_params = all_params[start_idx:end_idx]
                
                # 调试日志
                print(f'[JinkraMineShader] 参数显示调试: 总参数={len(all_params)}, 总页数={total_pages}, 当前页={_shader_param_page}, 当前页参数={len(page_params)}')
                
                # 显示当前页的参数
                col = box.column(align=True)
                param_displayed = 0
                for param_name, param_value in page_params:
                    try:
                        # 使用安全的参数名
                        safe_param_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in param_name)
                        prop_key = f'shader_param_{safe_param_name}'
                        
                        if hasattr(scene, prop_key):
                            row = col.row(align=True)
                            row.label(text=param_name[:25], icon='BLANK1')
                            row.prop(scene, prop_key, text='', slider=True)
                            param_displayed += 1
                        else:
                            print(f'[JinkraMineShader] 属性不存在: {prop_key}')
                    except Exception as e:
                        print(f'[JinkraMineShader] 显示参数出错: {e}')
                
                print(f'[JinkraMineShader] 本页显示了 {param_displayed} 个参数滑块')
                
                # 翻页控件
                if total_pages > 1:
                    row = box.row(align=True)
                    
                    # 上一页按钮
                    if _shader_param_page > 0:
                        row.operator("jinkra_mine_shader.param_prev_page", text="< 上一页")
                    
                    # 页码信息
                    row.label(text=f"第 {_shader_param_page + 1}/{total_pages} 页")
                    
                    # 下一页按钮
                    if _shader_param_page < total_pages - 1:
                        row.operator("jinkra_mine_shader.param_next_page", text="下一页 >")
        else:
            box.label(text="未加载光影参数", icon='INFO')
            box.label(text="（某些光影包不提供参数）", icon='BLANK1')


class jinkra_mine_shaderProperties(PropertyGroup):
    """JinkraMineShader 相关属性"""
    
    # 加载状态
    jinkra_mine_shader_loaded: BoolProperty(
        name="Shader Loaded",
        description="是否已加载光影包",
        default=False
    )
    
    jinkra_mine_shader_path: StringProperty(
        name="Shader Path",
        description="光影包文件路径",
        default=""
    )
    
    jinkra_mine_shader_param_count: IntProperty(
        name="Parameter Count",
        description="光影包参数总数",
        default=0
    )


def register():
    """注册 UI 类"""
    try:
        bpy.utils.register_class(jinkra_mine_shaderProperties)
    except RuntimeError:
        pass
    
    try:
        bpy.utils.register_class(jinkra_mine_shaderLoaderOperator)
    except RuntimeError:
        pass
    
    try:
        bpy.utils.register_class(jinkra_mine_shaderCreateEnvironmentOperator)
    except RuntimeError:
        pass
    
    try:
        bpy.utils.register_class(jinkra_mine_shaderCreateMaterialOperator)
    except RuntimeError:
        pass
    
    try:
        bpy.utils.register_class(jinkra_mine_shaderParamPrevPageOperator)
    except RuntimeError:
        pass
    
    try:
        bpy.utils.register_class(jinkra_mine_shaderParamNextPageOperator)
    except RuntimeError:
        pass
    
    try:
        bpy.utils.register_class(JinkraMineShaderPanel)
    except RuntimeError:
        pass
    
    # 添加属性到 Scene
    try:
        bpy.types.Scene.jinkra_mine_shader_props = bpy.props.PointerProperty(type=jinkra_mine_shaderProperties)
    except:
        pass
    
    # 快捷属性
    try:
        bpy.types.Scene.jinkra_mine_shader_loaded = BoolProperty(default=False)
        bpy.types.Scene.jinkra_mine_shader_path = StringProperty(default="")
        bpy.types.Scene.jinkra_mine_shader_param_count = IntProperty(default=0)
    except:
        pass


def unregister():
    """注销 UI 类"""
    # 移除属性
    for attr in ['jinkra_mine_shader_props', 'jinkra_mine_shader_loaded', 'jinkra_mine_shader_path', 'jinkra_mine_shader_param_count']:
        if hasattr(bpy.types.Scene, attr):
            try:
                delattr(bpy.types.Scene, attr)
            except:
                pass
    
    # 注销类
    try:
        bpy.utils.unregister_class(JinkraMineShaderPanel)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(jinkra_mine_shaderCreateMaterialOperator)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(jinkra_mine_shaderParamNextPageOperator)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(jinkra_mine_shaderParamPrevPageOperator)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(jinkra_mine_shaderCreateEnvironmentOperator)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(jinkra_mine_shaderLoaderOperator)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(jinkra_mine_shaderProperties)
    except:
        pass



