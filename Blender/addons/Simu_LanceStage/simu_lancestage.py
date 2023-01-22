
from multiprocessing import context
import bpy
import os
from bpy.props import IntProperty, PointerProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, FloatVectorProperty
from bpy.types import Panel, PropertyGroup, Operator
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ImportHelper

#################################################################################
######################### PANEL DRAW CODE #######################################
#################################################################################

class SIMULANCESTAGE_PT_main(Panel):
    bl_idname = 'SIMULANCESTAGE_PT_main'
    bl_label = ''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Simu_LanceStage'

    def draw_header(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Simu_LanceStage",icon='EVENT_L')

    def draw(self, context):
        layout = self.layout
        root = context.view_layer.objects.active
        propGroup = root.lancestage_vars
        #Addon update and tutorial section
        box = layout.box()
        col = box.column(align=True)
        col.scale_y = 1.5
        row = col.row(align=True)   
        row.operator("simu_lancestage_update.checker",text=r"Version 1.0.0 | Check For Updates",emboss=True,depress=False,icon='FILE_REFRESH')
        

        #Must select root of lance to make changes
        if root is not None and 'Controller' in root.name and root.type =='EMPTY':
            #Weapon selection
            col = layout.column()
            col.label(text=r"Weapon Toggles: " + root.name,icon='SETTINGS')
            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            row.label(text=r"")
            row.label(text=r"Right")
            row.label(text=r"Left")
            row = col.row(align=True)
            row.label(text=r"Primary")
            row.prop(propGroup,'primary_right',text=r"")
            row.prop(propGroup,'primary_left',text=r"")
            row = col.row(align=True)
            row.label(text=r"Secondary")
            row.prop(propGroup,'secondary_right',text=r"")
            row.prop(propGroup,'secondary_left',text=r"")
            # weapon_picker(context)

            #body color settings
            col = layout.column()
            col.label(text=r"Material Settings:",icon='MATERIAL')
            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(propGroup,'body_color',text=r"Body Color")
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(propGroup,'primary_color',text=r"Primary Color")
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(propGroup,'secondary_color',text=r"Secondary Color")

            #nose art settings
            col = box.column(align=True)
            row = col.row(align=True)
            row.label(text=r"Nose Art:")
            row.label(text=str(texture_name(context, "Nose Art")))
            row.operator("simu_lancestage.fbnoseart",text=r"",icon='FILEBROWSER')

            #skin texture settings
            col = box.column(align=True)
            row = col.row(align=True)
            row.label(text=r"Skin:")
            row.label(text=str(texture_name(context,"Skin")))
            row.operator("simu_lancestage.fbskin",text=r"",icon='FILEBROWSER')
            row = col.row(align=True)
            row.label(text=r"Pattern Scale")
            row.prop(propGroup,'pattern_scale',text=r"Pattern Scale",emboss=True,slider=False,)

            #grunge settings
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(propGroup,'grunge_color',text=r"Grunge Color")
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(propGroup, 'grunge_spread',text=r"Grunge",emboss=True,slider=True,)

            #edge wear and damage settings
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(propGroup, 'edgewear_amount',text=r"Edgewear",emboss=True,slider=True,)
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(propGroup, 'damage_amount',text=r"Damage",emboss=True,slider=True,)

            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            row.operator("simu_lancestage.update_selection",text=r"Update")

            

        else:
            col = layout.column()
            col.label(text=r"Weapon Toggles(SELECT CONTROLLER)",icon='SETTINGS')
                

    def execute(self, context):
        color_picker(context)
        material_values(context)
        

#################################################################################
######################### PANEL PROPERTY CODE ###################################
################################################################################# 

class SIMU_LanceStage_Vars(PropertyGroup):
    primary_right: EnumProperty(
        name='Primary Right Weapon: ',
        description='Select primary right weapon.',
        items=[
            ('0', "Wraith",""),
            ('1', "Catepult",""),
            ('2',"Inferno",""),
            ('3',"Banshee",""),
            ('4',"Brimstone",""),
            ('5',"Pike",""),
            ('6',"Javelin",""),
            ('7',"Hellfire",""),
            ('8',"Phalanx",""),
        ]

    )

    primary_left: EnumProperty(
        name='Primary Left Weapon: ',
        description='Select primary left weapon.',
        items=[
            ('0', "Wraith",""),
            ('1', "Catepult",""),
            ('2',"Inferno",""),
            ('3',"Banshee",""),
            ('4',"Brimstone",""),
            ('5',"Pike",""),
            ('6',"Javelin",""),
            ('7',"Hellfire",""),
            ('8',"Phalanx",""),
        ]

    )

    secondary_right: EnumProperty(
        name='Secondary Right Weapon: ',
        description='Select secondary right weapon.',
        items=[
            ('0', "Quadranid",""),
            ('1', "Parados",""),
            ('2',"Recurve",""),
            ('3',"Draconid",""),
            ('4',"Lurid",""),
            ('5',"Griffin",""),
        ]

    )

    secondary_left: EnumProperty(
        name='Secondary Left Weapon: ',
        description='Select secondary left weapon.',
        items=[
            ('0', "Quadranid",""),
            ('1', "Parados",""),
            ('2',"Recurve",""),
            ('3',"Draconid",""),
            ('4',"Lurid",""),
            ('5',"Griffin",""),
        ]

    )

    body_color: FloatVectorProperty(
        name = "Body Color",
        subtype = "COLOR",
        default = (1.0,1.0,1.0,1.0),
        min=0.0,
        max=1.0,
        size = 4,

    )

    primary_color: FloatVectorProperty(
        name = "Primary Color",
        subtype = "COLOR",
        default = (0.0,0.0,0.0,1.0),
        min=0.0,
        max=1.0,
        size = 4,

    )

    secondary_color: FloatVectorProperty(
        name = "Secondary Color",
        subtype = "COLOR",
        default = (0.0,0.0,0.0,1.0),
        min=0.0,
        max=1.0,
        size = 4,

    )

    pattern_scale: EnumProperty(
        name='Pattern Scale ',
        description='Select Pattern Scale',
        items=[
            ('0', "Tight",""),
            ('1', "Normal",""),
            ('2',"Loose",""),
        ],
        default= '1',

    )

    grunge_color: FloatVectorProperty(
        name = "Grunge Color",
        subtype = "COLOR",
        default = (0.205,0.084,0.0,1.0),
        min=0.0,
        max=1.0,
        size = 4,

    )

    grunge_spread: FloatProperty(
        name='grunge_spread',
        default=0.0,
        subtype='UNSIGNED',
        min=0.0,
        max=20.0,
    )

    edgewear_amount: FloatProperty(
        name='edgewear_amount',
        default=0.0,
        subtype='UNSIGNED',
        min=0.0,
        max=1.0,
    )

    damage_amount: FloatProperty(
        name='damage_amount',
        default=0.0,
        subtype='UNSIGNED',
        min=0.0,
        max=1.0,
    )
    

#################################################################################
######################### Function CODE #########################################
################################################################################# 

def weapon_picker(context):
    root = context.view_layer.objects.active
    propGroup = root.lancestage_vars

    #Lists of each weapon available for each attachment point
    primaryLeft = []
    primaryRight = []
    primaryLeftLower = []
    primaryRightLower = []
    secondaryLeft = []
    secondaryRight = []

    #The weapon attachment points
    primaryObjL = None
    primaryObjR = None
    primaryObjL_low = None
    primaryObjR_low = None
    secondaryObjL = None
    secondaryObjR = None
    
    #Assiging attachment points
    
    if 'Controller' in root.name and root.type =='EMPTY':
        collection = root.users_collection
        for child in collection[0].all_objects:
            if "0LanceStage_Primary_L" in child.name:
                primaryObjL = child
            if "0LanceStage_Primary_R" in child.name:
                primaryObjR = child
            if "0LanceStage_PrimeUpper_L" in child.name:
                primaryObjL = child
            if "0LanceStage_PrimeUpper_R" in child.name:
                primaryObjR = child
            if "0LanceStage_PrimeLower_L" in child.name:
                primaryObjL_low = child
            if "0LanceStage_PrimeLower_R" in child.name:
                primaryObjR_low = child
            if "0LanceStage_Secondary_L" in child.name:
                secondaryObjL = child
            if "0LanceStage_Secondary_R" in child.name:
                secondaryObjR = child
    
    #populating a weapon list for each attachment point
    for c in primaryObjL.children:
        primaryLeft.append(c)

    for c in primaryObjR.children:
        primaryRight.append(c)

    if primaryObjL_low:
        for c in primaryObjL_low.children:
            primaryLeftLower.append(c)

    if primaryObjR_low:
        for c in primaryObjR_low.children:
            primaryRightLower.append(c)

    for c in secondaryObjL.children:
        secondaryLeft.append(c)

    for c in secondaryObjR.children:
        secondaryRight.append(c)

    #toggle visibility based on UI selection
    for i in range (len(primaryLeft)):
        
        if str(i) == propGroup.primary_left:
            primaryLeft[i].hide_set(False)
            primaryLeft[i].hide_render = False

            for e in primaryLeft[i].children_recursive:
                e.hide_set(False)
                e.hide_render = False
            
        else:
            primaryLeft[i].hide_set(True)
            primaryLeft[i].hide_render = True
            
            for e in primaryLeft[i].children_recursive:
                e.hide_set(True)
                e.hide_render = True

    for i in range (len(primaryLeftLower)):
        
        if str(i) == propGroup.primary_left:
            primaryLeftLower[i].hide_set(False)
            primaryLeftLower[i].hide_render = False

            for e in primaryLeftLower[i].children_recursive:
                e.hide_set(False)
                e.hide_render = False
            
        else:
            primaryLeftLower[i].hide_set(True)
            primaryLeftLower[i].hide_render = True
            
            for e in primaryLeftLower[i].children_recursive:
                e.hide_set(True)
                e.hide_render = True

    for i in range (len(primaryRight)):
        
        if str(i) == propGroup.primary_right:
            primaryRight[i].hide_set(False)
            primaryRight[i].hide_render = False

            for e in primaryRight[i].children_recursive:
                e.hide_set(False)
                e.hide_render = False
            
        else:
            primaryRight[i].hide_set(True)
            primaryRight[i].hide_render = True
            
            for e in primaryRight[i].children_recursive:
                e.hide_set(True)
                e.hide_render = True

    for i in range (len(primaryRightLower)):
        
        if str(i) == propGroup.primary_right:
            primaryRightLower[i].hide_set(False)
            primaryRightLower[i].hide_render = False

            for e in primaryRightLower[i].children_recursive:
                e.hide_set(False)
                e.hide_render = False
            
        else:
            primaryRightLower[i].hide_set(True)
            primaryRightLower[i].hide_render = True
            
            for e in primaryRightLower[i].children_recursive:
                e.hide_set(True)
                e.hide_render = True

    for i in range (len(secondaryLeft)):
        
        if str(i) == propGroup.secondary_left:
            secondaryLeft[i].hide_set(False)
            secondaryLeft[i].hide_render = False

            for e in secondaryLeft[i].children_recursive:
                e.hide_set(False)
                e.hide_render = False
            
        else:
            secondaryLeft[i].hide_set(True)
            secondaryLeft[i].hide_render = True
            
            for e in secondaryLeft[i].children_recursive:
                e.hide_set(True)
                e.hide_render = True

    for i in range (len(secondaryRight)):
        
        if str(i) == propGroup.secondary_right:
            secondaryRight[i].hide_set(False)
            secondaryRight[i].hide_render = False

            for e in secondaryRight[i].children_recursive:
                e.hide_set(False)
                e.hide_render = False
            
        else:
            secondaryRight[i].hide_set(True)
            secondaryRight[i].hide_render = True
            
            for e in secondaryRight[i].children_recursive:
                e.hide_set(True)
                e.hide_render = True
                
def texture_load(self,root, texture_name, path):
    nodetex = bpy.data.images.load(path)
    if 'Controller' in root.name and root.type =='EMPTY':
        collection = root.users_collection
        for child in collection[0].all_objects:

            if child.type == 'MESH' and len(child.material_slots) > 0:
                mat = bpy.data.materials.get(child.material_slots[0].material.name)
                
                if texture_name in mat.node_tree.nodes:
                    texnode = mat.node_tree.nodes[texture_name]
                    if texnode:
                        texnode.image = nodetex
           
def texture_name(context, texture_name):
    root = context.view_layer.objects.active
    
    if 'Controller' in root.name and root.type =='EMPTY':
        collection = root.users_collection
        for child in collection[0].all_objects:

            if child.type == 'MESH' and len(child.material_slots) > 0:
                mat = bpy.data.materials.get(child.material_slots[0].material.name)
                
                if texture_name in mat.node_tree.nodes:
                    texnode = mat.node_tree.nodes[texture_name]
                    if texnode:
                        return texnode.image.name


def color_picker(context):
    root = context.view_layer.objects.active
    propGroup = root.lancestage_vars
    bodyColor = "Body Color"
    primaryColor = "Primary Color"
    secondaryColor = "Secondary Color"
    grungeColor = "Grunge Color"

    if 'Controller' in root.name and root.type =='EMPTY':
        collection = root.users_collection
        for child in collection[0].all_objects:
            if child.type == 'MESH' and len(child.material_slots) > 0:
                mat = bpy.data.materials.get(child.material_slots[0].material.name)

                if bodyColor in mat.node_tree.nodes:
                    texnode = mat.node_tree.nodes[bodyColor]
                    if texnode:
                        texnode.outputs[0].default_value = propGroup.body_color
                
                if primaryColor in mat.node_tree.nodes:
                    texnode = mat.node_tree.nodes[primaryColor]
                    if texnode:
                        texnode.outputs[0].default_value = propGroup.primary_color
                
                if secondaryColor in mat.node_tree.nodes:
                    texnode = mat.node_tree.nodes[secondaryColor]
                    if texnode:
                        texnode.outputs[0].default_value = propGroup.secondary_color

                if grungeColor in mat.node_tree.nodes:
                    texnode = mat.node_tree.nodes[grungeColor]
                    if texnode:
                        texnode.outputs[0].default_value = propGroup.grunge_color

def material_values(context):
    root = context.view_layer.objects.active
    propGroup = root.lancestage_vars
    edgewear = "Edgewear Amount"
    grunge = "Grunge Spread"
    damage = "Damage Amount"

    if 'Controller' in root.name and root.type =='EMPTY':
        collection = root.users_collection
        for child in collection[0].all_objects:
            if child.type == 'MESH' and len(child.material_slots) > 0:
                mat = bpy.data.materials.get(child.material_slots[0].material.name)

                if edgewear in mat.node_tree.nodes:
                    texnode = mat.node_tree.nodes[edgewear]
                    texnode.outputs[0].default_value = propGroup.edgewear_amount

                if grunge in mat.node_tree.nodes:
                    texnode = mat.node_tree.nodes[grunge]
                    texnode.outputs[0].default_value = propGroup.grunge_spread
                
                if damage in mat.node_tree.nodes:
                    texnode = mat.node_tree.nodes[damage]
                    texnode.outputs[0].default_value = propGroup.damage_amount


def pattern_scale(context):
    root = context.view_layer.objects.active
    propGroup = root.lancestage_vars
    tiling = "Skin Tiling"
    tileAmount = 0

    if propGroup.pattern_scale == '0':
        tileAmount = 8
    elif propGroup.pattern_scale == '1':
        tileAmount = 6
    elif propGroup.pattern_scale == '2':
        tileAmount = 4


    if 'Controller' in root.name and root.type =='EMPTY':
        collection = root.users_collection
        for child in collection[0].all_objects:
            if child.type == 'MESH' and len(child.material_slots) > 0:
                mat = bpy.data.materials.get(child.material_slots[0].material.name)

                if tiling in mat.node_tree.nodes:
                    texnode = mat.node_tree.nodes[tiling]
                    texnode.inputs[3].default_value[0] = tileAmount
                    texnode.inputs[3].default_value[1] = tileAmount
                    texnode.inputs[3].default_value[2] = tileAmount

                





    

#################################################################################
######################### OPERATOR CODE #########################################
#################################################################################

class UPDATE_OT_lancestage_update_checker(Operator):
    """Check for Add-on Updates."""
    bl_idname = "simu_lancestage_update.checker"
    bl_label = "Check: Add-on Updates"
    bl_description = 'Check for Add-on Updates'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.script.reload()
    
        self.report({'INFO'}, "Simu_LanceStage update check completed.")

        return{'FINISHED'}

class SIMU_OT_filebrowswer_noseart(Operator, ImportHelper):
    bl_idname = "simu_lancestage.fbnoseart" 
    bl_label = "Import Nose Art Texture" 

    filter_glob: StringProperty( default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp', options={'HIDDEN'} ) 

    def execute(self, context):
        root = context.view_layer.objects.active
        file = os.path.basename(self.filepath) 
        filename, extension = os.path.splitext(file)
        
        types = ('.jpg','.jpeg','.png','.tif','.tiff','.bmp')

        
        if extension in types:
            texture_load(self,root, "Nose Art", self.filepath)
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        

        return{'FINISHED'}

class SIMU_OT_filebrowswer_skin(Operator, ImportHelper):
    bl_idname = "simu_lancestage.fbskin" 
    bl_label = "Import Skin Texture" 

    filter_glob: StringProperty( default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp', options={'HIDDEN'} ) 

    def execute(self, context):
        root = context.view_layer.objects.active
        file = os.path.basename(self.filepath) 
        filename, extension = os.path.splitext(file)
        
        types = ('.jpg','.jpeg','.png','.tif','.tiff','.bmp')

        
        if extension in types:
            texture_load(self,root, "Skin", self.filepath)
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
            

        return{'FINISHED'}

class SIMU_OT_update_selection(Operator):
    """Update Selecton."""
    bl_idname = "simu_lancestage.update_selection"
    bl_label = "Update Selection"
    bl_description = 'Update Selection'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        weapon_picker(context)
        color_picker(context)
        material_values(context)
        pattern_scale(context)
        

        return{'FINISHED'}



#################################################################################
######################### REGISTRATION CODE #####################################
#################################################################################   

def register():
    register_class(SIMU_LanceStage_Vars)
    register_class(SIMULANCESTAGE_PT_main)
    bpy.types.Object.lancestage_vars = PointerProperty(type=SIMU_LanceStage_Vars)
    register_class(UPDATE_OT_lancestage_update_checker)
    register_class(SIMU_OT_update_selection)
    register_class(SIMU_OT_filebrowswer_noseart)
    register_class(SIMU_OT_filebrowswer_skin)
    


def unregister():
    unregister_class(SIMU_LanceStage_Vars)
    unregister_class(SIMULANCESTAGE_PT_main)
    del bpy.types.Object.lancestage_vars
    unregister_class(UPDATE_OT_lancestage_update_checker)
    unregister_class(SIMU_OT_update_selection)
    unregister_class(SIMU_OT_filebrowswer_noseart)
    unregister_class(SIMU_OT_filebrowswer_skin)
