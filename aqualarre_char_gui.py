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

#Layout map
frame_map = {
    'vitals'          : {
        'self_config' : {'padding' : "12 12 12 12" },
        'grid_config' : {'row' : 0, 'column': 0, 'sticky' : 'N, W, E, S'},
        'content_config' : {
            'kingdom' :{
                'label' : {
                    'grid_config' : {'row' : 0, 'column' : 0},
                    'self_config' : {'width' : 15, 'text' : 'kingdom'}
                },
                'options' : {
                    'grid_config' : {'row' : 0, 'column' : 1},
                    'self_config' : {'width' : 15}
                    }
            },
            'people' : {
                'label' : {
                    'grid_config' : {'row' : 0, 'column' : 2},
                    'self_config' : {'width' : 15. , 'text' : 'people'}
                },
                'options' : {
                    'grid_config' : {'row' : 0, 'column' : 3},
                    'self_config' : {'width' : 15}
                    }
            },
            'profession' : {
                'label' : {
                    'grid_config' : {'row' : 0, 'column' : 4},
                    'self_config' : {'width' : 15, 'text' : 'profession'}
                },
                'options' : {
                    'grid_config' : {'row' : 0, 'column' : 5},
                    'self_config' : {'width' : 25}
                }
            }
        }
    },
    #'skills'          : {
    #    'self_config' : {
    #        'row' : 0, 'column': 0, 'sticky' : 'N, W, E, S'
    #    }
    #},
    'characteristics' : {
        'grid_config' : {
            'row' : 1, 'column': 0, 'sticky' : 'N, W, E, S'
        }
    }
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
            print ("NO")
    return total

def pop (event):
    print ("aaaaf")
    print ("pressed", repr(event.char))

def create_frame_content(frame_name, name_list):
    frame_description = frame_map.get(frame_name)
    for idx, name in enumerate(name_list):
        new_content = {
            name :{
                'label' : {
                    'grid_config' : {'row' :  0 + (idx % 10), 'column' : 0 + ((idx / 10)*2)},
                    'self_config' : {'width' : 15, 'text' : name}
                    },
                 'entry' : {
                     'grid_config' : {'row' :  0 + ((idx % 10)), 'column' :  1 + ((idx / 10)*2)},
                     'self_config' : {'width' : 3}
                    }
                }
            }
        if 'content_config' not in frame_description.keys():
            frame_description['content_config'] = {}
        frame_description['content_config'].update(new_content)



def populate_frame(frame_name, configs):
    print frame_name
    frame = frame_map.get(frame_name).get('frame')
    pprint (configs.keys())
    for content_name , content_config in configs.items():
        print "content name:{}".format(content_name)
        content_data = characteristic_map.get(content_name)
        content_data['var'] = StringVar()
        #pprint(content_config)
        for content_type, content_configs in content_config.items():
            print "content_type {}".format(content_type)
            if 'options' in content_type:
                content_options = content_data.get('options', {})
                options_menu = OptionMenu(frame, content_data['var'],  content_options[0], *content_options)
                options_menu.configure(**content_configs.get('self_config', {}))
                options_menu.grid(**content_configs.get('grid_config', {}))
                characteristic_map['options_menu'] = options_menu
            if 'label' in content_type:
                label = Label(frame, **content_configs.get('self_config', {}))
                label.grid(**content_configs.get('grid_config', {}))
                content_data['label'] = label
            if 'entry' in content_type:
                entry = Entry (frame, textvariable=content_data['var'], **content_configs.get('self_config', {}))
                entry.grid(**content_configs.get('grid_config', {}))
                content_data['entry'] = entry

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

    create_frame_content('characteristics', characteristic_label_strings)

    #pprint (frame_map)
    #exit()

    for frame_name, configs in frame_map.items():
        print "populate"
        populate_frame(frame_name, configs.get('content_config', {}))

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


#    for key, val in frame_map.items():
#        for child in val['frame'].winfo_children():
#            child.grid_configure(padx=1, pady=1)
#
    #root.bind('<Return>', calculate)



    root.mainloop()
