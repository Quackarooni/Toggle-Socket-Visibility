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
    "version": (1, 0, 0),
    "location": "Node Editor",
    "category": "Node",
}

from . import ui, prefs, keymaps

modules = (ui, prefs, keymaps)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in modules:
        module.unregister()


if __name__ == "__main__":
    register()
