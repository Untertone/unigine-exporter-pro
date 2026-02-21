# properties/__init__.py
import bpy
from .properties import UnigineExportProps

def register():
    # Регистрируем класс через bpy.utils.register_class
    bpy.utils.register_class(UnigineExportProps)
    # Добавляем свойство к сцене
    bpy.types.Scene.unigine = bpy.props.PointerProperty(type=UnigineExportProps)
    print("  ✅ Свойства зарегистрированы")

def unregister():
    # Удаляем свойство из сцены
    if hasattr(bpy.types.Scene, 'unigine'):
        del bpy.types.Scene.unigine
    # Отменяем регистрацию класса
    bpy.utils.unregister_class(UnigineExportProps)
    print("  ✅ Свойства отменены")