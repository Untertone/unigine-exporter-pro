# utils/file_utils.py
import os

class FileManager:
    """Класс для работы с файловой системой"""
    
    def __init__(self, logger=None):
        self.logger = logger or print
    
    def log(self, msg, level='INFO'):
        if self.logger:
            self.logger(f"[File] {msg}")
    
    def ensure_directory(self, path):
        """Создать директорию если не существует"""
        os.makedirs(path, exist_ok=True)
        return path
    
    def create_node_file(self, folder, asset_name, mesh_path, material_guid, material_name):
        """Создать .node файл для Unigine"""
        node_path = os.path.join(folder, f"{asset_name}.node")
        
        content = f'''<?xml version="1.0" encoding="utf-8"?>
<nodes version="2.5.0.2">
    <node type="ObjectMeshStatic" id="0" name="{asset_name}">
        <mesh>{mesh_path}/{asset_name}.mesh</mesh>
        <material guid="{material_guid}">{material_name}</material>
        <transform>1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</transform>
    </node>
</nodes>'''
        
        try:
            with open(node_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log(f"✅ .node: {asset_name}.node")
            return node_path
        except Exception as e:
            self.log(f"❌ Ошибка создания .node: {e}", 'ERROR')
            return None

def register():
    pass

def unregister():
    pass