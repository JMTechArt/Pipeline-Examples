if "bpy" in locals():
    import importlib
    importlib.reload(simu_collider)
    importlib.reload(prefs_collider)

else:
    from . import simu_collider
    from . import prefs_collider

    import bpy


bl_info = {
    'name': 'Simu_Collider',
    'category': 'Simutronics',
    'author': 'Jason Miller - Simutronics Corp.',
    'version': (1, 0, 0),
    'blender': (3, 1, 0),
    'location': '3D View > Tools > Simu_Collider Panel',
    'doc_url': '',
    'tracker_url': '',
    'description': ''
}


def register():
    simu_collider.register()
    prefs_collider.register()

    
def unregister():
    simu_collider.unregister()
    prefs_collider.unregister()



if __name__ == '__main__':
    register()