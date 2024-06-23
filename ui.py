import bpy
from bpy.types import NodeSocketVirtual, Operator, Panel


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


def nice_name(node):
    if hasattr(node, "node_tree"):
        return f"{node.bl_label} ({node.node_tree.name})"
    else:
        return node.bl_label


class SocketDrawingBaseclass:
    @staticmethod
    def draw_sockets(layout, node, sockets):
        if len(sockets) <= 0:
            return

        layout = layout.box().row(align=True)
        col1 = layout.column(align=True)
        col1.alignment = "RIGHT"
        col1.ui_units_x = 1
        col2 = layout.column(align=True)

        for inp in sockets:
            if not inp.enabled or isinstance(inp, NodeSocketVirtual):
                continue

            if inp.label == "":
                name = inp.name
            else:
                name = inp.label

            if inp.is_linked:
                col1.label(text="", icon="DECORATE_LINKED")
            elif node.bl_idname == "NodeReroute":
                col1.label(text="", icon="LOCKED")
            else:
                col1.prop(inp, "hide", text="", invert_checkbox=True)

            col2.label(text=name)
        return

    @staticmethod
    def draw_title(layout, header_text):
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text=header_text)


class NODE_PT_TOGGLE_NODE_SOCKETS(Panel, SocketDrawingBaseclass):
    bl_label = "Socket Visibility"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "View"

    @classmethod
    def poll(cls, context):
        nodetree = fetch_active_nodetree(context)
        return nodetree is not None

    def draw(self, context):
        layout = self.layout
        node_tree = fetch_active_nodetree(context)
        node = node_tree.nodes.active

        if (node is None) or (node not in context.selected_nodes):
            layout.label(text="No node currently selected.")
            return
        else:
            inputs = node.inputs
            outputs = node.outputs

            has_inputs = len(inputs) > 0
            has_outputs = len(outputs) > 0

            layout.label(text=f"{nice_name(node)}", icon="NODE")
            box = layout.box()

            panel_orientation = fetch_user_preferences("panel_orientation")

            if panel_orientation == "AUTOMATIC":
                sublayout = box.grid_flow(even_columns=True)
            elif panel_orientation == "HORIZONTAL":
                sublayout = box.row()
            else:
                sublayout = box.column()

            if has_inputs:
                col = sublayout.column(align=True)
                col.ui_units_x = 5
                self.draw_title(col, header_text="Inputs")
                self.draw_sockets(col, node=node, sockets=inputs)

            if has_outputs:
                col = sublayout.column(align=True)
                col.ui_units_x = 5
                self.draw_title(col, header_text="Outputs")
                self.draw_sockets(col, node=node, sockets=outputs)

            if not (has_inputs or has_outputs):
                sublayout.label(text="No inputs/outputs found.", icon="PANEL_CLOSE")


class NODE_OT_CALL_SOCKET_VISIBILITY_POPUP(Operator, SocketDrawingBaseclass):
    bl_label = "Call Socket Visibility Pop-up"
    bl_idname = "node.call_socket_visibility_popup"
    bl_description = "Calls the pop-up panel for socket visibility"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        node = context.active_node
        has_selection = (node is not None) and (node.select)
        has_nodetree = fetch_active_nodetree(context) is not None

        return has_nodetree and has_selection

    def draw(self, context):
        layout = self.layout
        node = context.active_node

        layout.label(text=f"{nice_name(node)}", icon="NODE")
        box = layout.box()

        inputs, outputs = node.inputs, node.outputs
        has_inputs = len(inputs) > 0
        has_outputs = len(outputs) > 0

        sublayout = box.row()

        if has_inputs:
            col = sublayout.column(align=True)
            self.draw_title(col, header_text="Inputs")
            self.draw_sockets(col, node=node, sockets=inputs)

        if has_outputs:
            col = sublayout.column(align=True)
            self.draw_title(col, header_text="Outputs")
            self.draw_sockets(col, node=node, sockets=outputs)

        if not (has_inputs or has_outputs):
            sublayout.label(text="No inputs/outputs found.", icon="PANEL_CLOSE")

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        node = context.active_node

        if len(node.inputs) and len(node.outputs):
            no_of_columns = 1.75
        else:
            no_of_columns = 1

        width = int(fetch_user_preferences("popup_width") * no_of_columns)
        return context.window_manager.invoke_popup(self, width=width)


classes = (
    NODE_PT_TOGGLE_NODE_SOCKETS,
    NODE_OT_CALL_SOCKET_VISIBILITY_POPUP,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
