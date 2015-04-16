import bpy
from bpy.app.handlers import persistent

@persistent
def frameChangeHandler(scene):
  scene = bpy.data.scenes["Scene"]
  frame = scene.frame_current
  print("Frame Change", frame)
  seq_all = bpy.data.scenes["Scene"].sequence_editor.sequences_all
  for s in seq_all:
      b = s
      bfs = b.frame_start
      print(b.name," frame_start:",b.frame_start)
      o = bpy.data.objects[b.name]
      print("object:",o)
      if frame < b.frame_final_start or frame > b.frame_final_end:
          o.hide = True
          o.hide_render = True
      else:
          o.hide = False
          o.hide_render = False
      if o.data.body == 'Scene':
          print ("o.data.body = 'Scene'")
          o.hide = True
          o.hide_render = True
def seq_to_text(seq_all):
#    seq_all = scenes['Scene'].sequence_editor.sequences_all
    y = 0
    t_o = []
    for s in seq_all:
      s_n = s.name
      bpy.ops.object.text_add(radius=0.5, view_align=False, enter_editmode=False, location=(-3, y, 0), rotation=(0, 0, 0))
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

seq_all = bpy.data.scenes["Scene"].sequence_editor.sequences_all
t_o_a = seq_to_text(seq_all)
bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(frameChangeHandler)

# for currentFrame from start frame to end frame
# getStripStartFrame,endFrame,offSet
# if currentFrame < stripStartFrame then object.hide = True

bpy.app.handlers.load_post.clear()
bpy.app.handlers.load_post.append(frameChangeHandler)
