from os import unlink
from unicodedata import name
import bpy
import bpy.utils
import bmesh
import blf
import math
from mathutils import Vector
from bpy.props import IntProperty, PointerProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty
from bpy.types import Panel, PropertyGroup, Operator
from bpy.utils import register_class, unregister_class


#################################################################################
######################### PANEL DRAW CODE #######################################
#################################################################################

class SIMULOD_PT_main(Panel):
    bl_idname = 'SIMU_LOD_PT_main'
    bl_label = ''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Simu_LOD'

    def draw_header(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Simu_LOD",icon='EVENT_L')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        lod_vars = scene.lod_vars
        lod_number = lod_vars.lod_number
        make_lod_zero = lod_vars.make_lod_zero
        make_lod_children = lod_vars.make_lod_children
        make_lod_viewer = lod_vars.make_lod_viewer
        
        #Addon update and tutorial section
        box = layout.box()
        col = box.column(align=True)
        col.scale_y = 1.5
        row = col.row(align=True)   
        row.operator("simu_update.checker",text=r"Version 1.0.0 | Check For Updates",emboss=True,depress=False,icon='FILE_REFRESH')
        col = box.column(align=True)
        col.operator("wm.url_open", text=r"View Help and Info",icon='HELP').url = "https://github.com/simutronics/Galahad/blob/master/3DArtTools/Blender/scripts/addons/Simu_LOD/READ_ME.md"

        #LOD initialize section
        box = layout.box()
        col = box.column()
        row = col.row()
        if make_lod_zero == True:
            col.scale_y = 1.5
            row.alert = True
            row.enabled = True
            row.operator("simu_lod.initialize",text=r"Setup LOD0 For Selected",emboss=True,depress=False,icon='COLLECTION_NEW')
            scene.lod_vars.property_unset('lod_number')
        else:
            col.scale_y = .5
            row.alert = False
            row.enabled = False
            row.label(text=r"---LOD0 Successfully Created---",icon='CHECKMARK')

        #LOD addition and removal section 
        if make_lod_children:  
            scene.lod_vars.property_unset('view_lod_zero')
            scene.lod_vars.property_unset('view_lod_one')
            scene.lod_vars.property_unset('view_lod_two')
            scene.lod_vars.property_unset('view_lod_three')
                 
            box = layout.box()
            col = box.column()
            row = col.row()
            row.label(text=r"Add/Remove LODs: ")
            row.prop(lod_vars,'lod_number')                              
                
            if lod_number == 1:
                #1
                box = layout.box()
                col = box.column()
                row = col.row()
                row.label(text=r"LOD1 Settings:",icon='TOOL_SETTINGS')
                col = box.column()
                row = col.row()
                row.prop(lod_vars,'use_method_1')
                if lod_vars.use_method_1 == 'op1':
                    col = box.column()
                    row = col.row()
                    row.label(text=r"UV Channel Masks:")
                    col = box.column()
                    row = col.row()
                    for i in range(0,uv_channel_count('LOD Hierarchy')): 
                        row.prop(lod_vars,'use_lod1_channel'+str(i+1))
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars, 'decimate_ratio1')
                scene.lod_vars.property_unset('use_method_2')
                scene.lod_vars.property_unset('use_method_3')
                scene.lod_vars.property_unset('decimate_ratio2')
                scene.lod_vars.property_unset('decimate_ratio3')
                for i in range(0,uv_channel_count('LOD Hierarchy')): 
                    scene.lod_vars.property_unset('use_lod2_channel'+str(i+1))
                    scene.lod_vars.property_unset('use_lod3_channel'+str(i+1))
                if lod_number > 0:
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    row.label(text=r"Select LOD Parent Type:",icon='CON_CHILDOF')
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars,'parent_list')
                    col = box.column()
                    col.scale_y = 1.5
                    col.alert = True
                    row = col.row()
                    row.operator("simu_lod.children",text=r"Setup LOD Children",icon='PRESET_NEW')
                    

            if lod_number == 2:
                #1
                box = layout.box()
                col = box.column()
                row = col.row()
                row.label(text=r"LOD1 Settings:",icon='TOOL_SETTINGS')
                col = box.column()
                row = col.row()
                row.prop(lod_vars,'use_method_1')
                if lod_vars.use_method_1 == 'op1':
                    col = box.column()
                    row = col.row()
                    row.label(text=r"UV Channel Masks:")
                    col = box.column()
                    row = col.row()
                    for i in range(0,uv_channel_count('LOD Hierarchy')): 
                        row.prop(lod_vars,'use_lod1_channel'+str(i+1))
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars, 'decimate_ratio1')
                
                #2
                box = layout.box()
                col = box.column()
                row = col.row()
                row.label(text=r"LOD2 Settings:",icon='TOOL_SETTINGS')
                col = box.column()
                row = col.row()
                row.prop(lod_vars,'use_method_2')
                if lod_vars.use_method_2 == 'op1':
                    col = box.column()
                    row = col.row()
                    row.label(text=r"UV Channel Masks:")
                    col = box.column()
                    row = col.row()
                    for i in range(0,uv_channel_count('LOD Hierarchy')): 
                        row.prop(lod_vars,'use_lod2_channel'+str(i+1))
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars, 'decimate_ratio2')
                scene.lod_vars.property_unset('use_method_3')
                scene.lod_vars.property_unset('decimate_ratio3')
                for i in range(0,uv_channel_count('LOD Hierarchy')): 
                    scene.lod_vars.property_unset('use_lod3_channel'+str(i+1))

                if lod_number > 0:
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    row.label(text=r"Select LOD Parent Type:",icon='CON_CHILDOF')
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars,'parent_list')
                    col = box.column()
                    col.scale_y = 1.5
                    col.alert = True
                    row = col.row()
                    row.operator("simu_lod.children",text=r"Setup LOD Children",icon='PRESET_NEW')

            if lod_number == 3:
                #1
                box = layout.box()
                col = box.column()
                row = col.row()
                row.label(text=r"LOD1 Settings:",icon='TOOL_SETTINGS')
                col = box.column()
                row = col.row()
                row.prop(lod_vars,'use_method_1')
                if lod_vars.use_method_1 == 'op1':
                    col = box.column()
                    row = col.row()
                    row.label(text=r"UV Channel Masks:")
                    col = box.column()
                    row = col.row()
                    for i in range(0,uv_channel_count('LOD Hierarchy')): 
                        row.prop(lod_vars,'use_lod1_channel'+str(i+1))
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars, 'decimate_ratio1')
                
                #2
                box = layout.box()
                col = box.column()
                row = col.row()
                row.label(text=r"LOD2 Settings:",icon='TOOL_SETTINGS')
                col = box.column()
                row = col.row()
                row.prop(lod_vars,'use_method_2')
                if lod_vars.use_method_2 == 'op1':
                    col = box.column()
                    row = col.row()
                    row.label(text=r"UV Channel Masks:")
                    col = box.column()
                    row = col.row()
                    for i in range(uv_channel_count('LOD Hierarchy')): 
                        row.prop(lod_vars,'use_lod2_channel'+str(i+1))
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars, 'decimate_ratio2')
                
                #3
                box = layout.box()
                col = box.column()
                row = col.row()
                row.label(text=r"LOD3 Settings:",icon='TOOL_SETTINGS')
                col = box.column()
                row = col.row()
                row.prop(lod_vars,'use_method_3')
                if lod_vars.use_method_3 == 'op1':
                    col = box.column()
                    row = col.row()
                    row.label(text=r"UV Channel Masks:")
                    col = box.column()
                    row = col.row()
                    for i in range(0,uv_channel_count('LOD Hierarchy')): 
                        row.prop(lod_vars,'use_lod3_channel'+str(i+1))
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars, 'decimate_ratio3')
                
            
                if lod_number > 0:
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    row.label(text=r"Select LOD Parent Type:",icon='CON_CHILDOF')
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars,'parent_list')
                    col = box.column()
                    col.scale_y = 1.5
                    col.alert = True
                    row = col.row()
                    row.operator("simu_lod.children",text=r"Setup LOD Children",icon='PRESET_NEW')
            
        elif not make_lod_zero and not make_lod_children:
            box = layout.box()
            col = box.column()
            row = col.row()
            col.scale_y = .5
            row.alert = False
            row.enabled = False
            row.label(text=r"---LOD Children Successfully Created---",icon='CHECKMARK')

        #LOD visibility Toggles
        if make_lod_viewer:
            scene.lod_vars.property_unset('use_method_1')
            scene.lod_vars.property_unset('use_method_2')
            scene.lod_vars.property_unset('use_method_3')
            scene.lod_vars.property_unset('decimate_ratio1')
            scene.lod_vars.property_unset('decimate_ratio2')
            scene.lod_vars.property_unset('decimate_ratio3')
            for i in range(0,uv_channel_count('LOD Hierarchy')): 
                scene.lod_vars.property_unset('use_lod1_channel'+str(i+1))
                scene.lod_vars.property_unset('use_lod2_channel'+str(i+1))
                scene.lod_vars.property_unset('use_lod3_channel'+str(i+1))  

            box = layout.box()
            col = box.column()
            row = col.row()
            row.label(text=r"LOD Visibility: ")

            if lod_number == 1:
                if context.scene.lod_vars.view_lod_camera == False:
                    #0
                    col = box.column()
                    row = col.row()
                    row.operator("simu_lod.view_lod_zero",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_zero,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_zero else 'HIDE_ON')
                    row.label(text=r"LOD0")
                    #1
                    row.operator("simu_lod.view_lod_one",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_one,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_one else 'HIDE_ON')
                    row.label(text=r"LOD1")
                    #camera
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    row.label(text=r"LOD Camera Settings:")
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars,'lod1_percentage',text=r"LOD1 Percentage:")
                    # col = box.column()
                    # row = col.row()
                    # row.enabled = False
                    # row.prop(lod_vars,'unity_lod_bias',text=r"Unity LOD Bias:")
                else:
                    #0
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.operator("simu_lod.view_lod_zero",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_zero,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_zero else 'HIDE_ON')
                    row.label(text=r"LOD0")
                    #1
                    row.operator("simu_lod.view_lod_one",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_one,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_one else 'HIDE_ON')
                    row.label(text=r"LOD1")
                    #camera
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.label(text=r"LOD Camera Settings:")
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.prop(lod_vars,'lod1_percentage',text=r"LOD1 Percentage:")
                    # col = box.column()
                    # row = col.row()
                    # row.enabled = False
                    # row.prop(lod_vars,'unity_lod_bias',text=r"Unity LOD Bias:")

                col = box.column()
                col.scale_y = 1.5
                row = col.row()
                row.operator("simu_lod.view_lod_camera",text=r"Use Camera View",emboss=True,depress=context.scene.lod_vars.view_lod_camera,icon='VIEW_CAMERA')

                #Active LOD object modifier settings section
                box = layout.box()
                col = box.column()
                row = col.row()
                row.label(text=r"Active Object Modifier Settings:",icon='MODIFIER')
                if context.active_object is None:
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.label(text=r"---No Active Object---")
                else:
                    col = box.column()
                    row = col.row()
                    row.enabled = True
                    row.label(text=context.active_object.name)
                    #if modifiers
                    if len(context.active_object.modifiers) != 0:
                        #decimate modifier settings
                        if context.active_object.modifiers.get('Decimate'):
                            col = box.column()
                            row = col.row()
                            row.prop(context.active_object.modifiers["Decimate"], 'ratio',text=r"Decimate Ratio")
                            if context.mode == 'EDIT_MESH':
                                col = box.column(align=True)
                                row = col.row(align=True)
                                row.label(text=r"Decimate Mask Vertex Group:")
                                col = box.column(align=True)
                                row = col.row(align=True)
                                row.operator("object.vertex_group_assign",text=r"Assign")
                                row.operator("object.vertex_group_remove_from",text=r"Remove")
                                row = col.row(align=True)
                                row.operator("object.vertex_group_select",text=r"Select")
                                row.operator("object.vertex_group_deselect",text=r"Deselect")
                        #remesh modifier settings
                        if context.active_object.modifiers.get('Remesh') is not None:
                            col = box.column()
                            row = col.row()
                            row.prop(context.active_object.modifiers["Remesh"], 'octree_depth',text=r"Remesh Subdivisions")
                        #shrinkwrap modifier settings
                        if context.active_object.modifiers.get('Shrinkwrap') is not None:
                            col = box.column()
                            row = col.row()
                            row.prop(context.active_object.modifiers["Shrinkwrap"], 'offset',text=r"Remesh Offset")
                            col = box.column()
                            row = col.row()
                            row.operator("simu_lod.apply_modifiers",text=r"Apply Modifiers")
                    #if no modifiers
                    elif len(context.active_object.modifiers) == 0:
                        col = box.column()
                        row = col.row()
                        row.enabled = False
                        row.label(text=r"---No Modifiers Available---")
                #Remove LOD data section
                if context.scene.lod_vars.view_lod_camera == False:
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    col.scale_y = 1.5
                    row.alert = True
                    row.enabled = True
                    row.operator("simu_lod.remove",text=r"Remove All LOD Data",emboss=True,depress=False,icon='CANCEL')
                else:
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    col.scale_y = 1.5
                    row.alert = True
                    row.enabled = False
                    row.operator("simu_lod.remove",text=r"Remove All LOD Data",emboss=True,depress=False,icon='CANCEL')

            if lod_number == 2:
                if context.scene.lod_vars.view_lod_camera == False:
                    #0
                    col = box.column()
                    row = col.row()
                    row.operator("simu_lod.view_lod_zero",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_zero,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_zero else 'HIDE_ON')
                    row.label(text=r"LOD0")
                    #1
                    row.operator("simu_lod.view_lod_one",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_one,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_one else 'HIDE_ON')
                    row.label(text=r"LOD1")
                    #2
                    col = box.column()
                    row = col.row()
                    row.operator("simu_lod.view_lod_two",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_two,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_two else 'HIDE_ON')
                    row.label(text=r"LOD2")
                    #camera
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    row.label(text=r"LOD Camera Settings:")
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars,'lod1_percentage',text=r"LOD1 Percentage:")
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars,'lod2_percentage',text=r"LOD2 Percentage:")
                    # col = box.column()
                    # row = col.row()
                    # row.enabled = False
                    # row.prop(lod_vars,'unity_lod_bias',text=r"Unity LOD Bias:")
                else:
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.operator("simu_lod.view_lod_zero",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_zero,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_zero else 'HIDE_ON')
                    row.label(text=r"LOD0")
                    #1
                    row.operator("simu_lod.view_lod_one",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_one,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_one else 'HIDE_ON')
                    row.label(text=r"LOD1")
                    #2
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.operator("simu_lod.view_lod_two",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_two,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_two else 'HIDE_ON')
                    row.label(text=r"LOD2")
                    #camera
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    row.label(text=r"LOD Camera Settings:")
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.prop(lod_vars,'lod1_percentage',text=r"LOD1 Percentage:")
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.prop(lod_vars,'lod2_percentage',text=r"LOD2 Percentage:")
                    # col = box.column()
                    # row = col.row()
                    # row.enabled = False
                    # row.prop(lod_vars,'unity_lod_bias',text=r"Unity LOD Bias:")

                col = box.column()
                col.scale_y = 1.5
                row = col.row()
                row.operator("simu_lod.view_lod_camera",text=r"Use Camera View",emboss=True,depress=context.scene.lod_vars.view_lod_camera,icon='VIEW_CAMERA')
                #Active LOD object modifier settings section
                box = layout.box()
                col = box.column()
                row = col.row()
                row.label(text=r"Active Object Modifier Settings:",icon='MODIFIER')
                if context.active_object is None:
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.label(text=r"---No Active Object---")
                else:
                    col = box.column()
                    row = col.row()
                    row.enabled = True
                    row.label(text=context.active_object.name)
                    #if modifiers
                    if len(context.active_object.modifiers) != 0:
                        #decimate modifier settings
                        if context.active_object.modifiers.get('Decimate'):
                            col = box.column()
                            row = col.row()
                            row.prop(context.active_object.modifiers["Decimate"], 'ratio',text=r"Decimate Ratio")
                            if context.mode == 'EDIT_MESH':
                                col = box.column(align=True)
                                row = col.row(align=True)
                                row.label(text=r"Decimate Mask Vertex Group:")
                                col = box.column(align=True)
                                row = col.row(align=True)
                                row.operator("object.vertex_group_assign",text=r"Assign")
                                row.operator("object.vertex_group_remove_from",text=r"Remove")
                                row = col.row(align=True)
                                row.operator("object.vertex_group_select",text=r"Select")
                                row.operator("object.vertex_group_deselect",text=r"Deselect")
                        #remesh modifier settings
                        if context.active_object.modifiers.get('Remesh') is not None:
                            col = box.column()
                            row = col.row()
                            row.prop(context.active_object.modifiers["Remesh"], 'octree_depth',text=r"Remesh Subdivisions")
                        #shrinkwrap modifier settings
                        if context.active_object.modifiers.get('Shrinkwrap') is not None:
                            col = box.column()
                            row = col.row()
                            row.prop(context.active_object.modifiers["Shrinkwrap"], 'offset',text=r"Remesh Offset")
                            col = box.column()
                            row = col.row()
                            row.operator("simu_lod.apply_modifiers",text=r"Apply Modifiers")
                    #if no modifiers
                    elif len(context.active_object.modifiers) == 0:
                        col = box.column()
                        row = col.row()
                        row.enabled = False
                        row.label(text=r"---No Modifiers Available---")
                #Remove LOD data section
                if context.scene.lod_vars.view_lod_camera == False:
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    col.scale_y = 1.5
                    row.alert = True
                    row.enabled = True
                    row.operator("simu_lod.remove",text=r"Remove All LOD Data",emboss=True,depress=False,icon='CANCEL')
                else:
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    col.scale_y = 1.5
                    row.alert = True
                    row.enabled = False
                    row.operator("simu_lod.remove",text=r"Remove All LOD Data",emboss=True,depress=False,icon='CANCEL')
            
            if lod_number == 3:
                if context.scene.lod_vars.view_lod_camera == False:
                    #0
                    col = box.column()
                    row = col.row()
                    row.operator("simu_lod.view_lod_zero",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_zero,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_zero else 'HIDE_ON')
                    row.label(text=r"LOD0")
                    #1
                    row.operator("simu_lod.view_lod_one",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_one,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_one else 'HIDE_ON')
                    row.label(text=r"LOD1")
                    #2
                    col = box.column()
                    row = col.row()
                    row.operator("simu_lod.view_lod_two",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_two,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_two else 'HIDE_ON')
                    row.label(text=r"LOD2")
                    #3
                    row.operator("simu_lod.view_lod_three",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_three,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_three else 'HIDE_ON')
                    row.label(text=r"LOD3")
                    #camera
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    row.label(text=r"LOD Camera Settings:")
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars,'lod1_percentage',text=r"LOD1 Percentage:")
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars,'lod2_percentage',text=r"LOD2 Percentage:")
                    col = box.column()
                    row = col.row()
                    row.prop(lod_vars,'lod3_percentage',text=r"LOD3 Percentage:")
                    # col = box.column()
                    # row = col.row()
                    # row.enabled = False
                    # row.prop(lod_vars,'unity_lod_bias',text=r"Unity LOD Bias:")
                else:
                     #0
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.operator("simu_lod.view_lod_zero",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_zero,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_zero else 'HIDE_ON')
                    row.label(text=r"LOD0")
                    #1
                    row.operator("simu_lod.view_lod_one",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_one,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_one else 'HIDE_ON')
                    row.label(text=r"LOD1")
                    #2
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.operator("simu_lod.view_lod_two",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_two,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_two else 'HIDE_ON')
                    row.label(text=r"LOD2")
                    #3
                    row.operator("simu_lod.view_lod_three",text=r"",emboss=True,depress=context.scene.lod_vars.view_lod_three,icon='HIDE_OFF' if context.scene.lod_vars.view_lod_three else 'HIDE_ON')
                    row.label(text=r"LOD3")
                    #camera
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    row.label(text=r"LOD Camera Settings:")
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.prop(lod_vars,'lod1_percentage',text=r"LOD1 Percentage:")
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.prop(lod_vars,'lod2_percentage',text=r"LOD2 Percentage:")
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.prop(lod_vars,'lod3_percentage',text=r"LOD3 Percentage:")
                    # col = box.column()
                    # row = col.row()
                    # row.enabled = False
                    # row.prop(lod_vars,'unity_lod_bias',text=r"Unity LOD Bias:")
                col = box.column()
                col.scale_y = 1.5
                row = col.row()
                row.operator("simu_lod.view_lod_camera",text=r"Use Camera View",emboss=True,depress=context.scene.lod_vars.view_lod_camera,icon='VIEW_CAMERA')
                #Active LOD object modifier settings section
                box = layout.box()
                col = box.column()
                row = col.row()
                row.label(text=r"Active Object Modifier Settings:",icon='MODIFIER')
                if context.active_object is None:
                    col = box.column()
                    row = col.row()
                    row.enabled = False
                    row.label(text=r"---No Active Object---")
                else:
                    col = box.column()
                    row = col.row()
                    row.enabled = True
                    row.label(text=context.active_object.name)
                    #if modifiers
                    if len(context.active_object.modifiers) != 0:
                        #decimate modifier settings
                        if context.active_object.modifiers.get('Decimate'):
                            col = box.column()
                            row = col.row()
                            row.prop(context.active_object.modifiers["Decimate"], 'ratio',text=r"Decimate Ratio")
                            if context.mode == 'EDIT_MESH':
                                col = box.column(align=True)
                                row = col.row(align=True)
                                row.label(text=r"Decimate Mask Vertex Group:")
                                col = box.column(align=True)
                                row = col.row(align=True)
                                row.operator("object.vertex_group_assign",text=r"Assign")
                                row.operator("object.vertex_group_remove_from",text=r"Remove")
                                row = col.row(align=True)
                                row.operator("object.vertex_group_select",text=r"Select")
                                row.operator("object.vertex_group_deselect",text=r"Deselect")
                        #remesh modifier settings
                        if context.active_object.modifiers.get('Remesh') is not None:
                            col = box.column()
                            row = col.row()
                            row.prop(context.active_object.modifiers["Remesh"], 'octree_depth',text=r"Remesh Subdivisions")
                        #shrinkwrap modifier settings
                        if context.active_object.modifiers.get('Shrinkwrap') is not None:
                            col = box.column()
                            row = col.row()
                            row.prop(context.active_object.modifiers["Shrinkwrap"], 'offset',text=r"Remesh Offset")
                            col = box.column()
                            row = col.row()
                            row.operator("simu_lod.apply_modifiers",text=r"Apply Modifiers")
                    #if no modifiers
                    elif len(context.active_object.modifiers) == 0:
                        col = box.column()
                        row = col.row()
                        row.enabled = False
                        row.label(text=r"---No Modifiers Available---")
                #Remove LOD data section
                if context.scene.lod_vars.view_lod_camera == False:
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    col.scale_y = 1.5
                    row.alert = True
                    row.enabled = True
                    row.operator("simu_lod.remove",text=r"Remove All LOD Data",emboss=True,depress=False,icon='CANCEL')
                else:
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    col.scale_y = 1.5
                    row.alert = True
                    row.enabled = False
                    row.operator("simu_lod.remove",text=r"Remove All LOD Data",emboss=True,depress=False,icon='CANCEL')


                
                
                
            
        
