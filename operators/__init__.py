# operators/__init__.py
import bpy
from .export_operator import UNIGINE_OT_export
from .test_operator import UNIGINE_OT_test

classes = [
    UNIGINE_OT_export,
    UNIGINE_OT_test,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        print(f"  ✅ Оператор: {cls.__name__}")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        print(f"  ✅ Оператор: {cls.__name__}")