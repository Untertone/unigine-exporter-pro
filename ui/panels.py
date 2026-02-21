# ui/panels.py
import bpy
import os
from bpy.types import Panel
from ..utils.animation_utils import AnimationExporter

def has_armature(objects):
    """Проверить наличие арматуры"""
    for obj in objects:
        if obj.type == 'ARMATURE':
            return True
    return False

def get_material_count(objects):
    """Получить количество материалов"""
    count = 0
    for obj in objects:
        if obj.type == 'MESH' and obj.data.materials:
            count += len(obj.data.materials)
    return count

class UNIGINE_PT_main_panel(Panel):
    bl_label = "Unigine Exporter Pro"
    bl_idname = "UNIGINE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unigine"
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.unigine
        
        layout.label(text="Professional Exporter", icon='WORLD')
        layout.label(text="v2.1.0 | Batch Export")
        
        if settings.project_path:
            if os.path.exists(settings.project_path):
                layout.label(text="✅ Project OK", icon='CHECKMARK')
            else:
                layout.label(text="❌ Path not found", icon='ERROR')
        else:
            layout.label(text="⚠️ Set project path", icon='INFO')


class UNIGINE_PT_export_mode(Panel):
    bl_label = "Export Mode"
    bl_idname = "UNIGINE_PT_export_mode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unigine"
    bl_parent_id = "UNIGINE_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.unigine
        
        layout.prop(settings, "export_mode", expand=True)
        
        if settings.export_mode == 'SINGLE':
            layout.prop(settings, "asset_name")
            
        elif settings.export_mode == 'BATCH':
            box = layout.box()
            box.label(text="Naming:", icon='FILE')
            box.prop(settings, "batch_prefix")
            box.prop(settings, "batch_suffix")
            box.prop(settings, "auto_number")
            if settings.auto_number:
                box.prop(settings, "number_padding")


class UNIGINE_PT_project_settings(Panel):
    bl_label = "Project Settings"
    bl_idname = "UNIGINE_PT_project_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unigine"
    bl_parent_id = "UNIGINE_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.unigine
        
        layout.prop(settings, "project_path")
        layout.prop(settings, "mesh_path")
        layout.prop(settings, "texture_path")


class UNIGINE_PT_material_settings(Panel):
    bl_label = "Materials"
    bl_idname = "UNIGINE_PT_material_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unigine"
    bl_parent_id = "UNIGINE_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.unigine
        
        layout.prop(settings, "export_materials")
        if settings.export_materials:
            layout.prop(settings, "copy_textures")
            if settings.copy_textures:
                layout.prop(settings, "texture_handling")


class UNIGINE_PT_animation_settings(Panel):
    bl_label = "Animation"
    bl_idname = "UNIGINE_PT_animation_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unigine"
    bl_parent_id = "UNIGINE_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.unigine
        anim_mgr = AnimationExporter()
        
        # Проверка наличия арматуры
        has_arm = False
        if context.selected_objects:
            has_arm = anim_mgr.has_armature(context.selected_objects)
        
        if has_arm:
            layout.label(text="✅ Armature detected", icon='ARMATURE_DATA')
        else:
            layout.label(text="❌ No armature selected", icon='ERROR')
        
        layout.prop(settings, "export_animation")
        
        if settings.export_animation and has_arm:
            layout.prop(settings, "bake_animation")
            layout.prop(settings, "animation_fps")
            
            # Диапазон кадров
            if context.selected_objects:
                start, end = anim_mgr.get_animation_range(context.selected_objects)
                layout.label(text=f"Frames: {start}-{end}")


class UNIGINE_PT_export_options(Panel):
    bl_label = "Options"
    bl_idname = "UNIGINE_PT_export_options"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unigine"
    bl_parent_id = "UNIGINE_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.unigine
        
        layout.prop(settings, "export_selected")
        layout.prop(settings, "create_node")
        layout.prop(settings, "verbose")


class UNIGINE_PT_export_button(Panel):
    bl_label = "Export"
    bl_idname = "UNIGINE_PT_export_button"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unigine"
    bl_parent_id = "UNIGINE_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.unigine
        
        # Проверка готовности
        can_export = True
        issues = []
        
        if not settings.project_path:
            can_export = False
            issues.append("• Project path not set")
        elif not os.path.exists(settings.project_path):
            can_export = False
            issues.append("• Project path does not exist")
        
        if settings.export_mode == 'SINGLE' and not settings.asset_name:
            can_export = False
            issues.append("• Asset name not set")
        
        if settings.export_selected and not context.selected_objects:
            can_export = False
            issues.append("• No objects selected")
        
        # Показываем проблемы
        if issues:
            box = layout.box()
            box.label(text="Cannot export:", icon='ERROR')
            for issue in issues:
                box.label(text=issue)
        
        # Кнопка экспорта
        row = layout.row(align=True)
        row.scale_y = 2.0
        
        if can_export:
            # Определяем, что экспортируется
            export_info = []
            if settings.export_materials:
                export_info.append("Mats")
            if settings.export_animation and has_armature(context.selected_objects):
                export_info.append("Anim")
            
            if export_info:
                text = f"EXPORT ({', '.join(export_info)})"
            else:
                text = "EXPORT (Model only)"
            
            row.operator("unigine.export", icon='EXPORT', text=text)
        else:
            row.operator("unigine.export", icon='ERROR', text="FIX SETTINGS")
        
        # Тестовая кнопка
        row = layout.row(align=True)
        row.operator("unigine.test", icon='QUESTION', text="Test")


class UNIGINE_PT_help(Panel):
    bl_label = "Help"
    bl_idname = "UNIGINE_PT_help"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unigine"
    bl_parent_id = "UNIGINE_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="Quick Guide:", icon='INFO')
        box.label(text="1. Set project path")
        box.label(text="2. Choose export mode")
        box.label(text="3. Select objects")
        box.label(text="4. Configure options")
        box.label(text="5. Click EXPORT")
        
        box = layout.box()
        box.label(text="Export Modes:", icon='EXPORT')
        box.label(text="• Single: One model with custom name")
        box.label(text="• Batch: Each selected object as separate model")
        box.label(text="• Collection: Each collection as separate model")

# Список всех панелей
panels = [
    UNIGINE_PT_main_panel,
    UNIGINE_PT_export_mode,
    UNIGINE_PT_project_settings,
    UNIGINE_PT_material_settings,
    UNIGINE_PT_animation_settings,
    UNIGINE_PT_export_options,
    UNIGINE_PT_export_button,
    UNIGINE_PT_help,
]