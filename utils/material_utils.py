# utils/material_utils.py
import os
import uuid
import bpy

class MaterialExporter:
    """Класс для экспорта материалов в Unigine"""
    
    def __init__(self, logger=None):
        self.logger = logger or print
        self.materials = {}
        self.guids = {}
    
    def log(self, msg, level='INFO'):
        if self.logger:
            self.logger(f"[Material] {msg}")
    
    def extract_textures(self, material):
        """Извлечь текстуры из материала"""
        textures = {}
        
        if not material or not material.use_nodes:
            return textures
        
        self.log(f"Анализ материала: {material.name}")
        
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                tex_path = bpy.path.abspath(node.image.filepath)
                
                if not tex_path or not os.path.exists(tex_path):
                    continue
                
                filename = os.path.basename(tex_path).lower()
                tex_type = 'unknown'
                
                if 'diffuse' in filename or 'albedo' in filename or 'color' in filename:
                    tex_type = 'diffuse'
                elif 'normal' in filename:
                    tex_type = 'normal'
                elif 'metallic' in filename:
                    tex_type = 'metallic'
                elif 'roughness' in filename or 'gloss' in filename:
                    tex_type = 'roughness'
                elif 'specular' in filename:
                    tex_type = 'specular'
                elif 'emission' in filename or 'emissive' in filename:
                    tex_type = 'emission'
                elif 'ao' in filename or 'ambient' in filename:
                    tex_type = 'ao'
                elif 'opacity' in filename or 'alpha' in filename:
                    tex_type = 'opacity'
                
                if tex_type != 'unknown':
                    textures[tex_type] = tex_path
                    self.log(f"  + {tex_type}: {os.path.basename(tex_path)}")
        
        return textures
    
    def collect_all_textures(self, objects):
        """Собрать все текстуры со всех объектов"""
        textures = {}
        
        for obj in objects:
            if obj.type == 'MESH' and obj.data.materials:
                for material in obj.data.materials:
                    if material:
                        mat_textures = self.extract_textures(material)
                        textures.update(mat_textures)
        
        return textures
    
    def create_material_file(self, material_name, textures, materials_folder, texture_path):
        """Создать .mat файл для Unigine"""
        safe_name = material_name.replace(' ', '_').replace('.', '_')
        mat_path = os.path.join(materials_folder, f"{safe_name}.mat")
        
        guid = uuid.uuid4().hex
        self.guids[material_name] = guid
        
        xml = f'''<?xml version="1.0" encoding="utf-8"?>
<material version="2.0" guid="{guid}" name="{safe_name}">
    <parameters>'''
        
        for tex_type, tex_path in textures.items():
            rel_path = os.path.join(texture_path, os.path.basename(tex_path)).replace('\\', '/')
            xml += f'\n        <texture name="{tex_type}">{rel_path}</texture>'
        
        xml += '''
    </parameters>
    <states>
        <state name="cull">back</state>
        <state name="blend">false</state>
        <state name="depth_test">true</state>
        <state name="depth_write">true</state>
    </states>
</material>'''
        
        try:
            with open(mat_path, 'w', encoding='utf-8') as f:
                f.write(xml)
            self.log(f"✅ .mat: {safe_name}.mat")
            return guid
        except Exception as e:
            self.log(f"❌ Ошибка создания .mat: {e}", 'ERROR')
            return None

def register():
    pass

def unregister():
    pass