
from multiprocessing import context
import bpy
import os
from bpy.props import IntProperty, PointerProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, FloatVectorProperty
from bpy.types import Panel, PropertyGroup, Operator
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ImportHelper
import csv
import numpy as np

#################################################################################
######################### PANEL DRAW CODE #######################################
#################################################################################

class SIMUFACEANIM_PT_main(Panel):
    bl_idname = 'SIMUFACEANIM_PT_main'
    bl_label = ''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Simu_FaceAnim'

    def draw_header(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Simu_FaceAnim",icon='EVENT_F')

    def draw(self, context):
        layout = self.layout
        propGroup = context.scene.faceanim_vars
        #Addon update and tutorial section
        box = layout.box()
        col = box.column(align=True)
        col.scale_y = 1.5
        row = col.row(align=True)   
        row.operator("simu_faceanim_update.checker",text=r"Version 1.0.0 | Check For Updates",emboss=True,depress=False,icon='FILE_REFRESH')
        

        #CSV Importer
        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        # row.label(text=r"CSV:")
        row.prop(propGroup,'csv_name')
        row.operator("simu_faceanim.fbcsv",text=r"Import",icon='FILE_FOLDER')
        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(propGroup,'retime',text= 'Fix Keframe Scaling')

        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.operator("simu_faceanim_shapekey.reset",text=r"Reset Shape Keys",icon='SHAPEKEY_DATA') 


            

    
        

#################################################################################
######################### PANEL PROPERTY CODE ###################################
################################################################################# 

class SIMU_FaceAnim_Vars(PropertyGroup):
    retime: BoolProperty(
        name='retime',
        default=True,
    )

    csv_name: StringProperty(
        name= 'CSV',
        default= '-none-',

    )
    

#################################################################################
######################### Function CODE #########################################
################################################################################# 

def csv_load(self,context,file):
    propGroup = context.scene.faceanim_vars
    ob = bpy.context.active_object
    ob_armature = ob.parent

    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        names = next(reader)
        data = np.array(list(reader))
        if propGroup.retime == True:
            data = np.delete(data, slice(None,None,2), 0)

    if ob.type == 'MESH':
        shapekeys = ob.data.shape_keys.key_blocks

        for i in range(data.shape[0]):
            if data[i][1] != '0':
                for shape in shapekeys:
                    if shape.name in names:
                        index = names.index(shape.name)
                        shape.value=float(data[i][index])
                        shape.keyframe_insert("value", frame=i)

def reset_shapekeys():
    ob = bpy.context.active_object
    if ob.type == 'MESH':
        shapekeys = ob.data.shape_keys.key_blocks
        
        for shape in shapekeys:
            shape.value = 0
            
        ob.data.shape_keys.animation_data_clear()



#################################################################################
######################### OPERATOR CODE #########################################
#################################################################################

class UPDATE_OT_faceanim_update_checker(Operator):
    """Check for Add-on Updates."""
    bl_idname = "simu_faceanim_update.checker"
    bl_label = "Check: Add-on Updates"
    bl_description = 'Check for Add-on Updates'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.script.reload()
    
        self.report({'INFO'}, "Simu_FaceAnim update check completed.")

        return{'FINISHED'}

class SIMU_OT_filebrowswer_CSV(Operator, ImportHelper):
    bl_idname = "simu_faceanim.fbcsv" 
    bl_label = "Import CSV File" 

    filter_glob: StringProperty( default='*.csv', options={'HIDDEN'} ) 

    def execute(self, context):
        file = os.path.basename(self.filepath) 
        filename, extension = os.path.splitext(file)
        propGroup = context.scene.faceanim_vars
        
        types = ('.csv')

        
        if extension in types:
            csv_load(self,context,self.filepath)
            propGroup.csv_name = filename
            
        

        return{'FINISHED'}


class SIMU_OT_reset_shapekeys(Operator):
    """Reset Shape Keys."""
    bl_idname = "simu_faceanim_shapekey.reset"
    bl_label = "Reset Shape Keys"
    bl_description = 'Reset Shape Keys'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        reset_shapekeys()

        return{'FINISHED'}





#################################################################################
######################### REGISTRATION CODE #####################################
#################################################################################   

def register():
    register_class(SIMU_FaceAnim_Vars)
    register_class(SIMUFACEANIM_PT_main)
    bpy.types.Scene.faceanim_vars = PointerProperty(type=SIMU_FaceAnim_Vars)
    register_class(UPDATE_OT_faceanim_update_checker)
    register_class(SIMU_OT_filebrowswer_CSV)
    register_class(SIMU_OT_reset_shapekeys)

    


def unregister():
    unregister_class(SIMU_FaceAnim_Vars)
    unregister_class(SIMUFACEANIM_PT_main)
    del bpy.types.Scene.faceanim_vars
    unregister_class(UPDATE_OT_faceanim_update_checker)
    unregister_class(SIMU_OT_filebrowswer_CSV)
    unregister_class(SIMU_OT_reset_shapekeys)