import bpy
from bpy.app.handlers import persistent
import time

#@persistent
#def preRenderHandler(self):
#  scene = bpy.data.scenes["Scene"]
#  frame = scene.frame_current
#  print("preRenderHandler: <======\nFrame ", frame)
##  frameChangeHandler(scene)

@persistent
def preRenderHandler(self):
  scene = bpy.data.scenes["Scene"]
  frame = scene.frame_current
  print("preRenderHandler:\nFrame ", frame)
  updateFrame(frame)

@persistent
def frameChangeHandler(scene):
  #scene = bpy.data.scenes["Scene"]
  frame = scene.frame_current
  print("frameChangeHandler: <======\nFrame ", frame)
  updateFrame(frame)

def updateFrame(frame):
  print("updateFrame", frame)
  seq_all = bpy.data.scenes["Scene"].sequence_editor.sequences_all
  for s in seq_all:
    b = s
    bfs = b.frame_start
    print(b.name," frame_start:",b.frame_start)
    try:
      o = bpy.data.objects[b.name]
    except:
      print("Couldn't find ",b.name)
      continue
    print("object:",o)
#    if frame < (b.frame_final_start - 1) or frame > (b.frame_final_end - 2):
#    if frame < (b.frame_final_start) or frame > (b.frame_final_end):
    if frame < (b.frame_final_start) or frame > (b.frame_final_end - 1):
      print("hiding "+o.data.body)
      o.hide = True
      o.hide_render = True
    else:
      print("unhiding "+o.data.body)
      o.hide = False
      o.hide_render = False
    if o.data.body == 'Scene':
      print ("o.data.body = 'Scene'. Forcing hide")
      o.hide = True
      o.hide_render = True
    time.sleep(0.125)

def seq_to_text(seq_all):
  print("seq_to_text")
#    seq_all = scenes['Scene'].sequence_editor.sequences_all
  y = 0
  t_o = []
  seq_all_len = 0
  seq_all_len = len(seq_all)
  print("seq_all_len",seq_all_len)
  textScale = 1.0/(seq_all_len - 1)
  textScale = 1.0/((seq_all_len - 1)*10.0)
  print("textScale:",textScale)
  for s in seq_all:
    s_n = s.name
    if "transform" in s_n.lower():
      continue
    if "wipe" in s_n.lower():
      continue
    if s.mute == True:
      continue
    bpy.ops.object.text_add(radius=1.0, view_align=False, enter_editmode=False, location=(s.frame_final_start*textScale*2, s.channel, -s.channel), rotation=(0, 0, 0))
    ob = bpy.context.object
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

## add handlers
#print("bpy.app.handlers.frame_change_pre.clear()")
#bpy.app.handlers.frame_change_pre.clear()
#print("bpy.app.handlers.frame_change_pre.append(frameChangeHandler)")
#bpy.app.handlers.frame_change_pre.append(frameChangeHandler)

print("bpy.app.handlers.render_pre.clear()")
bpy.app.handlers.render_pre.clear()
print("bpy.app.handlers.render_pre.append(preRenderHandler)")
bpy.app.handlers.render_pre.append(preRenderHandler)

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
    scene = bpy.data.scenes["Scene"]
    for frame in range(1,15):
        bpy.context.scene.frame_current = frame
        print("frame: ", frame)
        updateFrame(frame)
        setRenderOutputName(frame)
        bpy.ops.render.render(write_still=True)

def setRenderOutputName(frameNumber):
  print("setRenderOutputName()")
  import os
  import bpy
  frameNumberAndExtension = str(frameNumber) + ".png"
  filename = bpy.path.basename(bpy.data.filepath)
  filename = os.path.splitext(filename)[0]
  if filename:
    fileNameFrameNumberExtension = filename + "." + frameNumberAndExtension
    filepath = os.path.join("//../comp/annotate.v008/", fileNameFrameNumberExtension)
    print ("Setting filepath to:",filepath)
    bpy.context.scene.render.filepath = filepath
    #//../comp/annotate.v005/annotate.v006.