#################################################################################
######################### PANEL PROPERTY CODE ###################################
################################################################################# 

class SIMU_LOD_Vars(PropertyGroup):
    make_lod_zero: BoolProperty(
        name='make_lod_zero',
        default= True,
    )

    make_lod_children: BoolProperty(
        name='make_lod_children',
        default= False,

    )

    make_lod_viewer: BoolProperty(
        name='make_lod_viewer',
        default= False,

    )

    lod_number: IntProperty(
        name='',
        description='Add or Remove Additional LODs. Minimun is 1. Maximum is 3.',
        default=1,
        subtype='UNSIGNED',
        min=1,
        max=3,
    )
    
    use_method_1: EnumProperty(
        name='Method: ',
        description='Select Method For Extra Data Manipulation.',
        items=[
            ('op1', "Decimate Modifier",""),
            ('op2',"Remesh To Low Poly",""),
        ]
    )

    use_lod1_channel1: BoolProperty(
        name='UV 1',
        default=False,

    )

    use_lod1_channel2: BoolProperty(
        name='UV 2',
        default=False,

    )

    use_lod1_channel3: BoolProperty(
        name='UV 3',
        default=False,

    )

    decimate_ratio1: FloatProperty(
        name='Decimate Ratio:',
        description='Set Decimate Modifier Ratio for LOD1.',
        default=0.5,
        subtype='UNSIGNED',
        min=0.0,
        max=1.0,

    )

    use_method_2: EnumProperty(
        name='Method: ',
        description='Select Method For Extra Data Manipulation.',
        items=[
            ('op1', "Decimate Modifier",""),
            ('op2',"Remesh To Low Poly",""),
        ]
    )

    use_lod2_channel1: BoolProperty(
        name='UV 1',
        default=False,

    )

    use_lod2_channel2: BoolProperty(
        name='UV 2',
        default=False,

    )

    use_lod2_channel3: BoolProperty(
        name='UV 3',
        default=False,

    )

    decimate_ratio2: FloatProperty(
        name='Decimate Ratio:',
        description='Set Decimate Modifier Ratio for LOD2.',
        default=0.15,
        subtype='UNSIGNED',
        min=0.0,
        max=1.0,

    )

    use_method_3: EnumProperty(
        name='Method: ',
        description='Select Method For Extra Data Manipulation.',
        items=[
            ('op1', "Decimate Modifier",""),
            ('op2',"Remesh To Low Poly",""),
        ]
    )

    use_lod3_channel1: BoolProperty(
        name='UV 1',
        default=False,

    )

    use_lod3_channel2: BoolProperty(
        name='UV 2',
        default=False,

    )

    use_lod3_channel3: BoolProperty(
        name='UV 3',
        default=False,

    )

    decimate_ratio3: FloatProperty(
        name='Decimate Ratio:',
        description='Set Decimate Modifier Ratio for LOD3.',
        default=0.05,
        subtype='UNSIGNED',
        min=0.0,
        max=1.0,

    )

    parent_list: EnumProperty(
        name='',
        description='Select how each consecutive LOD will be parented.',
        items=[('op1', "Root as Parent", ""),
                ('op2', "LOD0 as Parent",""),
                ('op3',"Consecutive LOD Parents",""),
        ],
       
    )

    view_lod_zero: BoolProperty(
        name="",
        default= True,
    )

    view_lod_one: BoolProperty(
        name="",
        default= False,
    )

    view_lod_two: BoolProperty(
        name="",
        default= False,
    )

    view_lod_three: BoolProperty(
        name="",
        default= False,
    )
    view_lod_camera: BoolProperty(
        name="",
        default= False,

    )

    lod1_percentage: IntProperty(
        min=0,
        max=100,
        default=50,

    )

    lod2_percentage: IntProperty(
        min=0,
        max=100,
        default=15,
        
    )

    lod3_percentage: IntProperty(
        min=0,
        max=100,
        default=5,
        
    )

    unity_lod_bias: IntProperty(
        min=0,
        default=1,

    )

