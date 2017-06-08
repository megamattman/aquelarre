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

def initialise_and_draw_widgets(frame_name, object_type, rows):
    add_widget_data_to_map(frame_name, data.get(frame_name), object_type)
    add_widgets_to_frame(gui_map.get(frame_name).get('frame'), gui_map.get(frame_name).get('widgets'), rows)

root = Tk()

char_frame = create_frames(root, 'characteristics', {"self_config": {'width':200, 'height':200}, "grid_config":{'row' : 0, 'column': 1}})
skill_frame = create_frames(root,'skills', {"self_config": {'width':200, 'height':200}, "grid_config":{'row' : 0, 'column': 2}})
arms_skills_frame = create_frames(root,'arms_skills', {"self_config": {'width':200, 'height':200}, "grid_config":{'row' : 1, 'column': 2}})
language_skills_frame = create_frames(root,'language_skills', {"self_config": {'width':200, 'height':200}, "grid_config":{'row' : 3, 'column': 2}})

gui_map = {
    'characteristics' : {
        'frame': char_frame
    },
    'skills' : {
        'frame': skill_frame
    },
    'language_skills' : {
        'frame': language_skills_frame
    },
    'arms_skills' : {
        'frame': arms_skills_frame
    }
}

initialise_and_draw_widgets('characteristics', aqCharacteristic, 7)
initialise_and_draw_widgets('skills', aqSkill, 7)
initialise_and_draw_widgets('arms_skills', aqSkill, 2)
initialise_and_draw_widgets('language_skills', aqSkill, 2)


root.mainloop()

