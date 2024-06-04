# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Toggle Socket Visibility",
    "author": "Quackers",
    "description": "Adds a panel for configuring the visibility of a node's inputs and/or outputs",
    "blender": (3, 0, 0),
    "version": (0, 0, 1),
    "location": "Node Editor",
    "category": "Node",
}

import bpy
from bpy.props import EnumProperty, IntProperty
from bpy.types import AddonPreferences, NodeSocketVirtual, Operator, Panel


def fetch_user_preferences(attr_id=None):
    prefs = bpy.context.preferences.addons[__package__].preferences

    if attr_id is None:
        return prefs
    else:
        return getattr(prefs, attr_id)


def fetch_active_nodetree(context):
    edit_tree = context.space_data.edit_tree
    node_tree = context.space_data.node_tree

    if edit_tree is not None:
        return edit_tree
    else:
        return node_tree


class SocketDrawingBaseclass:
    @staticmethod
    def draw_sockets(layout, sockets):
        if len(sockets) <= 0:
            return

        layout = layout.box().column(align=True)

        for inp in sockets:
            if not inp.enabled or isinstance(inp, NodeSocketVirtual):
                continue

            if inp.label == "":
                name = inp.name
            else:
                name = inp.label

            row = layout.row(align=True)

            if not inp.is_linked:
                row.prop(inp, "hide", text="", invert_checkbox=True)
            else:
                row.label(text="", icon="DECORATE_LINKED")

            row.label(text=name)
        return

    @staticmethod
    def draw_title(layout, header_text):
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text=header_text)

    def draw(self, context):
        layout = self.layout
        node_tree = fetch_active_nodetree(context)
        node = node_tree.nodes.active

        if (node is None) or (node not in context.selected_nodes):
            layout.label(text="No node currently selected.")
            return
        else:
            label = node.bl_label

            is_nodegroup = hasattr(node, "node_tree")
            if is_nodegroup:
                label += f" ({node.node_tree.name})"

            inputs = node.inputs
            outputs = node.outputs

            has_inputs = len(inputs) > 0
            has_outputs = len(outputs) > 0

            layout.label(text=f"Active Node: {label}")
            box = layout.box()

            display_horizontal = fetch_user_preferences("display_mode") == "HORIZONTAL"

            if display_horizontal:
                sublayout = box.row()
            else:
                sublayout = box.column()

            if has_inputs:
                col = sublayout.column(align=True)
                self.draw_title(col, header_text="Inputs")
                self.draw_sockets(col, sockets=inputs)

            if has_outputs:
                col = sublayout.column(align=True)
                self.draw_title(col, header_text="Outputs")
                self.draw_sockets(col, sockets=outputs)

            if not (has_inputs or has_outputs):
                sublayout.label(text="No inputs/outputs found.", icon="PANEL_CLOSE")


class NODE_PT_TOGGLE_NODE_SOCKETS(Panel, SocketDrawingBaseclass):
    bl_label = "Toggle Socket Visibility"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "View"

    @classmethod
    def poll(cls, context):
        nodetree = fetch_active_nodetree(context)
        return nodetree is not None


class NODE_OT_TOGGLE_NODE_SOCKETS_POPUP(Operator, SocketDrawingBaseclass):
    bl_label = "Socket Visibility"
    bl_idname = "node.toggle_socket_visibility"
    bl_description = "Renames all selected nodes according to specified label"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        node = context.active_node
        has_selection = (node is not None) and (node.select)
        has_nodetree = fetch_active_nodetree(context) is not None

        return has_nodetree and has_selection

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        width = fetch_user_preferences("popup_width")
        return context.window_manager.invoke_popup(self, width=width)


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

    popup_width: IntProperty(name="Popup Width", default=250, min=100, soft_max=600, max=9999)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "display_mode")
        layout.prop(self, "popup_width")


classes = (
    NODE_PT_TOGGLE_NODE_SOCKETS,
    NODE_OT_TOGGLE_NODE_SOCKETS_POPUP,
    NodeToggleInputOutputPrefs,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