#################################################################################
######################### FUNCTION CODE #########################################
#################################################################################

def uv_channel_count(collection_name):
    channel_count = []
    for o in bpy.data.collections.get(collection_name).all_objects:
        if o.type == 'MESH':
            channel_count.append(len(o.data.uv_layers))
    return max(channel_count)

def duplicate(obj, data=True, actions=True, collection=None, context=bpy.context):
    obj_copy = obj.copy()
    if data:
        obj_copy.data = obj_copy.data.copy()
    if actions and obj_copy.animation_data:
        obj_copy.animation_data.action = obj_copy.animation_data.action.copy()
    if not collection:
        collection = bpy.data.collections.get("LOD Hierarchy")
    collection.objects.link(obj_copy)
    # context.scene.collection.objects.unlink(obj_copy)
    return obj_copy

def lod_decimate(object,uv_channel, decimate_ratio):        
    selectedfaces = []
    
    if object.vertex_groups.get('Decimate Mask'):
        group = object.vertex_groups.get('Decimate Mask')
    else:    
        group = object.vertex_groups.new( name = 'Decimate Mask' )
    if len(object.data.uv_layers) != 1:
        if uv_channel is None:
            pass
        elif not object.data.uv_layers[uv_channel].active or object.data.uv_layers[uv_channel].active:
            object.data.uv_layers[uv_channel].active = True
            for face in object.data.polygons:
                for loop_id in face.loop_indices:
                    uv_coords = object.data.uv_layers.active.data[loop_id].uv
                    x = uv_coords.x
                    y = uv_coords.y
                    if x > 0 and x < 1:
                        if y > 0 and y < 1:                            
                            for v in face.vertices:
                                selectedfaces.append(v)                                
                                group.add(selectedfaces, 1.0, 'ADD')
    
    if not object.modifiers.get('Decimate'):    
        object.modifiers.new(name="Decimate", type='DECIMATE')
        object.modifiers["Decimate"].vertex_group = "Decimate Mask"
        object.modifiers["Decimate"].ratio = decimate_ratio
        object.modifiers["Decimate"].invert_vertex_group = True

