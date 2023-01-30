if "bpy" in locals():
    import importlib
    importlib.reload(simu_faceanim)
    importlib.reload(prefs_faceanim)

else:
    from . import simu_faceanim
    from . import prefs_faceanim

    import bpy


bl_info = {
    'name': 'Simu_FaceAnim',
    'category': 'Simutronics',
    'author': 'Jason Miller - Simutronics Corp.',
    'version': (1, 0, 0),
    'blender': (3, 2, 0),
    'location': '3D View > Tools > Simu_FaceAnim Panel',
    'doc_url': '',
    'tracker_url': '',
    'description': ''
}


def register():
    simu_faceanim.register()
    prefs_faceanim.register()

    
def unregister():
    simu_faceanim.unregister()
    prefs_faceanim.unregister()



if __name__ == '__main__':
    register()