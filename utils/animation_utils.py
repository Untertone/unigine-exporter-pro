# utils/animation_utils.py
import bpy

class AnimationExporter:
    """Класс для работы с анимациями"""
    
    def __init__(self, logger=None):
        self.logger = logger or print
    
    def log(self, msg, level='INFO'):
        if self.logger:
            self.logger(f"[Animation] {msg}")
    
    def has_armature(self, objects):
        """Проверить наличие арматуры"""
        for obj in objects:
            if obj.type == 'ARMATURE':
                return True
        return False
    
    def get_animation_range(self, objects):
        """Получить диапазон анимации"""
        start = float('inf')
        end = float('-inf')
        
        for obj in objects:
            if obj.animation_data and obj.animation_data.action:
                action = obj.animation_data.action
                if action.frame_range:
                    s, e = action.frame_range
                    start = min(start, s)
                    end = max(end, e)
        
        if start == float('inf'):
            start = bpy.context.scene.frame_start
            end = bpy.context.scene.frame_end
        
        return int(start), int(end)

def register():
    pass

def unregister():
    pass