def lod_remesh(object):
    bm = bmesh.new()
    me = object.data 
    verts = [bm.verts.new(b) for b in object.bound_box]
    bmesh.ops.convex_hull(bm, input=verts)
    bm.to_mesh(me)
    bm.clear()
    bm.free()  

    if not object.modifiers.get('Remesh'):    
        object.modifiers.new(name="Remesh", type='REMESH')
        object.modifiers["Remesh"].mode = 'SHARP'
        object.modifiers["Remesh"].octree_depth = 2
        object.modifiers["Remesh"].scale = 0.990
        object.modifiers["Remesh"].sharpness = 1.000
        object.modifiers["Remesh"].threshold = 0.990

    if not object.modifiers.get('Shrinkwrap'):    
        object.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')
        object.modifiers["Shrinkwrap"].wrap_method = 'NEAREST_SURFACEPOINT'
        object.modifiers["Shrinkwrap"].wrap_mode = 'ABOVE_SURFACE'
        object.modifiers["Shrinkwrap"].target = bpy.data.objects[object.name[:-1] + str(0)]
        object.modifiers["Shrinkwrap"].offset = 0.1


def object_bounds(object):

    obminx = object.location.x
    obminy = object.location.y
    obminz = object.location.z

    obmaxx = object.location.x
    obmaxy = object.location.y
    obmaxz = object.location.z

    for vertex in object.bound_box[:]:

        x = object.location.x + (object.scale.x * vertex[0])
        y = object.location.y + (object.scale.y * vertex[1])
        z = object.location.z + (object.scale.z * vertex[2])

        if x <= obminx:
            obminx = x
        if y <= obminy:
            obminy = y
        if z <= obminz:
            obminz = z

        if x >= obmaxx:
            obmaxx = x
        if y >= obmaxy:
            obmaxy = y
        if z >= obmaxz:
            obmaxz = z

    boundsmin = [obminx,obminy,obminz]
    boundsmax = [obmaxx,obmaxy,obmaxz] 

    bounds = [boundsmin,boundsmax]

    return bounds

