# -*- coding: utf-8 -*-

# ======================================
# ИНФОРМАЦИЯ О ПЛАГИНЕ
# ======================================
bl_info = {
    "name": "Unigine Exporter Pro",
    "author": "Alexander Filatov",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Unigine",
    "description": "Пакетный экспорт моделей, материалов и анимаций в Unigine",
    "category": "Import-Export",
}

import bpy
import importlib
import sys

# ======================================
# МОДУЛИ ДЛЯ ПЕРЕЗАГРУЗКИ (ДЛЯ РАЗРАБОТКИ)
# ======================================
modules = [
    "properties",
    "utils.material_utils",
    "utils.texture_utils",
    "utils.animation_utils",
    "utils.file_utils",
    "operators.export_operator",
    "operators.test_operator",
    "ui.panels",
]

def reload_modules():
    """Перезагрузить все модули (для разработки)"""
    for module_name in modules:
        full_name = f"{__package__}.{module_name}"
        if full_name in sys.modules:
            importlib.reload(sys.modules[full_name])
            print(f"  🔄 Перезагружен: {module_name}")

# ======================================
# ИМПОРТ МОДУЛЕЙ
# ======================================
from . import properties
from . import utils
from . import operators
from . import ui

# ======================================
# РЕГИСТРАЦИЯ
# ======================================
def register():
    """Регистрация всех модулей"""
    print("\n" + "="*60)
    print("📦 РЕГИСТРАЦИЯ UNIGINE EXPORTER PRO v1.0.0")
    print("="*60)
    
    # Регистрируем в правильном порядке
    properties.register()
    utils.register()
    operators.register()
    ui.register()
    
    print("\n" + "="*60)
    print("✅ Unigine Exporter Pro v1.0.0 зарегистрирован")
    print("="*60 + "\n")

def unregister():
    """Отмена регистрации всех модулей"""
    print("\n" + "="*60)
    print("📦 ОТКЛЮЧЕНИЕ UNIGINE EXPORTER PRO")
    print("="*60)
    
    ui.unregister()
    operators.unregister()
    utils.unregister()
    properties.unregister()
    
    print("\n" + "="*60)
    print("❌ Unigine Exporter Pro отключен")
    print("="*60 + "\n")

if __name__ == "__main__":
    register()
