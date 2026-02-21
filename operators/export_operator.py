# operators/export_operator.py
import bpy
import os
import shutil
from bpy.types import Operator
from ..utils.material_utils import MaterialExporter
from ..utils.texture_utils import TextureManager
from ..utils.animation_utils import AnimationExporter
from ..utils.file_utils import FileManager

class UNIGINE_OT_export(Operator):
    bl_idname = "unigine.export"
    bl_label = "Export to Unigine"
    bl_options = {'REGISTER', 'UNDO'}
    
    def log(self, msg, level='INFO'):
        settings = bpy.context.scene.unigine
        if settings.verbose or level == 'ERROR':
            print(f"[{level}] {msg}")
        if level == 'ERROR':
            self.report({'ERROR'}, msg)
    
    def get_models_for_export(self, context, settings):
        """Получить список моделей для экспорта"""
        models = []
        
        if settings.export_mode == 'SINGLE':
            objects = context.selected_objects if settings.export_selected else context.scene.objects
            models.append((settings.asset_name, objects))
            
        elif settings.export_mode == 'BATCH':
            selected = context.selected_objects
            meshes = [obj for obj in selected if obj.type == 'MESH']
            
            for i, obj in enumerate(meshes):
                name = settings.batch_prefix + obj.name + settings.batch_suffix
                if settings.auto_number:
                    number = str(i + 1).zfill(settings.number_padding)
                    name = f"{name}_{number}"
                
                # Собираем связанные объекты
                related = [obj]
                for child in obj.children:
                    if child.type in {'MESH', 'ARMATURE'}:
                        related.append(child)
                
                models.append((name, related))
        
        elif settings.export_mode == 'COLLECTION':
            for collection in bpy.data.collections:
                if collection.objects:
                    name = settings.batch_prefix + collection.name + settings.batch_suffix
                    models.append((name, list(collection.objects)))
        
        return models
    
    def export_single_model(self, context, settings, model_name, objects):
        """Экспортировать одну модель"""
        self.log(f"\n  🔨 Экспорт модели: {model_name}")
        
        # Инициализируем менеджеры
        material_mgr = MaterialExporter(self.log)
        texture_mgr = TextureManager(self.log)
        anim_mgr = AnimationExporter(self.log)
        file_mgr = FileManager(self.log)
        
        # Создаём папки
        mesh_folder = os.path.join(settings.project_path, "data", settings.mesh_path)
        materials_folder = os.path.join(settings.project_path, "data", "materials")
        textures_folder = os.path.join(settings.project_path, "data", settings.texture_path)
        
        file_mgr.ensure_directory(mesh_folder)
        file_mgr.ensure_directory(materials_folder)
        file_mgr.ensure_directory(textures_folder)
        
        has_arm = anim_mgr.has_armature(objects)
        
        # 1. Собираем и экспортируем материалы
        all_textures = {}
        material_guid = None
        material_name = None
        
        if settings.export_materials or settings.copy_textures:
            all_textures = material_mgr.collect_all_textures(objects)
            
            if settings.export_materials:
                # Собираем уникальные материалы
                materials = set()
                for obj in objects:
                    if obj.type == 'MESH' and obj.data.materials:
                        for mat in obj.data.materials:
                            if mat:
                                materials.add(mat)
                
                for material in materials:
                    textures = material_mgr.extract_textures(material)
                    
                    if textures and settings.copy_textures:
                        processed = {}
                        for tex_type, tex_path in textures.items():
                            rel_path = texture_mgr.copy_texture(tex_path, settings.project_path, settings.texture_path)
                            if rel_path:
                                processed[tex_type] = rel_path
                        
                        if processed:
                            guid = material_mgr.create_material_file(
                                material.name, processed, materials_folder, settings.texture_path
                            )
                            if guid and not material_guid:
                                material_guid = guid
                                material_name = material.name.replace(' ', '_')
        
        # 2. Экспорт FBX
        fbx_path = os.path.join(mesh_folder, f"{model_name}.fbx")
        
        # Сохраняем текущее выделение
        old_selection = context.selected_objects[:]
        old_active = context.view_layer.objects.active
        
        # Выделяем нужные объекты
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.select_set(True)
        
        # Устанавливаем активный объект
        if objects:
            context.view_layer.objects.active = objects[0]
        
        # Настройки экспорта
        export_kwargs = {
            'filepath': fbx_path,
            'use_selection': True,
            'global_scale': 1.0,
            'axis_forward': '-Y',
            'axis_up': 'Z',
            'object_types': {'MESH', 'ARMATURE'} if has_arm else {'MESH'},
            'mesh_smooth_type': 'FACE',
            'use_mesh_modifiers': True,
            'path_mode': 'COPY',
            'embed_textures': (settings.texture_handling == 'EMBED'),
        }
        
        if settings.export_animation and has_arm:
            export_kwargs.update({
                'bake_anim': settings.bake_animation,
                'bake_anim_use_all_bones': True,
                'bake_anim_step': 1.0 / settings.animation_fps,
                'add_leaf_bones': False,
                'use_armature_deform_only': True,
            })
        
        try:
            bpy.ops.export_scene.fbx(**export_kwargs)
            self.log(f"    ✅ FBX сохранён: {fbx_path}")
        except Exception as e:
            self.log(f"    ❌ Ошибка экспорта FBX: {e}", 'ERROR')
            return False
        finally:
            # Восстанавливаем выделение
            bpy.ops.object.select_all(action='DESELECT')
            for obj in old_selection:
                obj.select_set(True)
            context.view_layer.objects.active = old_active
        
        # 3. Обработка текстур для .fbm
        if settings.copy_textures and all_textures:
            if settings.texture_handling in ['BOTH', 'FBM_ONLY']:
                copied = texture_mgr.copy_textures_to_fbm(fbx_path, all_textures)
                self.log(f"    📦 Скопировано в .fbm: {copied} текстур")
        
        # 4. Создание .node файла
        if settings.create_node and material_guid:
            file_mgr.create_node_file(
                mesh_folder, model_name, settings.mesh_path, 
                material_guid, material_name or "material"
            )
        
        return True
    
    def execute(self, context):
        settings = context.scene.unigine
        
        # Проверки
        if not settings.project_path:
            self.log("Укажите путь к проекту", 'ERROR')
            return {'CANCELLED'}
        
        if settings.export_mode == 'SINGLE' and not settings.asset_name:
            self.log("Укажите имя файла", 'ERROR')
            return {'CANCELLED'}
        
        if settings.export_selected and not context.selected_objects:
            self.log("Нет выделенных объектов", 'ERROR')
            return {'CANCELLED'}
        
        if not os.path.exists(settings.project_path):
            self.log(f"Папка не существует: {settings.project_path}", 'ERROR')
            return {'CANCELLED'}
        
        print("\n" + "="*60)
        print(f"🚀 ЭКСПОРТ В UNIGINE v2.1.0")
        print(f"📋 Режим: {settings.export_mode}")
        print("="*60)
        
        # Получаем модели для экспорта
        models = self.get_models_for_export(context, settings)
        
        if not models:
            self.log("Нет моделей для экспорта", 'ERROR')
            return {'CANCELLED'}
        
        self.log(f"\n📦 Найдено моделей: {len(models)}")
        
        # Экспортируем каждую модель
        success = 0
        failed = 0
        
        for i, (name, objects) in enumerate(models):
            self.log(f"\n[{i+1}/{len(models)}] Обработка: {name}")
            if self.export_single_model(context, settings, name, objects):
                success += 1
            else:
                failed += 1
        
        print("\n" + "="*60)
        print(f"✅ ИТОГИ ЭКСПОРТА:")
        print(f"   Успешно: {success}")
        if failed:
            print(f"   С ошибками: {failed}")
        print("="*60)
        
        self.report({'INFO'}, f"Экспорт завершён: {success} моделей")
        return {'FINISHED'}