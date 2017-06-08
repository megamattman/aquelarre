# using Tkinter's Optionmenu() as a combobox
from pprint import pprint
try:
    # Python2
    from Tkinter import *
    from ttk import *
except ImportError:
    # Python3
    import tkinter as tk

from lib.aqWidget import *

import yaml

imported_data = {}
with open("data/AquallarreData.yaml", 'r') as stream:
    data = yaml.load(stream)

skills_data = data.get('skills', {})
language_skills_data = data.get('language_skills', {})
arms_skills_data = data.get('arms_skills', {})
kingdoms_data = data.get('kingdoms', {})
people_data = data.get('people', {})
professions_data = data.get('professions', {})
society_data = data.get('society', {})

kingdom_options    = sorted(kingdoms_data.keys())
people_options     = sorted(people_data.keys())
profession_options = sorted(professions_data.keys())

def create_frames (master, name, configs):
    new_frame = Labelframe(master, text=name, **configs.get('self_config', {}))
    new_frame.columnconfigure(0,weight=1)
    new_frame.rowconfigure(0, weight=1)
    new_frame.grid(**configs.get('grid_config',{}))
    #master.add(new_frame, text=name)
    return new_frame

def add_widget_data_to_map (frame_name, widget_data, widget_func):
    for widget_info in widget_data:
        new_entry = {'name' : widget_info.iterkeys().next(), 'widget' : widget_func, 'info' : widget_info.itervalues().next()}
        #new_entry.update(widget_info.itervalues().next())
        if 'widgets' not in gui_map[frame_name]:
            gui_map[frame_name]['widgets'] = []
        gui_map[frame_name]['widgets'].append(new_entry)

def add_widgets_to_frame (frame, widgets, rows):
    loc = {'row' : 0, 'column' : 0}
    for idx, widget in enumerate(widgets):
        new_widget = widget['widget'](widget.get('name'),frame, dict(loc), **widget['info'])
        widget['widget'] = new_widget
        #update location
        loc['row'] = (idx % rows) * len(new_widget.widgets)
        loc['column'] = (idx / rows) * len(new_widget.widgets)


root = Tk()

char_frame = create_frames(root, 'characteristics', {"self_config": {'width':200, 'height':200}, "grid_config":{'row' : 0, 'column': 1}})
skill_frame = create_frames(root,'skills', {"self_config": {'width':200, 'height':200}, "grid_config":{'row' : 0, 'column': 2}})


gui_map = {
    'characteristics' : {
        'frame': char_frame
    },
    'skills' : {
        'frame': skill_frame
    }
}

add_widget_data_to_map('characteristics', data.get('characteristics'), aqCharacteristic)
add_widgets_to_frame(gui_map.get('characteristics').get('frame'), gui_map.get('characteristics').get('widgets'), 7)
add_widget_data_to_map('skills', data.get('skills'), aqSkill)
add_widgets_to_frame(gui_map.get('skills').get('frame'), gui_map.get('skills').get('widgets'), 7)

#loc = {'row':0, 'column':0}
#for frame_name, contents in gui_map.items():
#    for widget in contents.get('widgets', []):
#        new_widget = widget['widget'](widget.get('name'),contents.get('frame'), dict(loc), min_val='0')
#        print "im here"
#        widget['widget'] = new_widget
#        loc['row'] += 1

#pprint (gui_map)
root.mainloop()



#allowed_classes = ['townssfolk', 'noble']
#current_class = ['townsfolk']
#match = [p_class for p_class in allowed_classes if p_class in current_class]
#if match:
#    print "boop"
#
#


#
#w = Spinbox(master, from_=0, to=10, state='readonly')
#w.pack()
#
#mainloop()

#def make_popup():
#
#    top = Toplevel()
#    top.title("About this application...")
#
#    msg = Message(top, text="bert")
#    msg.pack()
#
#    button = Button(top, text="Dismiss", command=top.destroy)
#    button.pack()
#
#master = Tk()
#
#w = Scale(master, from_=5, to=20)
#w.pack()
#
#w = Scale(master, from_=5, to=20, orient=HORIZONTAL)
#w.pack()
#
#
#
#
#button = Button(master, text="popup", command=make_popup)
#button.pack()
#
#mainloop()


#print "hello"
#
#bigdict = {
#    1 : 'a',
#    2 : 'a',
#    3 : 'b',
#    4 : 'b'
#}
#
#smalldict = {key: val for key, val in bigdict.items() if 'a' in val}
#print smalldict

#master = Tk()
#
#listbox = Listbox(master)
#listbox.pack()
#
#listbox.insert(END, "a list entry")
#
#for item in ["one", "two", "three", "four"]:
#    listbox.insert(END, item)
#
#b = Button(master, text="Delete",
#           command=lambda lb=listbox: listbox.delete(ANCHOR))
#
#b.pack()
#master.mainloop()

#def select():
#    sf = "value is %s" % var.get()
#    root.title(sf)
#    # optional
#    color = var.get()
#    root['bg'] = color
#
#root = Tk()
#mainframe = Frame(root, height=200, width=200, bg='blue')
#mainframe.grid(column=0, row=0, columnspan=4)
#mainframe.columnconfigure(0,weight=1)
#mainframe.rowconfigure(0, weight=1)
#
#subframe = Frame(root, width=20, height=200, bg='red')
#subframe.grid(column=0, row=2)
#subframe.columnconfigure(0,weight=1)
#subframe.rowconfigure(0, weight=1)
#
#for idx in range (4) :
#    l = Label (subframe, text="hello")
#    l.grid(column=0, row=idx)
#
#for idx in range (4) :
#    l = Label (mainframe, text="hello hello hello")
#    l.grid(column=idx, row=0)
#
#
##for child in mainframe.winfo_children():
##    child.grid_configure(padx=1, pady=1)
#
#root.mainloop()

#root = Tk()
## use width x height + x_offset + y_offset (no spaces!)
#root.geometry("%dx%d+%d+%d" % (330, 80, 200, 150))
#root.title("tk.Optionmenu as combobox")
#var = StringVar(root)
## initial value
#var.set('red')
#choices = ['red', 'green', 'blue', 'yellow','white', 'magenta']
#option = OptionMenu(root, var, *choices)
#option.pack(side='left', padx=10, pady=10)
#button = Button(root, text="check value slected", command=select)
#print button
#button.pack(side='left', padx=20, pady=10)

