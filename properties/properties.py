# properties/properties.py
import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    BoolProperty, StringProperty, FloatProperty,
    EnumProperty, IntProperty
)

class UnigineExportProps(PropertyGroup):
    """Свойства экспорта в Unigine"""
    
    # ----- Базовые настройки -----
    project_path: StringProperty(
        name="Project Path",
        description="Корневая папка проекта Unigine",
        subtype='DIR_PATH',
        default=""
    )
    
    # ----- Настройки путей -----
    mesh_path: StringProperty(
        name="Mesh Folder",
        description="Папка для мешей внутри data",
        default="meshes"
    )
    
    texture_path: StringProperty(
        name="Texture Folder",
        description="Папка для текстур внутри data",
        default="textures"
    )
    
    # ----- Настройки материалов -----
    export_materials: BoolProperty(
        name="Export Materials",
        description="Экспортировать материалы",
        default=True
    )
    
    copy_textures: BoolProperty(
        name="Copy Textures",
        description="Копировать текстуры в проект",
        default=True
    )
    
    texture_handling: EnumProperty(
        name="Texture Handling",
        description="Как обрабатывать текстуры",
        items=[
            ('BOTH', "Copy to both folders", "Копировать и в .fbm и в textures"),
            ('FBM_ONLY', "Copy to .fbm only", "Только в .fbm (для Unigine)"),
            ('TEXTURES_ONLY', "Copy to textures only", "Только в textures (для .mat)"),
            ('EMBED', "Embed in FBX", "Встроить текстуры в FBX"),
        ],
        default='BOTH'
    )
    
    # ----- Настройки анимации -----
    export_animation: BoolProperty(
        name="Export Animation",
        description="Экспортировать анимацию",
        default=True
    )
    
    bake_animation: BoolProperty(
        name="Bake Animation",
        description="Запекать анимацию",
        default=True
    )
    
    animation_fps: FloatProperty(
        name="FPS",
        description="Частота кадров анимации",
        default=24.0,
        min=1.0,
        max=120.0
    )
    
    # ----- Настройки пакетного экспорта -----
    export_mode: EnumProperty(
        name="Export Mode",
        description="Режим экспорта",
        items=[
            ('SINGLE', "Single Model", "Экспортировать одну модель"),
            ('BATCH', "Batch Export", "Экспортировать по объектам"),
            ('COLLECTION', "By Collection", "Экспортировать по коллекциям"),
        ],
        default='SINGLE'
    )
    
    asset_name: StringProperty(
        name="Asset Name",
        description="Имя файла без расширения",
        default="MyModel"
    )
    
    batch_prefix: StringProperty(
        name="Name Prefix",
        description="Префикс для имен файлов",
        default=""
    )
    
    batch_suffix: StringProperty(
        name="Name Suffix",
        description="Суффикс для имен файлов",
        default=""
    )
    
    auto_number: BoolProperty(
        name="Auto Number",
        description="Автоматически добавлять номер",
        default=True
    )
    
    number_padding: IntProperty(
        name="Number Padding",
        description="Количество цифр в номере",
        default=3,
        min=1,
        max=5
    )
    
    # ----- Общие опции -----
    export_selected: BoolProperty(
        name="Export Selected Only",
        description="Экспортировать только выделенные объекты",
        default=True
    )
    
    create_node: BoolProperty(
        name="Create .node File",
        description="Создать .node файл для модели",
        default=True
    )
    
    verbose: BoolProperty(
        name="Verbose Output",
        description="Показывать подробный вывод в консоли",
        default=False
    )