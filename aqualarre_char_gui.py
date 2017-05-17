# #!/usr/bin/python
import yaml
try:
	from Tkinter import *
	from ttk import *
except:
	from tkinter import *
	#from ttk import *

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

frame_order = ['vitals', 'characteristics', 'skills']

def update():
    #for label in characteristic_label_strings:
    #    print "{} = {}".format(label, characteristic_map[label]['var'].get())
    total_points = characteristic_map['total_points'].get('var')
    total_points.set( "Total points: {}".format(total_characteristics()))
    print total_points.get()

def clear():
    for key, val in characteristic_map.items():
        if 'int' in val.get('type', ''):
            val.get('var').set(0)
        else :
            val.get('var').set('')


def event_handler (event, widget_name):
    print widget_name


#This map should contain data and pointers to the widgets
characteristic_map = {
    'character_name': {'frame': 'vitals'},
    'kingdom'       : {'frame': 'vitals', 'options': kingdom_options},
    'people'        : {'frame': 'vitals', 'options': people_options},
    'profession'    : {'frame': 'vitals', 'options': profession_options},
    'Strength'      : {'frame': 'characteristics', 'Name' : 'Strength',      'value' :  5, 'type' : 'int'},
    'Agility'       : {'frame': 'characteristics', 'Name' : 'Agility',       'value' :  5, 'type' : 'int'},
    'Dexterity'     : {'frame': 'characteristics', 'Name' : 'Dexterity',     'value' :  5, 'type' : 'int'},
    'Resistance'    : {'frame': 'characteristics', 'Name' : 'Resistance',    'value' : 10, 'type' : 'int'},
    'Perception'    : {'frame': 'characteristics', 'Name' : 'Perception',    'value' :  5, 'type' : 'int'},
    'Communication' : {'frame': 'characteristics', 'Name' : 'Communication', 'value' :  5, 'type' : 'int'},
    'Culture'       : {'frame': 'characteristics',                           'value' :  5, 'type' : 'int'},
    'IRR'           : {'frame': 'derived',                           'value' :  50, 'type' : 'int'},
    'RR'            : {'frame': 'derived',                           'value' :  50, 'type' : 'int'},
    'luck'          : {'frame': 'derived',                           'value' :  15, 'type' : 'int'},
    'Appearance'    : {'frame': 'derived',                           'value' :  15, 'type' : 'int'}
}

#Layout map
frame_map = {
    'controls'        :{
        'self_config' : {'padding' : "8 0 0 0" },
        'grid_config' : {'row' : 0, 'column': 0, 'sticky' : 'N, W'},#'columnspan' : 2},
        'content_config' :{
            'clear' : {
                'button' : {
                    'grid_config' : {'row' : 0, 'column' : 0, 'sticky' : 'N, W'},
                    'self_config' : {'width' : 15, 'text' : 'clear' , 'command' : clear }
                }
            },
            'update' : {
                'button' : {
                    'grid_config' : {'row' : 0, 'column' : 1, 'sticky' : 'N, W'},
                    'self_config' : {'width' : 15, 'text' : 'update' , 'command' : update }
                }
            },
            'total_points' : {
                'label' : {
                    'grid_config' : {'row' : 0, 'column' : 2, 'sticky' : 'N, W'},
                    'self_config' : {'width' : 15, 'text' : 'Total Points', 'textvariable' : None}
                }
            }
        }
    },
    'vitals'          : {
        'self_config' : {'padding' : "8 0 0 0" },
        'grid_config' : {'row' : 1, 'column': 0, 'sticky' : 'N, W','columnspan' : 3},
        'content_config' : {
            'character_name' : {
                'label' : {
                    'grid_config' : {'row' : 0, 'column' : 0, 'sticky' : 'N, W'},
                    'self_config' : {'width' : 15, 'text' : 'Character name'}
                },
                'entry' : {
                    'grid_config' : {'row' : 0, 'column' : 1, 'sticky' : 'N, W'},
                    'self_config' : {'width' : 15}
                    }
            },
            'kingdom' :{
                'label' : {
                    'grid_config' : {'row' : 0, 'column' : 2, 'sticky' : 'N, W'},
                    'self_config' : {'width' : 15, 'text' : 'Kingdom'}
                },
                'option_menu' : {
                    'grid_config' : {'row' : 0, 'column' : 3, 'sticky' : 'N, W'},
                    'self_config' : {'width' : 15}
                }
            },
            'people' : {
                'label' : {
                    'grid_config' : {'row' : 1, 'column' : 0, 'sticky' : 'N, W'},
                    'self_config' : {'width' : 15. , 'text' : 'People'}
                },
                'option_menu' : {
                    'grid_config' : {'row' : 1, 'column' : 1, 'sticky' : 'N, W'},
                    'self_config' : {'width' : 15}
                }
            },
            'profession' : {
                'label' : {
                    'grid_config' : {'row' : 1, 'column' : 2, 'sticky' : 'N, W'},
                    'self_config' : {'width' : 15, 'text' : 'Profession'}
                },
                'option_menu' : {
                    'grid_config' : {'row' : 1, 'column' : 3, 'sticky' : 'N, W'},
                    'self_config' : {'width' : 25}
                }
            }
        }
    },
    'skills'          : {
        'grid_config' : {
            'row' : 2, 'column': 2, 'sticky' : 'E'
        }
    },
    'characteristics' : {
        'grid_config' : {
            'row' : 2, 'column': 0, 'sticky' : 'W'
        }
    },
    'derived' : {
        'grid_config' : {
            'row' : 2, 'column': 1, 'sticky' : 'W'
        }
    }
    #'vitals' : {'row' : 0, 'column': 0, 'width' : 0, 'height': 0},
    #'vitals' : {'row' : 0, 'column': 0, 'width' : 0, 'height': 0},
}

