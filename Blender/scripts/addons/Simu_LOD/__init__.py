if "bpy" in locals():
    import importlib
    importlib.reload(simu_lod)
    importlib.reload(prefs_lod)

else:
    from . import simu_lod
    from . import prefs_lod

    import bpy


bl_info = {
    'name': 'Simu_LOD',
    'category': 'Simutronics',
    'author': 'Jason Miller - Simutronics Corp.',
    'version': (1, 0, 0),
    'blender': (3, 1, 0),
    'location': '3D View > Tools > Simu_LOD Panel',
    'doc_url': '',
    'tracker_url': '',
    'description': ''
}


def register():
    simu_lod.register()
    prefs_lod.register()

    
def unregister():
    simu_lod.unregister()
    prefs_lod.unregister()



if __name__ == '__main__':
    register()
