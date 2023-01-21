import bpy
from bpy.types import AddonPreferences

from bpy.utils import register_class, unregister_class


class SIMU_lancestage_prefs(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align = True)

        col.operator("wm.url_open", text="Help Information", icon='HELP').url = "https://github.com/simutronics/Galahad/blob/master/3DArtTools/Blender/scripts/addons/Simu_Collider/READ_ME.md"
        col.operator("wm.url_open", text="Change Log Information", icon='HELP').url = "https://github.com/simutronics/Galahad/blob/master/3DArtTools/Blender/scripts/addons/Simu_Collider/CHANGE_LOG.md"



def register():
    register_class(SIMU_lancestage_prefs)


def unregister():
    unregister_class(SIMU_lancestage_prefs)