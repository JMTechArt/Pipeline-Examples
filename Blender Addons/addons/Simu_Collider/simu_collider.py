import bpy
from bpy.props import IntProperty, PointerProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty
from bpy.types import Panel, PropertyGroup, Operator
from bpy.utils import register_class, unregister_class

#################################################################################
######################### PANEL DRAW CODE #######################################
#################################################################################

class SIMUCOLLIDER_PT_main(Panel):
    bl_idname = 'SIMUCOLLIDER_PT_main'
    bl_label = ''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Simu_Collider'

    def draw_header(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Simu_Collider",icon='EVENT_C')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        active = context.view_layer.objects.active
        
        #Addon update and tutorial section
        box = layout.box()
        col = box.column(align=True)
        col.scale_y = 1.5
        row = col.row(align=True)   
        row.operator("simu_collider_update.checker",text=r"Version 1.0.0 | Check For Updates",emboss=True,depress=False,icon='FILE_REFRESH')
        col = box.column(align=True)
        col.operator("wm.url_open", text=r"View Help and Info",icon='HELP').url = "https://github.com/simutronics/Galahad/blob/master/3DArtTools/Blender/scripts/addons/Simu_Collider/READ_ME.md"

        #setup area
        setup_box = layout.box()
        setup_box.enabled = True
        setup_col = setup_box.column()
        setup_col.alert = True
        setup_col.scale_y = 1.5
        row = setup_col.row(align=True)
        row.operator("simu_collider.setup_collider",text=r"Setup Collider Tools",emboss=True,depress=False,icon='TOOL_SETTINGS')
        #generate area
        generate_box = layout.box()
        generate_box.enabled = True
        col = generate_box.column(align=True)
        row = col.row(align=True)
        row.label(text=r"Collider Mask Vertex Group:")
        col = generate_box.column(align=True)
        row = col.row(align=True)
        row.operator("object.vertex_group_assign",text=r"Assign")
        row.operator("object.vertex_group_remove_from",text=r"Remove")
        row = col.row(align=True)
        row.operator("object.vertex_group_select",text=r"Select")
        row.operator("object.vertex_group_deselect",text=r"Deselect")
             
        if active is not None and context.active_object.modifiers.get('Decimate'):
            col = generate_box.column()
            row = col.row()
            row.prop(context.active_object.modifiers["Decimate"], 'ratio',text=r"Reduce")
        else:
            col = generate_box.column()
            row = col.row()
            row.label(text=r"Reduce")
        if active is not None and context.active_object.modifiers.get('Decimate'):
            col = generate_box.column()
            row = col.row()
            row.prop(context.active_object.modifiers["Displace"], 'strength',text=r"Inflate/Deflate")
        else:
            col = generate_box.column()
            row = col.row()
            row.label(text=r"Inflate/Deflate")
        col = generate_box.column(align=True)
        row = col.row(align=True)
        row.label(text=r"Collider Naming Convention:")
        col = generate_box.column()
        row = col.row()
        row.prop(context.scene.collider_vars,'pick_collider_type',text=r"")
        generate_col = generate_box.column()
        #force naming convention choice
        if context.scene.collider_vars.pick_collider_type == 'none':
            generate_col.enabled = False
        else:
            generate_col.enabled = True
        generate_col.alert = True
        generate_col.scale_y = 1.5
        row = generate_col.row(align=True)
        row.operator("simu_collider.generate_collider",text=r"Generate New Collider",emboss=True,depress=False,icon='META_CUBE')
        #area toggles
        if active is None:
            setup_box.enabled = False
            generate_box.enabled = False
            context.scene.collider_vars.property_unset('pick_collider_type')
        elif 'copy' not in active.name:
            setup_box.enabled = True
            generate_box.enabled = False
            context.scene.collider_vars.property_unset('pick_collider_type')
        elif 'copy' in active.name:
            setup_box.enabled = False
            generate_box.enabled = True    

#################################################################################
######################### PANEL PROPERTY CODE ###################################
################################################################################# 

class SIMU_Collider_Vars(PropertyGroup):
     pick_collider_type: EnumProperty(
        name='Collider Type: ',
        description='Select type of collider.',
        items=[
            ('none', "Not Set : Generation Disabled",""),
            ('box', "Box : UBX",""),
            ('convex',"Convex Hull : UCX",""),
            ('mesh',"Mesh : UMC",""),
        ]

    )

#################################################################################
######################### Function CODE #########################################
################################################################################# 



#################################################################################
######################### OPERATOR CODE #########################################
#################################################################################

class UPDATE_OT_collider_update_checker(Operator):
    """Check for Add-on Updates."""
    bl_idname = "simu_collider_update.checker"
    bl_label = "Check: Add-on Updates"
    bl_description = 'Check for Add-on Updates'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.script.reload()
    
        self.report({'INFO'}, "Simu_Collider update check completed.")

        return{'FINISHED'}

class SIMU_OT_setup_collider(Operator):
    """Setup a duplicate of the selection and create modifiers."""
    bl_idname = "simu_collider.setup_collider"
    bl_label = "Setup: Collider"
    bl_description = 'Setup Collider'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        if context.view_layer.objects.active is not None:
            obj = context.view_layer.objects.active

            if obj.type == 'MESH':
                # make copy
                obj_copy = obj.copy()
                obj_copy.data = obj_copy.data.copy()
                # rename copy
                obj_copy.name = obj.name + '_copy'
                obj_copy.data.name = obj.name + '_copy'
                # link copy to scene
                collection = obj.users_collection[0]
                collection.objects.link(obj_copy)
                # parent copy to original
                obj_copy.parent = obj
                # create vertex group
                obj_copy.vertex_groups.new( name = 'Collider Mask' )

                ##.....GEOMETRY NODE GENERATION.......##
                # create geometry node modifier
                geonodemod = obj_copy.modifiers.new(name='Geometry Nodes',type='NODES')
                #setup geo node group data
                if bpy.data.node_groups.get("Collider Nodes") is None:
                    bpy.data.node_groups.new(name='Collider Nodes',type='GeometryNodeTree')
                    
                    node_grp = bpy.data.node_groups.get("Collider Nodes")
                    n_inputs = node_grp.inputs
                    n_outputs = node_grp.outputs
                    n_inputs.new(type="NodeSocketGeometry",name="Geometry")
                    n_outputs.new(type="NodeSocketGeometry",name="Geometry")
                    #create input/output nodes required
                    nodes = node_grp.nodes
                    outputnode = nodes.new(type="NodeGroupOutput")
                    outputnode.location.x = 0
                    outputnode.location.y = 0
                    inputnode = nodes.new(type="NodeGroupInput")
                    inputnode.location.x = -500
                    inputnode.location.y = 0
                    #create default node links
                    links = node_grp.links
                    links.new(nodes["Group Input"].outputs["Geometry"], nodes["Group Output"].inputs["Geometry"])
                #assign newly created node group to created geometry node modifier
                geonodemod.node_group = bpy.data.node_groups['Collider Nodes']
                ##..END GEO NODE STUFF..##

                #setup other modifiers
                obj_copy.modifiers.new(name='Decimate',type='DECIMATE')
                obj_copy.modifiers.new(name='Displace',type='DISPLACE')
                obj_copy.modifiers['Displace'].strength = 0
                # create collider material
                mat = bpy.data.materials.get('Collider_Setup_Mat')
                if bpy.data.materials.get('Collider_Setup_Mat') is None:
                    mat = bpy.data.materials.new(name='Collider_Setup_Mat')
                    mat.use_nodes = True
                    nodes = mat.node_tree.nodes
                    bsdf = nodes['Principled BSDF']
                    bsdf.inputs[0].default_value = (0.00458456, 0.0962419, 0.8, 1)
                    bsdf.inputs[7].default_value = 0
                    bsdf.inputs[9].default_value = 0
                    bsdf.inputs[21].default_value = 0.5
                    mat.blend_method = 'BLEND'
                # attach material to collider object
                # obj_copy.data.materials.append(mat)
                # swap selection
                obj.select_set(False)
                context.view_layer.objects.active = obj_copy
                # make geo node modifier active
                bpy.ops.object.modifier_set_active(modifier="Geometry Nodes")
                self.report({'INFO'}, "Collider setup process initiated")

        return{'FINISHED'}

class SIMU_OT_generate_collider(Operator):
    """Generate final collider."""
    bl_idname = "simu_collider.generate_collider"
    bl_label = "Generate: Collider"
    bl_description = 'Generate Collider'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        if context.mode == 'OBJECT':
            if context.view_layer.objects.active is not None:
                obj = context.view_layer.objects.active
                obj.select_set(True)

                if obj.type == 'MESH' and 'copy' in obj.name:
                    # rename copy based on collider type
                    if context.scene.collider_vars.pick_collider_type == 'box':
                        obj.name = 'UBX_' + obj.name[:-5] + '_boxCollider'
                        obj.data.name = obj.name[:-5] + '_boxCollider'
                    if context.scene.collider_vars.pick_collider_type == 'convex':
                        obj.name = 'UCX_' + obj.name[:-5] + '_convexCollider'
                        obj.data.name = obj.name[:-5] + '_convextCollider'                
                    if context.scene.collider_vars.pick_collider_type == 'mesh':
                        obj.name = 'UMC_' + obj.name[:-5] + '_meshCollider'
                        obj.data.name = obj.name[:-5] + '_meshCollider'
                    # apply modifiers and return to being a normal mesh object
                    bpy.ops.object.convert(target='MESH')
                    # remove vertex group
                    vg = obj.vertex_groups.get('Collider Mask')
                    if vg is not None:
                        obj.vertex_groups.remove(vg)
                    # create final collider material
                    mat = bpy.data.materials.get('Collider_Generated_Mat')
                    if bpy.data.materials.get('Collider_Generated_Mat') is None:
                        mat = bpy.data.materials.new(name='Collider_Generated_Mat')
                        mat.use_nodes = True
                        nodes = mat.node_tree.nodes
                        bsdf = nodes['Principled BSDF']
                        bsdf.inputs[0].default_value = (0.8, 0.404982, 0.0202153, 1)
                        bsdf.inputs[7].default_value = 0
                        bsdf.inputs[9].default_value = 0
                        bsdf.inputs[21].default_value = 0.5
                        mat.blend_method = 'BLEND'
                    # attach new final material to collider object
                    obj.data.materials.append(mat)
                    #remove old setup material(work around for geo node bug)
                    if context.scene.collider_vars.pick_collider_type == "box":
                        for i in range(2):
                            obj.active_material_index = 0
                            bpy.ops.object.material_slot_remove()
                    else:
                        obj.active_material_index = 0
                        bpy.ops.object.material_slot_remove()
                    
                    # swap selection
                    obj.select_set(False)
                    context.view_layer.objects.active = obj.parent
                    obj.parent.select_set(True)
                    self.report({'INFO'}, "New Collider has been generated.")
        else:
            self.report({'ERROR'}, "Need to be in Object Mode. You are in Edit Mode.")

        return{'FINISHED'}

#################################################################################
######################### REGISTRATION CODE #####################################
#################################################################################   

def register():
    register_class(SIMU_Collider_Vars)
    register_class(SIMUCOLLIDER_PT_main)
    bpy.types.Scene.collider_vars = PointerProperty(type=SIMU_Collider_Vars)
    register_class(UPDATE_OT_collider_update_checker)
    register_class(SIMU_OT_setup_collider)
    register_class(SIMU_OT_generate_collider)

def unregister():
    unregister_class(SIMU_Collider_Vars)
    unregister_class(SIMUCOLLIDER_PT_main)
    del bpy.types.Scene.collider_vars
    unregister_class(UPDATE_OT_collider_update_checker)
    unregister_class(SIMU_OT_setup_collider)
    unregister_class(SIMU_OT_generate_collider)