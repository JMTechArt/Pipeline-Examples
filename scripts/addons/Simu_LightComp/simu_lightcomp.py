
from multiprocessing import context
import bpy
import os
from bpy.props import IntProperty, PointerProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, FloatVectorProperty
from bpy.types import Panel, PropertyGroup, Operator
from bpy.utils import register_class, unregister_class




#################################################################################
######################### PANEL DRAW CODE #######################################
#################################################################################

class SIMULIGHTCOMP_PT_main(Panel):
    bl_idname = 'SIMULIGHTCOMP_PT_main'
    bl_label = ''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Simu_LightComp'

    def draw_header(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Simu_LightComp",icon='LIGHT')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        view = context.space_data
       
        #Addon update and tutorial section
        box = layout.box()
        col = box.column(align=True)
        col.scale_y = 1.5
        row = col.row(align=True)   
        row.operator("simu_lightcomp_update.checker",text=r"Version 1.0.0 | Check For Updates",emboss=True,depress=False,icon='FILE_REFRESH')
        
        #Texture Utilities
        box = layout.box()
        col = box.column()
        col.label(text='Texture Utilities',icon='TEXTURE_DATA')
        col.operator("simu_lightcomp_path.fix",text='Fix Missing Textures(textures folder in Asset dir)')
        
        #Viewport Controls
        box = layout.box()
        col = box.column()
        col.label(text='Viewport Controls',icon='VIEW3D')
        col.operator("simu_lightcomp_view.camera",text='Toggle Camera View')
        col = box.column(align=True, heading="Use as Camera")
        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(view, "use_local_camera", text="")
        sub = sub.row(align=True)
        sub.enabled = view.use_local_camera
        sub.prop(view, "camera", text="")
        col = box.column(align=True,heading='Lock Camera')
        col.prop(view, "lock_camera", text="")
        col.operator("simu_lightcomp_navigation.walk",text='Toggle Walk Navigation')

class SIMULIGHTCOMP_PT_renderlayer(Panel):
    bl_idname = 'SIMULIGHTCOMP_PT_renderlayer'
    bl_label = ''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Simu_LightComp'

    def draw_header(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Layer Setup",icon='RENDERLAYERS')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        window = context.window
        scene = window.scene
        view_layer = context.view_layer        
        
        #View Layer creation/selection
        col = layout.column(align=True)
        row = col.row(align=True)  
        row.template_search(
            window, "view_layer",
            scene, "view_layers",
            new="scene.view_layer_add",
            unlink="scene.view_layer_remove")
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("simu_lightcomp_collection.create",text=r"Create Layer Collection",icon='COLLECTION_NEW')  
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("simu_lightcomp_collection.exclude",text=r"Exclude All Not in Layer Collection",icon='CANCEL') 
        

        #Current Layer Light Group Settings
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text='Current Layer Light Groups:')
        row = layout.row()
        col = row.column()
        col.template_list("UI_UL_list", "lightgroups", view_layer,
                        "lightgroups", view_layer, "active_lightgroup_index", rows=3)
        col = row.column()
        sub = col.column(align=True)
        sub.operator("scene.view_layer_add_lightgroup", icon='ADD', text="")
        sub.operator("scene.view_layer_remove_lightgroup", icon='REMOVE', text="")
        col = layout.column(align=True)
        
        col.operator("scene.view_layer_add_used_lightgroups", icon='ADD')
        col.operator("scene.view_layer_remove_unused_lightgroups", icon='REMOVE')

class SIMULIGHTCOMP_PT_objectsettings(Panel):
    bl_idname = 'SIMULIGHTCOMP_PT_objectsettings'
    bl_label = ''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Simu_LightComp'

    def draw_header(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Object Settings",icon='SETTINGS')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        view_layer = context.view_layer
        scene = context.scene        
        
        tool_settings = context.tool_settings        

        try:
            obj = view_layer.objects.active

            if obj == view_layer.objects.active:
                #Light Settings
                box = layout.box()
                col = box.column(align=False)
                row = col.row(align=True)
                row.label(text='Selected Light Settings',icon='LIGHT_AREA')

                if obj.type == 'LIGHT':
                    col = layout.column(align=False)
                    col.label(text=obj.name +' Settings:')
                    col.prop(obj.data, "color")
                    col.prop(obj.data, "energy")
                    col.prop(obj.data, "shape", text="Shape")
                    sub = col.column(align=True)
                    if obj.data.shape in {'SQUARE', 'DISK'}:
                        sub.prop(obj.data, "size")
                    elif obj.data.shape in {'RECTANGLE', 'ELLIPSE'}:
                        sub.prop(obj.data, "size", text="Size X")
                        sub.prop(obj.data, "size_y", text="Y")
                    
                    sub = col.column(align=True)
                    sub.prop(obj.data.cycles, "cast_shadow",text="Cast Shadow(Cycles)")
                    
                    col = layout.column()
                    row = col.row(align=True)
                    row.prop_search(obj, "lightgroup", view_layer, "lightgroups", text="Light Group", results_are_suggestions=True)
                else:
                    col = layout.column(align=True)
                    col.alert=True
                    row = col.row(align=True)
                    row.label(text='NO LIGHT SELECTED',icon='ERROR')    

                #Camera Settings
                box = layout.box()
                col = box.column(align=False)
                row = col.row(align=True)
                row.label(text='Selected Camera Settings',icon='CAMERA_DATA')

                if obj.type == 'CAMERA':
                    col = layout.column(align=False)
                    col.label(text=obj.name +' Settings:')
                    if obj.constraints["Track To"]:
                        col.prop(obj.constraints["Track To"], 'target', text='Look At Constraint')
                    box = layout.box()
                    col = box.column(align=True)
                    col.prop(obj.data.dof, "use_dof", text="Depth of Field")
                    col.prop(obj.data.dof, "aperture_fstop")
                    if 'DOF_Focus_Target' in obj.data.dof.focus_object.name:
                        focus = bpy.data.objects[obj.data.dof.focus_object.name]
                        geoNode = focus.modifiers['GeometryNodes']               
                        if geoNode:
                            col.prop(geoNode, '["Input_2"]', text='Current DOF Target')
                        col.label(text='*Set DOF_Focus_Target Collection in Modifier')
                else:
                    col = layout.column(align=True)
                    col.alert=True
                    row = col.row(align=True)
                    row.label(text='NO CAMERA SELECTED',icon='ERROR')   

                #Look At Target Settings
                box = layout.box()
                col = box.column(align=False)
                row = col.row(align=True)
                row.label(text='Selected LookAt Target Settings',icon='CONSTRAINT')

                if obj.type == 'EMPTY' and 'LookAt' in obj.name:
                    col = layout.column(align=False)
                    col.label(text=obj.name +' Settings:')
                    if obj.constraints["Copy Rotation"]:
                        col.prop(obj.constraints["Copy Rotation"], 'target', text='Camera Constraint')
                    col.prop(tool_settings, "use_transform_skip_children", text="Keep Lights At Positions")
                else:
                    col = layout.column(align=True)
                    col.alert=True
                    row = col.row(align=True)
                    row.label(text='NO LOOKAT TARGET SELECTED',icon='ERROR')
        except:
            obj = context.scene.cursor

            col = layout.column(align=True)
            col.alert=True
            row = col.row(align=True)
            row.label(text='NO LIGHT SELECTED',icon='ERROR')    

            box = layout.box()
            col = box.column(align=False)
            row = col.row(align=True)
            row.label(text='Selected Camera Settings',icon='CAMERA_DATA')  

            col = layout.column(align=True)
            col.alert=True
            row = col.row(align=True)
            row.label(text='NO CAMERA SELECTED',icon='ERROR') 

            box = layout.box()
            col = box.column(align=False)
            row = col.row(align=True)
            row.label(text='Selected LookAt Target Settings',icon='CONSTRAINT')

            col = layout.column(align=True)
            col.alert=True
            row = col.row(align=True)
            row.label(text='NO LOOKAT TARGET SELECTED',icon='ERROR')

class SIMULIGHTCOMP_PT_render(Panel):
    bl_idname = 'SIMULIGHTCOMP_PT_render'
    bl_label = ''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Simu_LightComp'

    def draw_header(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Rendering Setup",icon='SCENE')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        window = context.window
        scene = window.scene
        rd = scene.render
        cscene = scene.cycles
        view_layer = context.view_layer                   
            
        #Render Settings
        
        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(scene, "camera",text='Render Camera')
        

        col = box.column(align=True)
        col.prop(rd, "resolution_x", text="Resolution X")
        col.prop(rd, "resolution_y", text="Y")
        col.prop(rd, "film_transparent", text="Transparent Background")

        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(rd, "engine", text="Render Engine")
        if context.engine == 'CYCLES':
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(cscene, "device")
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(cscene, "samples", text=" Max Samples")
            col = box.column(align=True)
            row = col.row(align=True)
            col.prop(view_layer, "use_pass_ambient_occlusion", text="Ambient Occlusion Pass")
        else:
            col = layout.column(align=True)
            col.alert=True
            row = col.row(align=True)
            row.label(text='MUST USE CYCLES FOR LIGHT GROUPS',icon='ERROR')
        box = layout.box()    
        col = box.column(align=True)
        col.scale_y = 2    
        col.operator("simu_lightcomp_render.viewport",text='RENDER  VIEWPORT',icon='RENDER_STILL')

            
            
            



    
        

#################################################################################
######################### PANEL PROPERTY CODE ###################################
################################################################################# 



#################################################################################
######################### Function CODE #########################################
################################################################################# 





#################################################################################
######################### OPERATOR CODE #########################################
#################################################################################

class UPDATE_OT_lightcomp_update_checker(Operator):
    """Check for Add-on Updates."""
    bl_idname = "simu_lightcomp_update.checker"
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

class SIMU_OT_create_layer_collection(Operator):
    """Create New Collection with View Layer Name."""
    bl_idname = "simu_lightcomp_collection.create"
    bl_label = "Create new layer collection"
    bl_description = 'Create new layer collection'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        collection = bpy.context.blend_data.collections.new(name= context.window.view_layer.name + '_Render_Layer',)
        bpy.context.collection.children.link(collection)

        return{'FINISHED'}

class SIMU_OT_toggle_camera_view(Operator):
    """Toggle Camera View."""
    bl_idname = "simu_lightcomp_view.camera"
    bl_label = "Toggle Camera View"
    bl_description = 'Toggle Camera View'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                if area.spaces[0].region_3d.view_perspective == 'PERSP' or area.spaces[0].region_3d.view_perspective == 'ORTHO':
                    area.spaces[0].region_3d.view_perspective = 'CAMERA'
                    break
                else:
                    area.spaces[0].region_3d.view_perspective = 'PERSP'
                    break

        return{'FINISHED'}

class SIMU_OT_use_walk_navigation(Operator):
    """Toggle Walk Navigation."""
    bl_idname = "simu_lightcomp_navigation.walk"
    bl_label = "Toggle Walk Navigation"
    bl_description = 'Toggle Walk Navigation. Controls appear at bottom of Blender window.'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        C = context
        walk_nav = C.preferences.inputs.walk_navigation
        walk_nav.walk_speed = 5

        for area in C.screen.areas:
            if area.type == 'VIEW_3D':
                override = C.copy()
                override['area'] = area
                override["region"] = area.regions[-1]
                bpy.ops.view3d.walk(override, 'INVOKE_DEFAULT')
                break

        return{'FINISHED'}

class SIMU_OT_fix_texture_paths(Operator):
    """Fixes file paths."""
    bl_idname = "simu_lightcomp_path.fix"
    bl_label = "Fix File Paths for Textures"
    bl_description = "Fix File Paths for Textures"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.file.find_missing_files('INVOKE_DEFAULT')

        return{'FINISHED'}

class SIMU_OT_render_viewport(Operator):
    """Render Viewport."""
    bl_idname = "simu_lightcomp_render.viewport"
    bl_label = "Render Viewport"
    bl_description = "Render Viewport"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.render.render('INVOKE_DEFAULT')

        return{'FINISHED'}

class SIMU_OT_exclude_collections(Operator):
    """Exclude Collections from Render Layer."""
    bl_idname = "simu_lightcomp_collection.exclude"
    bl_label = "Exclude Collections from Render Layer"
    bl_description = "Exclude Collections from Render Layer"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        for collection in context.scene.collection.children:
            if context.view_layer.name not in collection.name:
                context.layer_collection.children[collection.name].exclude = True

        return{'FINISHED'}





#################################################################################
######################### REGISTRATION CODE #####################################
#################################################################################   

def register():
    register_class(SIMULIGHTCOMP_PT_main)
    register_class(SIMULIGHTCOMP_PT_renderlayer)
    register_class(SIMULIGHTCOMP_PT_objectsettings)
    register_class(SIMULIGHTCOMP_PT_render)
    bpy.types.Scene.all_collections = PointerProperty(type=bpy.types.Collection)
    register_class(UPDATE_OT_lightcomp_update_checker)
    register_class(SIMU_OT_create_layer_collection)
    register_class(SIMU_OT_use_walk_navigation)
    register_class(SIMU_OT_toggle_camera_view)
    register_class(SIMU_OT_fix_texture_paths)
    register_class(SIMU_OT_render_viewport)
    register_class(SIMU_OT_exclude_collections)

    


def unregister():
    unregister_class(SIMULIGHTCOMP_PT_main)
    unregister_class(SIMULIGHTCOMP_PT_renderlayer)
    unregister_class(SIMULIGHTCOMP_PT_objectsettings)
    unregister_class(SIMULIGHTCOMP_PT_render)
    del bpy.types.Scene.all_collections
    unregister_class(UPDATE_OT_lightcomp_update_checker)
    unregister_class(SIMU_OT_create_layer_collection)
    unregister_class(SIMU_OT_use_walk_navigation)
    unregister_class(SIMU_OT_toggle_camera_view)
    unregister_class(SIMU_OT_fix_texture_paths)
    unregister_class(SIMU_OT_render_viewport)
    unregister_class(SIMU_OT_exclude_collections)
    