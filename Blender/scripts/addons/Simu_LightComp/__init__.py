if "bpy" in locals():
    import importlib
    importlib.reload(simu_lightcomp)
    importlib.reload(prefs_lightcomp)

else:
    from . import simu_lightcomp
    from . import prefs_lightcomp

    import bpy


bl_info = {
    'name': 'Simu_LightComp',
    'category': 'Simutronics',
    'author': 'Jason Miller - Simutronics Corp.',
    'version': (1, 0, 0),
    'blender': (3, 2, 0),
    'location': '3D View > Tools > Simu_LightComp Panel',
    'doc_url': '',
    'tracker_url': '',
    'description': ''
}


def register():
    simu_lightcomp.register()
    prefs_lightcomp.register()

    
def unregister():
    simu_lightcomp.unregister()
    prefs_lightcomp.unregister()



if __name__ == '__main__':
    register()