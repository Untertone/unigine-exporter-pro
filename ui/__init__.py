# ui/__init__.py
import bpy
from .panels import panels

def register():
    for panel in panels:
        bpy.utils.register_class(panel)
        print(f"  ✅ Панель: {panel.__name__}")

def unregister():
    for panel in reversed(panels):
        bpy.utils.unregister_class(panel)
        print(f"  ✅ Панель: {panel.__name__}")