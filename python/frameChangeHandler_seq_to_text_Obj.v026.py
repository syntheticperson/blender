import bpy
from bpy.app.handlers import persistent
import time

@persistent
def preRenderHandler(self):
  scene = bpy.data.scenes["Scene"]
  frame = scene.frame_current
  print("preRenderHandler: <======\nFrame ", frame)
#  frameChangeHandler(scene)

@persistent
def frameChangeHandler(scene):
  #scene = bpy.data.scenes["Scene"]
  frame = scene.frame_current
  print("frameChangeHandler: <======\nFrame ", frame)

#  print("Frame Change", frame)
  seq_all = bpy.data.scenes["Scene"].sequence_editor.sequences_all
  for s in seq_all:
      b = s
      bfs = b.frame_start
      print(b.name," frame_start:",b.frame_start)
      o = bpy.data.objects[b.name]
      print("object:",o)
      if frame < (b.frame_final_start - 1) or frame > (b.frame_final_end - 2):
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
# end of def seq_to_text(seq_all):

# convert all sequences to text objects
seq_all = bpy.data.scenes["Scene"].sequence_editor.sequences_all
t_o_a = seq_to_text(seq_all)

# add handlers
print("bpy.app.handlers.frame_change_pre.clear()")
bpy.app.handlers.frame_change_pre.clear()

print("bpy.app.handlers.frame_change_pre.append(frameChangeHandler)")
bpy.app.handlers.frame_change_pre.append(frameChangeHandler)

print("bpy.app.handlers.render_pre.clear()")
bpy.app.handlers.render_pre.clear()
print("bpy.app.handlers.render_pre.append(preRenderHandler)")
bpy.app.handlers.render_pre.append(preRenderHandler)