all_bounds = [0,0,0]
all_center = Vector((0,0,0))

def group_bounds():
    global all_bounds
    global all_center
    minx = 0
    miny = 0
    minz = 0
    maxx = 0
    maxy = 0
    maxz = 0
    centerx = 0
    c1=0
	
    for o in bpy.data.collections.get("LOD Hierarchy").all_objects:
        if o.type == 'MESH' and "LOD0" in o.name:
            bounds = object_bounds(o)

            oxmin = bounds[0][0]
            oxmax = bounds[1][0]

            oymin = bounds[0][1]
            oymax = bounds[1][1]
        
            ozmin = bounds[0][2]
            ozmax = bounds[1][2]

            if  c1 == 0 :
                minx = oxmin
                miny = oymin
                minz = ozmin

                maxx = oxmax
                maxy = oymax
                maxz = ozmax

            # min 
            if oxmin <= minx:
                minx = oxmin

            if oymin <= miny:
                miny = oymin

            if ozmin <= minz:
                minz = ozmin
        # max 
            if oxmax >= maxx:
                maxx = oxmax

            if oymax >= maxy:
                maxy = oymax

            if ozmax >= maxz:
                maxz = ozmax

        c1+=1
        
    widhtx= maxx-minx
    widhty=maxy-miny
    widhtz=maxz-minz

    centerx = (maxx-minx)/2
    centery = (maxy-miny)/2
    centerz = (maxz-minz)/2

    group_bounds = [widhtx ,widhty ,widhtz]
    all_bounds = group_bounds
    all_center = Vector((centerx,centery,centerz))
    
    return 

def screen_space_height(context):
    global all_bounds
    global all_center

    group_bounds()

    r3d = context.space_data.region_3d
    position = r3d.view_matrix.inverted().translation

    size = max(all_bounds[0],all_bounds[1],all_bounds[2])
    distance = (all_center - position).length

    #22.62 is 60mm focal length converted to the angle of view height degrees, matches Unity for Galahad camera settings
    screen_space_height = abs(math.degrees(math.atan2(size,distance)) * context.scene.lod_vars.unity_lod_bias)/22.62
    return screen_space_height

def draw_callback_px(self, context):
    vp_horizontal_center = 0
    for a in context.screen.areas:
        if a.type == 'VIEW_3D':
            for r in a.regions:
                if r.type == 'WINDOW':
                    vp_horizontal_center = r.width/2

    lod_number = ""
    for o in bpy.data.collections.get("LOD Hierarchy").all_objects:
        if o.type == 'MESH' and not o.hide_get():
            if 'LOD0' in o.name:
                lod_number = 'LOD0'
            elif 'LOD1' in o.name:
                lod_number = 'LOD1'
            elif 'LOD2' in o.name:
                lod_number = 'LOD2'
            elif 'LOD3' in o.name:
                lod_number = 'LOD3'

    font_id = 0
    blf.color(font_id,1,1,0,1)
    blf.size(font_id, 60, 72)
    dims = blf.dimensions(font_id, lod_number)
    blf.position(font_id, vp_horizontal_center - (dims[0]/2), 30, 0)
    blf.draw(font_id, lod_number)
    
    

