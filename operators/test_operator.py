# operators/test_operator.py
import bpy
from bpy.types import Operator
from ..utils.animation_utils import AnimationExporter

class UNIGINE_OT_test(Operator):
    bl_idname = "unigine.test"
    bl_label = "Test"
    
    def execute(self, context):
        settings = context.scene.unigine
        anim_mgr = AnimationExporter()
        
        print("\n✅ Плагин v2.1.0 работает!")
        print(f"Project: {settings.project_path}")
        print(f"Mode: {settings.export_mode}")
        print(f"Materials: {settings.export_materials}")
        print(f"Animation: {settings.export_animation}")
        
        if settings.export_selected and context.selected_objects:
            has_arm = anim_mgr.has_armature(context.selected_objects)
            print(f"Has Armature: {has_arm}")
            
            if has_arm:
                start, end = anim_mgr.get_animation_range(context.selected_objects)
                print(f"Animation Range: {start}-{end}")
        
        self.report({'INFO'}, "Плагин работает!")
        return {'FINISHED'}