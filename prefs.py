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

    panel_orientation: EnumProperty(
        name="Panel Orientation",
        items=(
            ("AUTOMATIC", "Automatic", "Display entries horizontally/vertically depending on panel width"),
            ("HORIZONTAL", "Horizontal", "Display input and output entries side-by-side"),
            ("VERTICAL", "Vertical", "Display input entries above output entries"),
        ),
        default="AUTOMATIC",
        description="Determines how the inputs & outputs are going to be displayed",
    )

    panel_location: StringProperty(
        name="Panel Location",
        default="View",
        update=panel_category_callback,
        description='Specifies in what category the "Socket Visibility" panel is placed (case-sensitive)',
    )

    popup_width: IntProperty(
        name="Pop-up Width",
        default=175,
        min=50,
        soft_max=300,
        max=9999,
        description="Specifies the width of the pop-up panel",
    )

    def draw(self, context):
        layout = self.layout

        grid_flow = layout.grid_flow(even_columns=True)
        col1 = grid_flow.column()
        col2 = grid_flow.column()
        col_width = 11.25
        col1.ui_units_x = col_width
        col2.ui_units_x = col_width

        panel_settings = col1.box().column()
        panel_settings.label(text="Panel Settings:")
        panel_settings.separator(factor=0.25)
        panel_settings.use_property_split = True
        panel_settings.prop(self, "panel_orientation", text="Orientation")
        panel_settings.prop(self, "panel_location", text="Location")

        popup_settings = col2.box().column()
        popup_settings.use_property_split = True
        popup_settings.label(text="Pop-up Settings:")
        popup_settings.separator(factor=0.25)
        popup_settings.prop(self, "popup_width", text="Width")

        keymap_layout.draw_keyboard_shorcuts(self, layout, context)


keymap_layout.register_properties(preferences=NodeToggleInputOutputPrefs)


classes = (NodeToggleInputOutputPrefs,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
