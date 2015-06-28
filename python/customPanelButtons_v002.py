#----------------------------------------------------------
# File customPanelButtons.py
#----------------------------------------------------------
import bpy

#
#    Menu in window region, object context
#
class ObjectPanel(bpy.types.Panel):
    bl_label = "Maelstrom II Edit"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
 
    def draw(self, context):
        self.layout.operator("maelstrom2.edit", text='unhide hidden').country = "France"
        self.layout.operator("maelstrom2.deletefontobjects", text='deleteFontObjects').country = "France"
        self.layout.operator("maelstrom2.seq_2_text", text='sequence to text').country = "France"
        
def unhideHidden():
    for obj in bpy.data.objects:
        print("Unhiding ",obj)
        obj.hide = False
        obj.hide_render = False

def deleteFontObjects():
    #print("bpy.context.space_data.context = 'OBJECT'")
    #bpy.context.space_data.context = 'OBJECT'
    print("Setting object mode to OBJECT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    print("Selecting all FONT objects")
    bpy.ops.object.select_by_type(type='FONT')
    print("Deleting selected")
    bpy.ops.object.delete(use_global=False)
    print("Removing Meshes")
    for item in bpy.data.meshes:
        print("Removing MESH for item:",item)
        try:
            bpy.data.meshes.remove(item)
        except:
            print ("item mesh has owner:",item)

def seq_to_text(seq_all):
  print("seq_to_text")
  m = bpy.data.materials.new("test")
  m.use_shadeless = True
  y = 0
  t_o = []
  seq_all_len = len(seq_all)
  print("seq_all_len",seq_all_len)
  textScale = 1.0/((seq_all_len - 1)*5.0)
  print("textScaleB:",textScale)
  print("bpy.ops.object",bpy.ops.object)
  for s in seq_all:
    print("s",s)
    s_n = s.name
    if "transform" in s_n.lower():
      continue
    if "wipe" in s_n.lower():
      continue
    if s.mute == True:
      continue
    print("bpy.ops.object B:",bpy.ops.object)
    bpy.ops.object.text_add(radius=1.0, view_align=False, enter_editmode=False, location=(0, s.channel, 0), rotation=(0, 0, 0))
    ob = bpy.context.active_object
    print("ob",ob)
    ob.data.resolution_u = 1
    #assign material
    ob.data.materials.append(m)
    ob.name = s_n
    t_o.append(ob)
    tcu = ob.data
    tcu.body = s_n
    print("s_n",s_n)
    if s_n == 'Scene':
      print ("s_n = 'Scene'")
      ob.hide = True
      ob.hide_render = True
    else:
      print ("s_n != 'Scene'")
    y += 1
  return(t_o)

class OBJECT_OT_unhideHiddenButton(bpy.types.Operator):
    bl_idname = "maelstrom2.edit"
    bl_label = "Say Hello"
    country = bpy.props.StringProperty()
 
    def execute(self, context):
        print("unhideHidden()")
        unhideHidden()
        return{'FINISHED'}    

class OBJECT_OT_deleteFontObjects(bpy.types.Operator):
    bl_idname = "maelstrom2.deletefontobjects"
    bl_label = "deleteFontObjects"
    country = bpy.props.StringProperty()
 
    def execute(self, context):
        print("deleteFontObjects()")
        deleteFontObjects()
        return{'FINISHED'}    

class OBJECT_OT_seq_2_text(bpy.types.Operator):
    bl_idname = "maelstrom2.seq_2_text"
    bl_label = "seq_2_text"
    country = bpy.props.StringProperty()
 
    def execute(self, context):
        print("seq_2_text()")
        print("context",context)
        # convert all sequences to text objects
        seq_all = bpy.data.scenes["Scene"].sequence_editor.sequences_all
        print("seq_all",seq_all)
        t_o_a = seq_to_text(seq_all)
        return{'FINISHED'}    

#	Registration
#   All panels and operators must be registered with Blender; otherwise
#   they do not show up. The simplest way to register everything in the
#   file is with a call to bpy.utils.register_module(__name__).
#
 
bpy.utils.register_module(__name__)
#bpy.utils.register_class(OBJECT_OT_unhideHiddenButton)
#bpy.utils.register_class(OBJECT_OT_deleteFontObjects)
#bpy.utils.unregister_module(__name__)