#################################################################################
######################### OPERATOR CODE #########################################
#################################################################################

class UPDATE_OT_update_checker(Operator):
    """Check for Add-on Updates."""
    bl_idname = "simu_update.checker"
    bl_label = "Check: Add-on Updates"
    bl_description = 'Check for Add-on Updates'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.script.reload()
    
        self.report({'INFO'}, "GALAHAD Toolkit Update Check Completed")

        return{'FINISHED'}

class LOD_OT_initialize(Operator):
    """LOD Collection Initial Setup."""
    bl_idname = "simu_lod.initialize"
    bl_label = "Setup: LODs"
    bl_description = 'LOD Collection Initial Setup'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        selected_objects = context.selected_objects

        if context.scene.lod_vars.make_lod_zero: 
        #Check for bad selections
            for o in selected_objects:
                if o.type != 'MESH':
                    self.report({'ERROR'}, "LOD Setup Failed! Incorrect selection. Select 'MESH' objects ONLY.")
                    return {'CANCELLED'}
                elif o.type == 'MESH':
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True) 
            if selected_objects == []:
                self.report({'ERROR'}, "LOD Setup Failed! Nothing selected. Select 'MESH' objects ONLY.")
                return {'CANCELLED'}

            #If proper Mesh selection exists
            #Turn on stats                
            context.space_data.overlay.show_stats = True
            context.space_data.overlay.show_cursor = False
                     

            #Generate Collection if it does not exist
            collection = bpy.data.collections.get('LOD Hierarchy')

            if not collection:    
                newColl = context.blend_data.collections.new(name= 'LOD Hierarchy')
                context.collection.children.link(newColl)

            #Link meshes to new LOD collection
            to_unlink = []
            for o in selected_objects: 
                to_unlink.append(o)
                new_collection = bpy.data.collections.get('LOD Hierarchy')
                new_collection.objects.link(o)
                

                #Check naming convention while removing old meshes to avoid naming conflicts
                # for block in bpy.data.objects:
                #     if block.users == 0:
                #         bpy.data.objects.remove(block)

                o.name = o.name + "_" + 'LOD0'
                        
                # for block in bpy.data.meshes:
                #     if block.users == 0:
                #         bpy.data.meshes.remove(block)
                            
                o.data.name = o.name
            
            #Unlink any old collections
            for o in to_unlink:
                for col in o.users_collection:
                    if col != context.scene.collection and col.name != 'LOD Hierarchy':
                        old_collection = bpy.data.collections.get(col.name)
                        old_collection.objects.unlink(o)
                    elif col == context.scene.collection:
                        context.scene.collection.objects.unlink(o)
            
            del to_unlink

            #Create root empty parent
            root = bpy.data.objects.new('root_empty', None)
            root_collection = bpy.data.collections.get('LOD Hierarchy')
            root_collection.objects.link(root)
            root.empty_display_type = 'PLAIN_AXES'
            root.location = (0,0,0)
            root.scale = (1,1,1)
            root.rotation_euler = (0,0,0)

            #Make the root empty the parent of all LOD0 meshes while maintaining the preexisting heirarchy
            for o in selected_objects:
                if not o.parent:
                    o.parent = root
                    o.matrix_parent_inverse = root.matrix_world.inverted()
            root.hide_set(True)
           
            # for o in bpy.data.collections.get("LOD Hierarchy").all_objects:
            #     o.select_set(False)
                
            context.scene.lod_vars.make_lod_zero = False       
            context.scene.lod_vars.make_lod_children = True

            self.report({'INFO'}, "LOD Setup successfully completed.")

            return{'FINISHED'}

