# using Tkinter's Optionmenu() as a combobox
from pprint import pprint
try:
    # Python2
    from Tkinter import *
    from ttk import *
except ImportError:
    # Python3
    import tkinter as tk

import yaml

from lib.aqWidget import AqCharacteristic, AqSkill, AqVital


imported_data = {}
with open("data/AquallarreData.yaml", 'r') as stream:
    data = yaml.load(stream)

# import layout data from yaml file
with open("data/layout_data.yaml",'r') as stream:
    layout_data = yaml.load(stream)



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


def create_frames(master, name, configs):
    new_frame = Labelframe(master, text=name, **configs.get('self_config', {}))
    new_frame.columnconfigure(0,weight=1)
    new_frame.rowconfigure(0, weight=1)
    new_frame.grid(**configs.get('grid_config',{}))
    return new_frame


def add_widget_data_to_map (frame_name, widget_data, widget_func):
    for widget_info in widget_data:
        new_entry = {'name' : widget_info.iterkeys().next(), 'widget' : widget_func, 'info' : widget_info.itervalues().next()}
        if 'widgets' not in gui_map[frame_name]:
            gui_map[frame_name]['widgets'] = []
        gui_map[frame_name]['widgets'].append(new_entry)


def add_widgets_to_frame(frame, widgets, rows, start_loc):
    loc = dict(start_loc)
    for idx, widget in enumerate(widgets, 1):
        new_widget = widget['widget'](widget.get('name'), frame, dict(loc), **widget['info'])
        widget['widget'] = new_widget
        #update location
        loc['row'] = idx % rows
        loc['column'] = ((idx / rows) * (len(new_widget.widgets)))


def initialise_and_draw_widgets(frame_name, object_type, rows, start_loc):
    add_widget_data_to_map(frame_name, data.get(frame_name), object_type)
    add_widgets_to_frame(gui_map.get(frame_name).get('frame'), gui_map.get(frame_name).get('widgets'), rows, start_loc)


gui_map = {}

if __name__ == '__main__':
    root = Tk()

    for name, configs in layout_data.items():
        gui_map[name] = {}
        gui_map[name]['frame'] = create_frames(root, name, configs)

    default_loc_map = {'row': 0, 'column': 0}
    initialise_and_draw_list = [
        ('vitals', AqVital, 1, default_loc_map),
        ('characteristics', AqCharacteristic, 8, default_loc_map),
        ('skills', AqSkill, 8, default_loc_map),
        ('arms_skills', AqSkill, 2, default_loc_map),
        ('language_skills', AqSkill, 2, default_loc_map),
    ]
    for item in initialise_and_draw_list:
        print item[0]
        initialise_and_draw_widgets(*item)

    root.mainloop()

