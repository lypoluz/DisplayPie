bl_info = {
    "name": "DisplayPie",
    "author": "Dominik Potulski aka. lypoluz",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "3D View > Shortcut",
    "description": "Radial menu for changing an objects 'Display As' property",
    "category": "Object",
}

import bpy
from bpy.types import Menu


class OBJECT_MT_display_as_pie(Menu):
    bl_label = "DisplayPie"
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("object.set_display_as", text="Wire").mode = 'WIRE'
        pie.operator("object.set_display_as", text="Solid").mode = 'SOLID'
        pie.operator("object.set_display_as", text="Bounds").mode = 'BOUNDS'
        pie.operator("object.set_display_as", text="Textured").mode = 'TEXTURED'


class OBJECT_OT_set_display_as(bpy.types.Operator):
    bl_idname = "object.set_display_as"
    bl_label = "Set Display As"
    bl_description = "Set display type for active object."
    
    mode: bpy.props.EnumProperty(
        items=[
            ('BOUNDS', "Bounds", ""),
            ('WIRE', "Wire", ""),
            ('SOLID', "Solid", ""),
            ('TEXTURED', "Textured", ""),
        ]
    )

    def execute(self, context):
        obj = context.active_object
        if obj:
            obj.display_type = self.mode
            self.report({'INFO'}, f"Display set to {self.mode}")
        return {'FINISHED'}



classes = [
    OBJECT_OT_set_display_as,
    OBJECT_MT_display_as_pie,
]
dp_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # shortcuts
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if not kc: return
    km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'D', 'PRESS', shift=True, alt=True)
    kmi.properties.name = "OBJECT_MT_display_as_pie"
    dp_keymaps.append((km, kmi))
        

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # clear shortcuts
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    dp_keymaps.clear()


if __name__ == "__main__":
    register()