class LOD_OT_setup_children_LODs(Operator):
    """LOD Children Setup."""
    bl_idname = "simu_lod.children"
    bl_label = "Setup: Child LODs"
    bl_description = 'LOD Children Setup'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        scene = context.scene
        lod_vars = scene.lod_vars
        lod_number = lod_vars.lod_number
        use_method_1 = lod_vars.use_method_1
        use_method_2 = lod_vars.use_method_2
        use_method_3 = lod_vars.use_method_3
        use_lod1_channel1 = lod_vars.use_lod1_channel1
        use_lod1_channel2 = lod_vars.use_lod1_channel2
        use_lod1_channel3 = lod_vars.use_lod1_channel3
        use_lod2_channel1 = lod_vars.use_lod2_channel1
        use_lod2_channel2 = lod_vars.use_lod2_channel2
        use_lod2_channel3 = lod_vars.use_lod2_channel3
        use_lod3_channel1 = lod_vars.use_lod3_channel1
        use_lod3_channel2 = lod_vars.use_lod3_channel2
        use_lod3_channel3 = lod_vars.use_lod3_channel3
        decimate_ratio1 = lod_vars.decimate_ratio1
        decimate_ratio2 = lod_vars.decimate_ratio2
        decimate_ratio3 = lod_vars.decimate_ratio3
        parent_list = lod_vars.parent_list

        selected_objects = context.selected_objects
        #Check for bad selections
        for o in selected_objects:
            if o.type != 'MESH':
                self.report({'ERROR'}, "LOD Children Setup Failed! Incorrect selection. Select 'MESH' objects ONLY.")
                return {'CANCELLED'}
            elif o.type == 'MESH':
                continue 
        if selected_objects == []:
            self.report({'ERROR'}, "LOD Children Setup Failed! Nothing selected. Select 'MESH' objects ONLY.")
            return {'CANCELLED'}

        
        #Duplicate each LOD0 mesh by how many LOD children levels were created and rename them with the proper LOD tag
        for o in selected_objects:
            
            for i in range(lod_number):
                if o.type is not 'EMPTY':
            
                    obj_copy = duplicate(
                            obj=o,
                            data=True,
                            actions=True,      
                    )

                    obj_copy.name = obj_copy.name[:-5] + str(i+1)
                    obj_copy.data.name = obj_copy.name
                    print("loop number " + str(i+1))
                    o.select_set(False)
                    obj_copy.select_set(False)

        #Parenting Setup
        for o in bpy.data.collections.get("LOD Hierarchy").all_objects:
            for i in range(lod_number):
                if ("LOD" + str(i+1)) in o.name:
                    if parent_list == 'op1': #Root as Parent
                        if o.parent is not bpy.data.objects.get('root_empty'):
                            parent = bpy.data.objects.get(o.parent.name[:-1] + str(i+1))
                            if parent:
                                o.parent = parent
                                o.matrix_parent_inverse = parent.matrix_world.inverted()
                            
                    elif parent_list == 'op2': #LOD0 as Parent
                        parent = bpy.data.objects.get(o.name[:-1] + str(0))
                        if parent:
                            o.parent = parent
                            o.matrix_parent_inverse = parent.matrix_world.inverted()
                    elif parent_list == 'op3': #Consecutive LOD Parents
                        parent = bpy.data.objects.get(o.name[:-1] + str(i))
                        if parent:
                            o.parent = parent
                            o.matrix_parent_inverse = parent.matrix_world.inverted()

        #Setup Decimate Modifiers
        for o in bpy.data.collections.get('LOD Hierarchy').all_objects:
            o.select_set(False)
            if o.type == 'MESH':
                if 'LOD1' in o.name:
                    if use_method_1 == 'op1':
                        if not use_lod1_channel1 and not use_lod1_channel2 and not use_lod1_channel3:
                            lod_decimate(o,None, decimate_ratio1)
                        if use_lod1_channel1:
                            lod_decimate(o,0,decimate_ratio1)
                        if use_lod1_channel2:
                            lod_decimate(o,1,decimate_ratio1)
                        if use_lod1_channel3:
                            lod_decimate(o,2,decimate_ratio1)

        for o in bpy.data.collections.get('LOD Hierarchy').all_objects:
            o.select_set(False)
            if o.type == 'MESH':
                if 'LOD2' in o.name:
                    if use_method_2 == 'op1':
                        if not use_lod2_channel1 and not use_lod2_channel2 and not use_lod2_channel3:
                            lod_decimate(o,None, decimate_ratio2)    
                        if use_lod2_channel1:
                            lod_decimate(o,0, decimate_ratio= decimate_ratio2)
                        if use_lod2_channel2:
                            lod_decimate(o,1, decimate_ratio= decimate_ratio2)
                        if use_lod2_channel3:
                            lod_decimate(o,2, decimate_ratio= decimate_ratio2)
        
        for o in bpy.data.collections.get('LOD Hierarchy').all_objects:
            o.select_set(False)
            if o.type == 'MESH':
                if 'LOD3' in o.name:
                    if use_method_3 == 'op1':
                        if not use_lod3_channel1 and not use_lod3_channel2 and not use_lod3_channel3:
                            lod_decimate(o,None, decimate_ratio3)
                        if use_lod3_channel1:
                            lod_decimate(o,0, decimate_ratio= decimate_ratio3)
                        if use_lod3_channel2:
                            lod_decimate(o,1, decimate_ratio= decimate_ratio3)
                        if use_lod3_channel3:
                            lod_decimate(o,2, decimate_ratio= decimate_ratio3)

        o.select_set(False)
        context.view_layer.update()
        #Remesh Setup
        for o in bpy.data.collections.get('LOD Hierarchy').all_objects:
            if o.type == 'MESH':
                if 'LOD1' in o.name:
                    if use_method_1 == 'op2':
                        lod_remesh(o)
                if 'LOD2' in o.name:
                    if use_method_2 == 'op2':
                        lod_remesh(o)
                if 'LOD3' in o.name:
                    if use_method_3 == 'op2':
                        lod_remesh(o)            

        #initial visibility state setup
        context.scene.lod_vars.make_lod_children = False
        context.scene.lod_vars.make_lod_viewer = True

        for o in bpy.data.collections.get("LOD Hierarchy").all_objects:
            if "LOD0" in o.name:
                o.hide_set(False)
            else:
                o.hide_set(True)

        self.report({'INFO'}, "LOD Children Setup successfully completed.")

        return{'FINISHED'}