characteristic_map.update(skills)

def total_characteristics():
    total = 0
    strings_to_total = [
    'Strength',
    'Agility',
    'Dexterity',
    'Resistance',
    'Perception',
    'Communication',
    'Culture'
    ]
    for label in strings_to_total:
        value = characteristic_map[label]['var'].get()
        try:
            total += value
        except:
            print ("NO")
    return total

def pop (*args):
    for key, val in characteristic_map.items():
        try:
            value = val['var'].get()
            if value:
                print "{} : {}".format(key, value)
        except:
            print "failed to get value of {}".format(key)

def pip (event):
    print "pip"
    pprint (event)
    print event.widget

def get_tk_var (var_type) :
    if 'int' in var_type:
        return IntVar()
    else:
        return StringVar()

def create_frame_content(frame_name, name_list, rows, cols):
    frame_description = frame_map.get(frame_name)
    for idx, name in enumerate(name_list):
        new_content = {
            name :{
                'label' : {
                    'grid_config' : {'row' :  0 + (idx % rows), 'column' : 0 + ((idx / cols)*2), 'sticky' : "W"},
                    'self_config' : {'width' : 15, 'text' : name}
                    },
                 'entry' : {
                     'grid_config' : {'row' :  0 + ((idx % rows)), 'column' :  1 + ((idx / cols)*2), 'sticky' : "W"},
                     'self_config' : {'width' : 3, 'textvariable' : None}
                    }
                }
            }
        if 'content_config' not in frame_description.keys():
            frame_description['content_config'] = {}
        frame_description['content_config'].update(new_content)

def get_empty_widget (content_type, frame, content_data):
    if 'option_menu' in content_type :
        content_options = content_data.get('options', {})
        return OptionMenu(frame, content_data['var'],  content_options[0], *content_options)
    if 'button' in content_type :
        return Button(frame)
    if 'label' in content_type:
        return Label(frame)
    if 'entry' in content_type:
        return Entry(frame)


def populate_frame(frame_name, configs):
    print "populating: {}".format(frame_name)
    frame = frame_map.get(frame_name).get('frame')
    for content_name , content_config in configs.items():
        if content_name not in characteristic_map.keys():
            characteristic_map[content_name] = {}
        content_data = characteristic_map.get(content_name)
        content_data['var'] = get_tk_var(content_data.get('type', ''))
        content_data['var'].set(content_data.get('value', ''))

        for content_type, content_configs in content_config.items():
            new_content = get_empty_widget(content_type, frame, content_data)
            def handler (event, name=content_name) :
                return event_handler(event, name)

            if 'textvariable' in content_configs.get('self_config').keys():
                content_configs.get('self_config')['textvariable'] = content_data['var']

            if 'option_menu' in content_type:
                content_data['var'].trace("w", pop)
            elif 'entry' in content_type:
                new_content.bind('<FocusOut>', handler)

            if new_content is not None :
                new_content.grid(**content_configs.get('grid_config', {}))
                new_content.configure(**content_configs.get('self_config', {}))
                content_data[content_type] = new_content

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
    characteristic_label_strings = [key for key, val in characteristic_map.items() if 'characteristics' in val.get('frame','')]
    derived_label_strings = [key for key, val in characteristic_map.items() if 'derived' in val.get('frame','')]

    create_frame_content('characteristics', characteristic_label_strings, 7, 7)
    create_frame_content('derived', derived_label_strings, 7, 7)
    create_frame_content('skills', skills, 7, 7)

    #pprint (frame_map)
    #exit()

    for frame_name, configs in frame_map.items():
    #for frame_name in frame_order:
        print "populate"
        populate_frame(frame_name, configs.get('content_config', {}))
        #populate_frame(frame_name, frame_map.get(frame_name).get('content_config', {}))

        #if 'characteristics' in frame_name:
        #    draw_characteristics(frame, name , configs)
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

    #root.bind('<Return>', calculate)



    root.mainloop()
