if "bpy" in locals():
    import importlib
    importlib.reload(simu_lancestage)
    importlib.reload(prefs_lancestage)

else:
    from . import simu_lancestage
    from . import prefs_lancestage

    import bpy


bl_info = {
    'name': 'Simu_LanceStage',
    'category': 'Simutronics',
    'author': 'Jason Miller - Simutronics Corp.',
    'version': (1, 0, 0),
    'blender': (3, 2, 0),
    'location': '3D View > Tools > Simu_LanceStage Panel',
    'doc_url': '',
    'tracker_url': '',
    'description': ''
}


def register():
    simu_lancestage.register()
    prefs_lancestage.register()

    
def unregister():
    simu_lancestage.unregister()
    prefs_lancestage.unregister()



if __name__ == '__main__':
    register()