class LOD_OT_view_lod_zero(Operator):
    """View LOD Zero."""
    bl_idname = "simu_lod.view_lod_zero"
    bl_label = "View: LOD0"
    bl_description = 'LOD0 View Toggle'
    bl_options = {'UNDO_GROUPED'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        context.scene.lod_vars.view_lod_zero = not context.scene.lod_vars.view_lod_zero

        for o in bpy.data.collections.get("LOD Hierarchy").all_objects:
            if context.scene.lod_vars.view_lod_zero == True:
                if "LOD0" in o.name:
                    o.hide_set(False)
                    self.report({'INFO'}, "LOD0 View Enabled")
            else:
                if "LOD0" in o.name:
                    o.hide_set(True)
                    self.report({'INFO'}, "LOD0 View Disabled")

        return{'FINISHED'}

class LOD_OT_view_lod_one(Operator):
    """View LOD One."""
    bl_idname = "simu_lod.view_lod_one"
    bl_label = "View: LOD1"
    bl_description = 'LOD1 View Toggle'
    bl_options = {'UNDO_GROUPED'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        context.scene.lod_vars.view_lod_one = not context.scene.lod_vars.view_lod_one

        for o in bpy.data.collections.get("LOD Hierarchy").all_objects:
            if context.scene.lod_vars.view_lod_one == True:
                if "LOD1" in o.name:
                    o.hide_set(False)
                    self.report({'INFO'}, "LOD1 View Enabled")
            else:
                if "LOD1" in o.name:
                    o.hide_set(True)
                    self.report({'INFO'}, "LOD1 View Disabled")

        return{'FINISHED'}

class LOD_OT_view_lod_two(Operator):
    """View LOD Two."""
    bl_idname = "simu_lod.view_lod_two"
    bl_label = "View: LOD2"
    bl_description = 'LOD2 View Toggle'
    bl_options = {'UNDO_GROUPED'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        context.scene.lod_vars.view_lod_two = not context.scene.lod_vars.view_lod_two

        for o in bpy.data.collections.get("LOD Hierarchy").all_objects:
            if context.scene.lod_vars.view_lod_two == True:
                if "LOD2" in o.name:
                    o.hide_set(False)
                    self.report({'INFO'}, "LOD2 View Enabled")
            else:
                if "LOD2" in o.name:
                    o.hide_set(True)
                    self.report({'INFO'}, "LOD2 View Disabled")

        return{'FINISHED'}

class LOD_OT_view_lod_three(Operator):
    """View LOD Three."""
    bl_idname = "simu_lod.view_lod_three"
    bl_label = "View: LOD3"
    bl_description = 'LOD3 View Toggle'
    bl_options = {'UNDO_GROUPED'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        context.scene.lod_vars.view_lod_three = not context.scene.lod_vars.view_lod_three

        for o in bpy.data.collections.get("LOD Hierarchy").all_objects:
            if context.scene.lod_vars.view_lod_three == True:
                if "LOD3" in o.name:
                    o.hide_set(False)
                    self.report({'INFO'}, "LOD3 View Enabled")
            else:
                if "LOD3" in o.name:
                    o.hide_set(True)
                    self.report({'INFO'}, "LOD3 View Disabled")

        return{'FINISHED'}

class LOD_OT_view_lod_camera(Operator):
    """View LOD Camera."""
    bl_idname = "simu_lod.view_lod_camera"
    bl_label = "View: LOD Camera"
    bl_description = 'LOD Camera View Toggle'
    bl_options = {'UNDO_GROUPED'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'
    
    _timer = None

    

        
    
    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')

    def execute(self, context):
        
        context.scene.lod_vars.view_lod_camera = not context.scene.lod_vars.view_lod_camera
        if context.scene.lod_vars.view_lod_camera == True:
            args = (self,context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
            wm = context.window_manager
            self._timer = wm.event_timer_add(0.1, window=context.window)
            wm.modal_handler_add(self)
            self.report({'INFO'}, "Now Using Camera View Mode")

            return {'RUNNING_MODAL'}
        else: 
            return{'CANCELLED'}
    
    def modal(self, context, event):
        context.area.tag_redraw()    

        if context.scene.lod_vars.view_lod_camera == False:
            self.cancel(context)

            for o in bpy.data.collections.get("LOD Hierarchy").all_objects:
                if o.type == 'MESH' and "LOD0" in o.name:
                    o.hide_set(False)
                else:
                    o.hide_set(True)
            context.scene.lod_vars.view_lod_zero = True
            context.scene.lod_vars.view_lod_one = False
            context.scene.lod_vars.view_lod_two = False
            context.scene.lod_vars.view_lod_three = False
            self.report({'INFO'}, "No Longer Using Camera View Mode")
            return{'CANCELLED'}
        
        if event.type == 'TIMER':
            height = screen_space_height(context)
            lod1_val = context.scene.lod_vars.lod1_percentage/100
            lod2_val = context.scene.lod_vars.lod2_percentage/100
            lod3_val = context.scene.lod_vars.lod3_percentage/100

            for o in bpy.data.collections.get("LOD Hierarchy").all_objects:
                if context.scene.lod_vars.lod_number == 1:
                    if height > lod1_val:
                        if o.type == 'MESH' and "LOD0" in o.name:
                            o.hide_set(False)
                        else:
                            o.hide_set(True)
                    elif height < lod1_val:
                        if o.type == 'MESH' and "LOD1" in o.name:
                            o.hide_set(False)
                        else:
                            o.hide_set(True)
                    
                if context.scene.lod_vars.lod_number == 2:
                    if height > lod1_val:
                        if o.type == 'MESH' and "LOD0" in o.name:
                            o.hide_set(False)
                        else:
                            o.hide_set(True)
                    elif height < lod1_val and height > lod2_val:
                        if o.type == 'MESH' and "LOD1" in o.name:
                            o.hide_set(False)
                        else:
                            o.hide_set(True)
                    elif height < lod2_val:
                        if o.type == 'MESH' and "LOD2" in o.name:
                            o.hide_set(False)
                        else:
                            o.hide_set(True)
                    
                if context.scene.lod_vars.lod_number == 3:
                    if height > lod1_val:
                        if o.type == 'MESH' and "LOD0" in o.name:
                            o.hide_set(False)
                        else:
                            o.hide_set(True)
                    elif height < lod1_val and height > lod2_val:
                        if o.type == 'MESH' and "LOD1" in o.name:
                            o.hide_set(False)
                        else:
                            o.hide_set(True)
                    elif height < lod2_val and height > lod3_val:
                        if o.type == 'MESH' and "LOD2" in o.name:
                            o.hide_set(False)
                        else:
                            o.hide_set(True)
                    elif height < lod3_val:
                        if o.type == 'MESH' and "LOD3" in o.name:
                            o.hide_set(False)
                        else:
                            o.hide_set(True)
            
        
        return{'PASS_THROUGH'} 


    

class LOD_OT_apply_modifiers(Operator):
    """Destroy LOD Setup"""
    bl_idname = "simu_lod.apply_modifiers"
    bl_label = "Apply: Modifiers"
    bl_description = 'Apply Modifieres to Selected LOD Object'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.object.convert(target='MESH')
        self.report({'INFO'}, "All Modifiers have been applied")

        return{'FINISHED'}


class LOD_OT_remove_lods(Operator):
    """Remove LOD Setup"""
    bl_idname = "simu_lod.remove"
    bl_label = "Remove: LODs"
    bl_description = 'Remove all LOD data'
    bl_options = {'UNDO_GROUPED'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        objects = bpy.data.collections.get("LOD Hierarchy").all_objects
        for o in objects:
            o.hide_set(False)
            for collection in list(o.users_collection):
                if "LOD0" not in o.name:
                    collection.objects.unlink(o)
            if o.users == 0:
                bpy.data.objects.remove(o)

        del objects

        lod_zeroes = bpy.data.collections.get("LOD Hierarchy").all_objects
        to_unlink = []

        for o in lod_zeroes:
            o.name = o.name[:-5]
            o.data.name = o.name
            context.scene.collection.objects.link(o)
            to_unlink.append(o)

        del lod_zeroes

        for o in to_unlink:
            collection = bpy.data.collections.get("LOD Hierarchy")
            collection.objects.unlink(o)
        
        del to_unlink

        for coll in list(context.scene.collection.children):
            if "LOD Hierarchy" in coll.name:
                bpy.data.collections.remove(coll)
        
        del coll

        for block in bpy.data.objects:
            if block.users == 0:
                   bpy.data.objects.remove(block)

        for block in bpy.data.meshes:
            if block.users == 0:
                   bpy.data.meshes.remove(block)


        context.scene.lod_vars.make_lod_zero = True
        context.scene.lod_vars.make_lod_viewer = False


        self.report({'INFO'}, "LOD Data Has Been Removed")
        
        return{'FINISHED'}

#################################################################################
######################### REGISTRATION CODE #####################################
#################################################################################    

def register():
    register_class(SIMU_LOD_Vars)
    register_class(SIMULOD_PT_main)
    bpy.types.Scene.lod_vars = PointerProperty(type=SIMU_LOD_Vars)
    register_class(UPDATE_OT_update_checker)
    register_class(LOD_OT_initialize)
    register_class(LOD_OT_setup_children_LODs)
    register_class(LOD_OT_view_lod_zero)
    register_class(LOD_OT_view_lod_one)
    register_class(LOD_OT_view_lod_two)
    register_class(LOD_OT_view_lod_three)
    register_class(LOD_OT_view_lod_camera)
    register_class(LOD_OT_apply_modifiers)
    register_class(LOD_OT_remove_lods)

def unregister():
    unregister_class(SIMU_LOD_Vars)
    unregister_class(SIMULOD_PT_main)
    del bpy.types.Scene.lod_vars
    unregister_class(UPDATE_OT_update_checker)
    unregister_class(LOD_OT_initialize)
    unregister_class(LOD_OT_setup_children_LODs)
    unregister_class(LOD_OT_view_lod_zero)
    unregister_class(LOD_OT_view_lod_one)
    unregister_class(LOD_OT_view_lod_two)
    unregister_class(LOD_OT_view_lod_three)
    unregister_class(LOD_OT_view_lod_camera)
    unregister_class(LOD_OT_apply_modifiers)
    unregister_class(LOD_OT_remove_lods)