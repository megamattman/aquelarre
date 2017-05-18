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


skills_data = data.get('skills', {})
language_skills_data = data.get('language_skills', {})
arm_skills_data = data.get('arm_skills', {})
kingdoms_data = data.get('kingdoms', {})
people_data = data.get('people', {})
professions_data = data.get('professions', {})
society_data = data.get('society', {})

kingdom_options    = sorted(kingdoms_data.keys())
people_options     = sorted(people_data.keys())
profession_options = sorted(professions_data.keys())

previous_profession = ""

#this should be derived from people
class_options = ['upper_nobility', 'lesser_nobility', 'burgher', 'townsfolk', 'peasant', 'slave']

frame_order = ['vitals', 'characteristics', 'skills']

def get_widget_var (characteristic):
    return characteristic_map[characteristic]['var']

def get_widget (characteristic, widget_type):
    return characteristic_map[characteristic][widget_type]

def update():
    #for label in characteristic_label_strings:
    #    print "{} = {}".format(label, characteristic_map[label]['var'].get())
    total_points = characteristic_map['total_points'].get('var')
    total_points.set( "Total points: {}".format(total_characteristics()))
    print total_points.get()

def clear():
    for _, val in characteristic_map.items():
        if 'int' in val.get('type', ''):
            val.get('var').set(0)
        else :
            val.get('var').set('')

def update_options_menu(target_label, base_list, restrictions):
    widget_to_modify = characteristic_map[target_label]['option_menu']
    widget_var = get_widget_var(target_label)
    widget_to_modify['menu'].delete(0, 'end')
    new_options = [option for option in base_list if option not in restrictions]
    for option in new_options:
        widget_to_modify['menu'].add_command(label=option, command=lambda v=option: widget_var.set(v))

def update_kingdom(_, kingdom_value):
    new_people = kingdoms_data.get(kingdom_value)['people']
    update_options_menu('people', new_people, [])


#Setting people can impact profession AND class
#Not going to support backwards gen i.e. people -> kingdom
def update_people(_, people_value):
    new_society = people_data.get(people_value)['society']
    base_list = society_data[new_society.lower()].get('class',[]).keys()
    characteristic_map.get('society')['var'].set(new_society)
    people_restricitons = people_data.get(people_value).get('restrictions',{})
    if people_restricitons:
        for key, val in people_restricitons.items():
            if 'profession' in key :
                base_list = profession_options
            update_options_menu(key, base_list, val)
    else:
        update_options_menu('class',base_list.keys(),people_restricitons.get('class',[]))

# when updating classes find society base list and then remove people
def update_class(_, class_value):
    current_society = get_widget_var('society').get().lower()
    current_class = class_value.lower()
    try:
        #class and society determine profession list
        allowed_list = society_data.get(current_society).get('class').get(class_value)
        exlcusion_list = [exclusion for exclusion in profession_options if exclusion not in allowed_list]
        update_options_menu('profession', profession_options, exlcusion_list)
    except Exception as e :
        print e
        pprint (society_data.get(current_society))
        print "{} {} bad combination when filtering classes".format(current_society, current_class)


def update_profession(_, profession_value):
    #unset any changes made by previous professions
    #if previous_profession != "":
    #    for skill in previous_profession.get('primary_skills'):
    #        skill_label = get_widget(skill, 'label')
    #        skill_label.configure(background='grey')
    new_profession = professions_data[profession_value]
    #previous_profession = new_profession
    for skill in new_profession.get('primary_skills'):
        try:
            skill_label = get_widget(skill, 'label')
            skill_label.configure(background='green')
        except:
            print "Not a valid skill {}".format(skill)

def event_handler (_, widget_name):
    widget_function_mapping = {
    'kingdom' : update_kingdom,
    'people' : update_people,
    'class'  : update_class,
    'profession' : update_profession,
    }
    widget_data = characteristic_map.get(widget_name)
    widget_value = widget_data['var'].get()
    if widget_value != '':
        widget_function_mapping[widget_name](widget_data, widget_value)


#This map should contain data and pointers to the widgets
characteristic_map = {
    'character_name': {'frame': 'vitals'},
    'kingdom'       : {'frame': 'vitals', 'options': kingdom_options},
    'people'        : {'frame': 'vitals', 'options': people_options},
    'profession'    : {'frame': 'vitals', 'options': profession_options},
    'class'         : {'frame': 'vitals', 'options': class_options},
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
        'grid_config' : {'row' : 0, 'column': 0, 'sticky' : 'N, W'},
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
    }
}

#import layout data from yaml file
with open("data/layout_data.yaml",'r') as stream:
    layout_data = yaml.load(stream)

frame_map.update(layout_data)
characteristic_map.update(skills_data)

def total_characteristics():
    total = 0
    characteristic_strings = [key for key, val in characteristic_map.items() if 'characteristics' in val.get('frame','')]
    for label in characteristic_strings:
        value = get_widget_var(label).get()
        try:
            total += value
        except:
            print ("NO")
    return total

def pop (*args):
    for key, val in characteristic_map.items():
        try:
            value = val['var'].get()
            #if value:
            #    print "{} : {}".format(key, value)
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
                    'self_config' : {'width' : len(name)+2, 'text' : name}
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
        return OptionMenu(frame, content_data['var'],  'select', *content_options)
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
            def focus_out_handler (event, name=content_name) :
                return event_handler(event, name)

            def trace_handler (a,b,c, name=content_name) :
                return event_handler(None, name)
            try:
                if 'textvariable' in content_configs.get('self_config').keys():
                    content_configs.get('self_config')['textvariable'] = content_data['var']
            except:
                print content_name
                pprint (content_configs)
                exit()

            if 'option_menu' in content_type:
                content_data['var'].trace("w", trace_handler)
            elif 'entry' in content_type:
                new_content.bind('<FocusOut>', focus_out_handler)

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

    create_frame_content('language_skills', sorted(language_skills_data), 1,1)
    create_frame_content('arm_skills', sorted(arm_skills_data), 1,1)
    create_frame_content('characteristics', characteristic_label_strings, 7, 7)
    create_frame_content('derived', derived_label_strings, 7, 7)
    create_frame_content('skills', sorted(skills_data), 7, 7)

    for frame_name, configs in frame_map.items():
    #for frame_name in frame_order:
        print "populate"
        populate_frame(frame_name, configs.get('content_config', {}))

    for key, val in frame_map.items():
        for child in val['frame'].winfo_children():
            child.grid_configure(padx=1, pady=1)

    root.mainloop()
