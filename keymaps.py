from .keymap_ui import KeymapItemDef, KeymapStructure, KeymapLayout
from .ui import (
    NODE_OT_CALL_SOCKET_VISIBILITY_POPUP,
)


keymap_structure = KeymapStructure(
    [
        KeymapItemDef(NODE_OT_CALL_SOCKET_VISIBILITY_POPUP.bl_idname, keymap_name="Node Editor", space_type="NODE_EDITOR"),
    ]
)


keymap_layout = KeymapLayout(layout_structure=keymap_structure)


def register():
    keymap_structure.register()


def unregister():
    keymap_structure.unregister()
