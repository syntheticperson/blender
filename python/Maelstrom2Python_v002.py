import bpy
from bpy.app.handlers import persistent
import time

def updateFrame(frame):
  print("updateFrame", frame)
  seq_all = bpy.data.scenes["Scene"].sequence_editor.sequences_all
  visibleObjects = []
  for s in seq_all:
    b = s
    #print(b.name," frame_start:",b.frame_start)
    try:
      o = bpy.data.objects[b.name]
    except:
      #print("Couldn't find ",b.name)
      continue
    #print("object:",o)
#    if frame < (b.frame_final_start - 1) or frame > (b.frame_final_end - 2):
#    if frame < (b.frame_final_start) or frame > (b.frame_final_end):
    if frame < (b.frame_final_start) or frame > (b.frame_final_end - 1):
      #print("hiding "+o.data.body)
      o.hide = True
      o.hide_render = True
    else:
      print("unhiding "+o.data.body)
      o.hide = False
      o.hide_render = False
      print("appending object",o)
      visibleObjects.append(o)
      print("visibleObjects",visibleObjects)
    if o.data.body == 'Scene':
      #print ("o.data.body = 'Scene'. Forcing hide")
      o.hide = True
      o.hide_render = True
    #time.sleep(0.125)
    #time.sleep(0.05)
  #return visibleObjects
  print("calling alignVisible() with",visibleObjects)
  hideAll()
  alignVisible(visibleObjects)

def alignVisible(visibleObjects):
  print("alignVisible()",visibleObjects)
  y = 0
  for o in visibleObjects:
    #bpy.context.object.location[1] = -16.99
    o.location[1] = y
    print ("Setting",o,"location[1] to ",o.location[1])
    if o.data.body != 'Scene':
      o.hide = False
      o.hide_render = False
    y = y + 1

def seq_to_text(seq_all):
  print("seq_to_text")
  m = bpy.data.materials.new("test")
  m.use_shadeless = True
#    seq_all = scenes['Scene'].sequence_editor.sequences_all
  y = 0
  t_o = []
  seq_all_len = len(seq_all)
  print("seq_all_len",seq_all_len)
#  textScale = 1.0/((seq_all_len - 1)*10.0)
  textScale = 1.0/((seq_all_len - 1)*5.0)
  print("textScale:",textScale)
  for s in seq_all:
    s_n = s.name
    if "transform" in s_n.lower():
      continue
    if "wipe" in s_n.lower():
      continue
    if s.mute == True:
      continue
    #bpy.ops.object.text_add(radius=1.0, view_align=False, enter_editmode=False, location=(s.frame_final_start*textScale*2, s.channel, -s.channel), rotation=(0, 0, 0))
    bpy.ops.object.text_add(radius=1.0, view_align=False, enter_editmode=False, location=(0, s.channel, 0), rotation=(0, 0, 0))
    ob = bpy.context.active_object
    # set text resolution to lowest
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
# end of def seq_to_text(seq_all):

# convert all sequences to text objects
seq_all = bpy.data.scenes["Scene"].sequence_editor.sequences_all
t_o_a = seq_to_text(seq_all)

def deleteFontObjects():
    print("Setting context to OBJECT")
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

def createCam():
    cam = bpy.ops.object.camera_add()
    ob = bpy.context.object
    ob.name = "myCam"
    return cam

def moveCam(name,x,y):
    print("Selecting:",name)
    select_name(name)
    bpy.context.object.location[0] = x
    bpy.context.object.location[1] = y

def select_name( name = "", extend = True ):
    if extend == False:
        bpy.ops.object.select_all(action='DESELECT')
    ob = bpy.data.objects.get(name)
    ob.select = True
    bpy.context.scene.objects.active = ob

def unhideHidden():
    for obj in bpy.data.objects:
#        if obj.hide == True:
        print("Unhiding ",obj)
        obj.hide = False
        obj.hide_render = False

def hideAll():
    print("hideAll()")
    for obj in bpy.data.objects:
#        if obj.hide == True:
        print("Unhiding ",obj)
        obj.hide = True
        obj.hide_render = True

def createMaterial():
    bpy.ops.material.new()
    bpy.context.object.active_material.emit = 1
    bpy.context.object.active_material.use_shadeless = True
# select all objects to have same material
# then select object with target material
# then this command links the target material to all selected objects
#    bpy.ops.object.make_links_data(type='MATERIAL')

def renderFrameRange():
    print("renderFrameRange()")
    for frame in range(98605,101720):
        bpy.context.scene.frame_current = frame
        print("frame: ", frame)
        updateFrame(frame)
        setRenderOutputName(frame)
        bpy.ops.render.render(write_still=True)

def setRenderOutputName(frameNumber):
  print("setRenderOutputName()")
  import os
  frameNumberAndExtension = str(frameNumber) + ".png"
  filename = bpy.path.basename(bpy.data.filepath)
  filename = os.path.splitext(filename)[0]
  if filename:
    fileNameFrameNumberExtension = filename + "." + frameNumberAndExtension
    filepath = os.path.join("//../comp/cm2_edit_VO_2015-06-14.24fps/", fileNameFrameNumberExtension)
    print ("Setting filepath to:",filepath)
    bpy.context.scene.render.filepath = filepath

class Maelstrom2Panel(bpy.types.Panel):
    bl_label = "Maelstrom II Edit"
    bl_idname = "SCENE_PT_maelstrom2"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
 
    def draw(self, context):
        self.layout.operator("object.unhide_hidden", text='unhide hidden')
        self.layout.operator("object.delete_font_objects", text='delete font objects')
        self.layout.operator("object.sequence_to_text", text='sequence to text')

class UnhideHiddenButton(bpy.types.Operator):
    bl_idname = "object.unhide_hidden"
    bl_label = "unhide hidden"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print("unhideHidden()")
        unhideHidden()
        return{'FINISHED'}
 
class DeleteFontObjects(bpy.types.Operator):
    bl_idname = "object.delete_font_objects"
    bl_label = "delete font objects"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
 
    def execute(self, context):
        print("deleteFontObjects()")
        deleteFontObjects()
        return{'FINISHED'}

class SequenceToText(bpy.types.Operator):
    bl_idname = "object.sequence_to_text"
    bl_label = "sequence to text"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
 
    def execute(self, context):
        print("seq_2_text()")
        print("context",context)
        # convert all sequences to text objects
        seq_all = bpy.data.scenes["Scene"].sequence_editor.sequences_all
        print("seq_all",seq_all)
        t_o_a = seq_to_text(seq_all)
        return{'FINISHED'}    
    
#def register():
#    bpy.utils.register_class(Maelstrom2Panel)

bpy.utils.register_module(__name__)
#bpy.utils.register_class(UnhideHiddenButton)
#bpy.utils.unregister_module(__name__)
