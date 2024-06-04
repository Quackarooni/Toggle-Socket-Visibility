import bpy
from bpy.props import EnumProperty, IntProperty, StringProperty
from bpy.types import AddonPreferences

from .ui import NODE_PT_TOGGLE_NODE_SOCKETS
from .keymaps import keymap_layout


def panel_category_callback(self, context):
    NODE_PT_TOGGLE_NODE_SOCKETS.bl_category = self.panel_location
    if hasattr(bpy.types, "NODE_PT_TOGGLE_NODE_SOCKETS"):
        bpy.utils.unregister_class(NODE_PT_TOGGLE_NODE_SOCKETS)

    bpy.utils.register_class(NODE_PT_TOGGLE_NODE_SOCKETS)


class NodeToggleInputOutputPrefs(AddonPreferences):
    bl_idname = __package__

    display_mode: EnumProperty(
        name="Display Mode",
        items=(
            ("HORIZONTAL", "Horizontal", "Display input and output entries side-by-side"),
            ("VERTICAL", "Vertical", "Display input entries above output entries"),
        ),
        default="HORIZONTAL",
        description="Determines how the inputs & outputs are going to be displayed",
    )

    panel_location: StringProperty(
        name="Panel Location",
        default="View",
        update=panel_category_callback,
        description='Specifies in what category the "Socket Visibility" panel is placed (case-sensitive)',
    )

    popup_width: IntProperty(
        name="Popup Width",
        default=250,
        min=100,
        soft_max=600,
        max=9999,
        description="Specifies the width of the pop-up panel",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "display_mode")
        layout.prop(self, "panel_location")
        layout.prop(self, "popup_width")
        keymap_layout.draw_keyboard_shorcuts(self, layout, context)


keymap_layout.register_properties(preferences=NodeToggleInputOutputPrefs)


classes = (NodeToggleInputOutputPrefs,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
