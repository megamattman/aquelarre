# #!/usr/bin/python
import yaml
from Tkinter import *
from ttk import *
from pprint import pprint

#import aquallarre data
imported_data = {}
with open("data/AquallarreData.yaml", 'r') as stream:
    data = yaml.load(stream)


skills = data.get('skills', {})
kingdoms = data.get('kingdoms', {})
people = data.get('people', {})
professions = data.get('professions', {})

kingdom_options    = sorted([kingdom for kingdom in kingdoms.keys()])
people_options     = sorted([option for option in people.keys()])
profession_options = sorted([option for option in professions.keys()])

#Layout map
frame_map = {
    'vitals'          : {
        'self_config' : {'height' : 200, 'width' : 200, 'padding' : "12 12 12 12" },
        'grid_config' : {'row' : 0, 'column': 0, 'sticky' : 'N, W, E, S'},
        'content_config' : {
            'kingdom_label'           : {'row' : 0, 'column' : 0},
            'kingdom_options'         : {'row' : 0, 'column' : 1},
            'people_label'            : {'row' : 0, 'column' : 2},
            'people_options'          : {'row' : 0, 'column' : 3},
            'profession_label'        : {'row' : 0, 'column' : 4},
            'profession_options'      : {'row' : 0, 'column' : 5},
        }
    },
    #'skills'          : {
    #    'self_config' : {
    #        'row' : 0, 'column': 0, 'sticky' : 'N, W, E, S'
    #    }
    #},
    #'characteristics' : {
    #    'self_config' : {
    #        'row' : 0, 'column': 0, 'sticky' : 'N, W, E, S'
    #    }
    #}
    #'vitals' : {'row' : 0, 'column': 0, 'width' : 0, 'height': 0},
    #'vitals' : {'row' : 0, 'column': 0, 'width' : 0, 'height': 0},
}

#Allow accessing the elements of the form through a single map
characteristic_map = {
    'kingdom'       : {'frame': 'vitals', 'options': kingdom_options},
    'people'        : {'frame': 'vitals', 'options': people_options},
    'profession'    : {'frame': 'vitals', 'options': profession_options},
    'Strength'      : {'frame': 'characteristics', 'Name' : 'Strength',      'value' :  5},
    'Agility'       : {'frame': 'characteristics', 'Name' : 'Agility',       'value' :  5},
    'Dexterity'     : {'frame': 'characteristics', 'Name' : 'Dexterity',     'value' :  5},
    'Resistance'    : {'frame': 'characteristics', 'Name' : 'Resistance',    'value' : 10},
    'Perception'    : {'frame': 'characteristics', 'Name' : 'Perception',    'value' :  5},
    'Communication' : {'frame': 'characteristics', 'Name' : 'Communication', 'value' :  5},
    'Culture'       : {'frame': 'characteristics', 'Name' : 'Culture',       'value' :  5},

}
#ordered list used for displaying
characteristic_label_strings = [
    'Strength',
    'Agility',
    'Dexterity',
    'Resistance',
    'Perception',
    'Communication',
    'Culture'
]

#ordered list used for diplaying
vitals_strings = [
    'kingdom',
    'people',
    'profession'
]


def update():
    #for label in characteristic_label_strings:
    #    print "{} = {}".format(label, characteristic_map[label]['var'].get())
    total_points=StringVar()
    total_points.set( "Total points: {}".format(total_characteristics()))
    Label(mainframe, text=total_points.get()).grid(column=6,row=1,sticky=(E))
    characteristic_map['kingdom']['label'].configure(background='blue')
    #characteristic_map['Strength']['label'].background = 'blue'

def total_characteristics():
    total = 0
    for label in characteristic_label_strings:
        value = characteristic_map[label]['var'].get()
        try:
            total += value
        except:
            print "NO"
    return total

def pop (event):
    print "aaaaf"
    print "pressed", repr(event.char)

