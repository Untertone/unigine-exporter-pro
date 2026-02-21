# utils/texture_utils.py
import os
import shutil

class TextureManager:
    """Класс для управления текстурами"""
    
    def __init__(self, logger=None):
        self.logger = logger or print
    
    def log(self, msg, level='INFO'):
        if self.logger:
            self.logger(f"[Texture] {msg}")
    
    def copy_texture(self, tex_path, project_path, texture_folder):
        """Скопировать текстуру в проект"""
        if not os.path.exists(tex_path):
            return None
        
        target_dir = os.path.join(project_path, "data", texture_folder)
        os.makedirs(target_dir, exist_ok=True)
        
        filename = os.path.basename(tex_path)
        target_path = os.path.join(target_dir, filename)
        
        if not os.path.exists(target_path):
            shutil.copy2(tex_path, target_path)
            self.log(f"📋 Скопирована: {filename}")
        else:
            self.log(f"⏭️ Уже существует: {filename}")
        
        return os.path.join(texture_folder, filename).replace('\\', '/')
    
    def copy_textures_to_fbm(self, fbx_path, textures_dict):
        """Скопировать текстуры в папку .fbm"""
        fbm_folder = fbx_path + ".fbm"
        os.makedirs(fbm_folder, exist_ok=True)
        
        copied = 0
        for tex_path in textures_dict.keys():
            filename = os.path.basename(tex_path)
            dst = os.path.join(fbm_folder, filename)
            
            if not os.path.exists(dst):
                shutil.copy2(tex_path, dst)
                copied += 1
        
        return copied

def register():
    pass

def unregister():
    pass