def draw_vitals(frame, configs):
    for vitals in vitals_strings:
        stored_vitals = characteristic_map.get(vitals)
        stored_vitals['var'] = StringVar()
        options = stored_vitals['options']
        for name, grid_config in configs.items():
            if vitals in name:
                if 'options' in name:
                    options_menu = OptionMenu(frame, stored_vitals['var'],  options[0], *options)
                    options_menu.grid(**grid_config)
                    characteristic_map['options_menu'] = options_menu
                if 'label' in name:
                    label = Label(frame, text=vitals.title())
                    label.grid(**grid_config)
                    stored_vitals['label'] = label


def create_frames (master, name, configs):
    new_frame = Frame(master, **configs.get('self_config', {}))
    new_frame.columnconfigure(0,weight=1)
    new_frame.rowconfigure(0, weight=1)
    new_frame.grid(**configs.get('grid_config',{}))
    frame_map[name]['frame'] = new_frame

if __name__ == "__main__":
    #Place vitals

    root = Tk()

    root.title("Aqualarre Character sheet")

    for name, configs in frame_map.items():
        create_frames(root, name, configs)

    pprint (frame_map)

    for frame_name, configs in frame_map.items():
        frame = configs.get('frame')
        if 'vitals' in frame_name:
            print "drawing vitals"
            draw_vitals(frame, configs)
#        if 'characteristics' in frame_name:
#            draw_characteristics(frame, name , configs)
#        if 'skills' in fame_name
#    #Place characteristic labels and entries
#    for idx, label_string in enumerate (characteristic_label_strings):
#        characteristic_map[label_string]['var'] = IntVar()
#        label_row = layout_map['characteristics_labels']['row'] + idx
#        label_col = layout_map['characteristics_labels']['col']
#        entry_col = layout_map['characteristics_entries']['col']
#        entry_row = layout_map['characteristics_entries']['row'] +idx
#        characteristic_map[label_string]['label'] = Label(mainframe, text=label_string).grid(column=label_col,row=label_row,sticky=(W))
#        characteristic_map[label_string]['entry'] = Entry(mainframe, width=3, textvariable=characteristic_map[label_string]['var']).grid(column=entry_col, row=entry_row,sticky=(W))
#
#    #Place skill label and entries
#    for idx, skill in enumerate(skills):
#        #assumes {skill_name : {characteristic : XXX}}
#        label_string, _ = skill.items()[0]
#        skill['var'] = IntVar()
#        label_row = layout_map['skills_labels']['row'] + idx % 10
#        label_col = layout_map['skills_labels']['col'] + ((idx / 10)*2)
#        entry_col = layout_map['skills_entries']['col'] + ((idx / 10)*2)
#        entry_row = layout_map['skills_entries']['row'] + idx % 10
#        skill['label'] = Label(mainframe, text=label_string).grid(column=label_col,row=label_row,sticky=(E))
#        skill['entry'] = Entry(mainframe, width=3, textvariable=skill['var']).grid(column=entry_col, row=entry_row,sticky=(E))
#
#    total_points=StringVar()
#    total_points.set( "{}".format(total_characteristics()))
#
#
#    Button(mainframe, text="Update", command=update).grid(column=0,row=0, sticky=(N, E))
#    #feet = StringVar()
    #meters = StringVar()
    #
    #feet_entry = Entry(mainframe, width=7, textvariable=feet)
    #feet_entry.grid(column=2, row=1, sticky=(W, E))
    #
    #Label(mainframe, textvariable=meters).grid(column=2,row=2,sticky=(W, E))
    #Button(mainframe, text="Calculate", command=calculate).grid(column=3,row=3, sticky=E)
    #
    #Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
    #Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=W)
    #Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
    #
    #options = ["one", "two", "three"]
    #variable = StringVar(mainframe)
    #
    #OptionMenu(mainframe, variable,  options[0], *options)


    for key, val in frame_map.items():
        for child in val['frame'].winfo_children():
            child.grid_configure(padx=1, pady=1)
#
    #root.bind('<Return>', calculate)



    root.mainloop()
