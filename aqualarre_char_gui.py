# #!/usr/bin/python
import yaml
try:
    from Tkinter import *
    from ttk import *
    print "did this one"
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
arms_skills_data = data.get('arms_skills', {})
kingdoms_data = data.get('kingdoms', {})
people_data = data.get('people', {})
professions_data = data.get('professions', {})
society_data = data.get('society', {})

kingdom_options    = sorted(kingdoms_data.keys())
people_options     = sorted(people_data.keys())
profession_options = sorted(professions_data.keys())

previous_profession = ""

character_data = {}

#this should be derived from people
class_options = ['upper_nobility', 'lesser_nobility', 'burgher', 'townsfolk', 'peasant', 'slave']

frame_order = ['vitals', 'characteristics', 'skills']

def get_widget_var (characteristic):
    return characteristic_map[characteristic]['var']

def get_widget (characteristic, widget_type):
    return characteristic_map[characteristic][widget_type]

def names_by_frame(frame_name):
    return [key for key, val in characteristic_map.items() if frame_name in val.get('frame','')]

def get_subdict(big_dict, search_filter, element):
    sub_dict = {}
    for key, val in big_dict.items():
        if element in val.keys():
            if search_filter in val.get(element):
                sub_dict.update({key:val})
    return sub_dict

text_exceptions = {'RR':'RR', 'IRR':'IRR', 'LP':'LP'}
def beautify_text (text):
    return text_exceptions.get(text,text.replace('_', ' ').title())

def debeautify_text (text):
    return text_exceptions.get(text,text.replace(' ', '_').lower())

def update_widget (characteristic, widget_type, **config):
    widget = get_widget(characteristic, widget_type)
    widget.config(**config)

def update_widget_list(widget_list, widget_type, **config):
    for widget in widget_list:
        try :
            update_widget(widget, widget_type, **config)
        except:
            print "BAD widget combination {} {}".format(widget, widget_type)
            continue

def ordered_list_from_dict(big_dict, order_element):
    return [key for key, _ in sorted(big_dict.items(), key= lambda kv: kv[1].get(order_element,99))]


def filter_list (base_list, exclusion_list):
    return [item for item in base_list if item not in exclusion_list]

def derive_skill_list_from_requirements(skill_type, requirements):
    data_map = {
    'language_skills' : language_skills_data,
    'arms_skills'     : arms_skills_data
    }
    skill_data = data_map[skill_type]
    #no requirements, return entire skill list
    if not requirements:
        return skill_data.keys()
    output_list = []
    for requirement_key, requirement_values in requirements.get('requirements', {}).items():
        for item, data in skill_data.items():
            if [data_item for data_item in data.get(requirement_key,[]) if data_item in requirement_values]:
                output_list.append(item)
            else :
                if item in output_list:
                    output_list.remove(item)

    return output_list

#return two lists, a list of skills and a list of selections
def seperate_skills_from_selections(skill_list):
    selection_list = []
    output_skills = []
    for skill in skill_list:
        if type(skill) is type (dict()):
            selection_list.append(skill)
            continue
        output_skills.append(skill)

    final_selection_list = []
    for skill_selection in selection_list:
        for skills_type, requirement_map in skill_selection.items():
            final_selection_list.append(derive_skill_list_from_requirements(skills_type, requirement_map))

    for idx, skill_list in enumerate(final_selection_list):
        if len(skill_list) == 1:
            output_skills.append(skill_list[0])
            del skill_list[0]
        else:
            skill_list = filter_list(skill_list, output_skills)
            if 'skills' in character_data.keys() and 'primary_skills' in character_data.get('skills').keys():
                skill_list = filter_list(skill_list, character_data.get('skills').get('primary_skills'))
                final_selection_list[idx] = skill_list

    return output_skills, final_selection_list

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
    new_options = filter_list(base_list, restrictions)
    for option in new_options:
        widget_to_modify['menu'].add_command(label=beautify_text(option), command=lambda v=option: widget_var.set(v))

def update_kingdom(_, kingdom_value):
    new_people = kingdoms_data.get(kingdom_value)['people']
    update_options_menu('people', new_people, [])

#Setting people can impact profession AND class
#Not going to support backwards gen i.e. people -> kingdom
def update_people(_, people_value):
    new_society = people_data.get(people_value)['society']
    base_list = ordered_list_from_dict(society_data[new_society.lower()].get('class',{}), 'order')
    #base_list = sorted(society_data[new_society.lower()].get('class',{}).items(), key= lambda kv: kv[1].get('order',99))]
    get_widget_var('society').set(new_society)
    people_restricitons = people_data.get(people_value).get('restrictions',{})
    if people_restricitons:
        for key, val in people_restricitons.items():
            if 'profession' in key :
                base_list = profession_options
            update_options_menu(key, base_list, val)
    else:
        update_options_menu('class',base_list,people_restricitons.get('class',[]))

# when updating classes find society base list and then remove people
def update_class(_, class_value):
    current_society = debeautify_text(get_widget_var('society').get())
    current_class = debeautify_text(class_value)
    try:
        #class and society determine profession list
        allowed_list = society_data.get(current_society).get('class').get(class_value).get('professions')
        exlcusion_list = [exclusion for exclusion in profession_options if exclusion not in allowed_list]
        update_options_menu('profession', profession_options, exlcusion_list)
    except Exception as e :
        print e
        print "{} {} bad combination when filtering professions".format(current_society, current_class)

def mark_proffesion_skills (skill_type, profession):
    skill_type_config = {
        'primary' : {
            'label' : 'primary_skills',
            'select': 'primary_selections',
            'color' : 'green'
        },
        'secondary' : {
            'label' : 'secondary_skills',
            'select': 'secondary_selections',
            'color' : 'yellow'
        }
    }
    config = skill_type_config.get(skill_type)
    skill_list, skill_selections = seperate_skills_from_selections(profession.get(config.get('label')))
    character_data['skills'][config.get('label')] = skill_list
    character_data['skills'][config.get('select')] = skill_selections
    update_widget_list(skill_list, 'label', background=config.get('color'))

def reset_profession_changes():
    update_widget_list(skills_data.keys(), 'label', background='SystemButtonFace')
    update_widget_list(arms_skills_data.keys(), 'label', background='SystemButtonFace')
    update_widget_list(language_skills_data.keys(), 'label', background='SystemButtonFace')
    update_widget_list(names_by_frame('characteristics'), 'label', background='SystemButtonFace')
    characteristics = names_by_frame('characteristics')
    for characteristic in characteristics:
        characteristic_data = characteristic_map.get(characteristic)
        characteristic_data.get('var').set(characteristic_data.get('value'))


def update_profession(_, profession_value):
    new_profession = professions_data[profession_value]
    #get skill list keeping in mind slection options
    reset_profession_changes()

    if 'skills' not in character_data.keys():
        character_data['skills'] = {}

    mark_proffesion_skills('primary', new_profession)
    mark_proffesion_skills('secondary', new_profession)

    if character_data['skills']['primary_selections']:
        update_widget_list(character_data['skills']['primary_selections'][0], 'label', background='grey')
    elif character_data['skills']['secondary_selections']:
        update_widget_list(character_data['skills']['secondary_selections'][0], 'label', background='grey')

    try :
        for characteristic, val in new_profession.get('minimum_characteristics', {}).items():
            get_widget_var(characteristic).set(val)
            update_widget(characteristic, 'label', background='red')
    except:
        print "no minimum characteristics for {}".format(profession_value)

    characteristic_update("","")

def set_skills (skill_data):
    characteristic_entries = get_subdict(characteristic_map, 'characteristics', 'frame')
    for skill, data in skill_data.items():
        skill_widget = get_widget(skill, 'label')
        skill_var = get_widget_var(skill)
        multiplier = 1
        widget_color = str(skill_widget.cget('background'))
        if 'green' in widget_color:
            multiplier = 3
        try:
            skill_var.set(characteristic_entries.get(data['characteristic']).get('var').get() * multiplier)
        except Exception as e:
            print e

def update_derived (characteristic_data):
    pass

# sets skills to value based on characteristic
# doesn't account for user made changes'
def characteristic_update (characteristic_data, _):
    update_derived(characteristic_data)
    set_skills(skills_data)
    set_skills(arms_skills_data)


def update_selections(selection_skill_list, selected_skill_list, color, skill_type):
    skill_type_mapping = {
        'primary' : 'secondary',
        'secondary' : 'primary'
    }
    character_skills = character_data['skills']["{}_skills".format(skill_type_mapping.get(skill_type))]
    skill_to_update = filter_list(selection_skill_list, selected_skill_list)
    skill_to_update = filter_list(skill_to_update, character_skills)
    update_widget_list(skill_to_update, 'label', background=color)

def select_skill(widget_data, _):
    if 'grey' in str(widget_data['label']['background']):
        background_color = 'grey'
        skill_type = ""
        if character_data.get('skills').get('primary_selections'):
            print "primary selection"
            background_color = 'green'
            skill_type = 'primary'
        elif character_data.get('skills').get('secondary_selections'):
            print 'secondary selection'
            background_color = 'yellow'
            skill_type = 'secondary'

        widget_data['label'].configure(background=background_color)
        skill_text = debeautify_text(widget_data['label'].cget('text'))
        selected_skill_list = character_data.get('skills').get('{}_skills'.format(skill_type))
        selected_skill_list.append(skill_text)

        selection_skill_list = character_data.get('skills').get('{}_selections'.format(skill_type))[0]
        selection_skill_list.remove(skill_text)

        update_selections(selection_skill_list, selected_skill_list, 'SystemButtonFace', skill_type)
        del character_data.get('skills').get('{}_selections'.format(skill_type))[0]
        next_selection_skill_list = []

        if character_data.get('skills').get('{}_selections'.format(skill_type)):
            next_selection_skill_list = character_data.get('skills').get('{}_selections'.format(skill_type))[0]
        elif 'primary' in skill_type and character_data.get('skills').get('secondary_selections'):
            next_selection_skill_list = character_data.get('skills').get('secondary_selections')[0]

        if next_selection_skill_list:
            print "problem after here"
            update_selections(next_selection_skill_list, selected_skill_list, 'grey', skill_type)


def event_handler (_, widget_name):
    widget_function_mapping = {
    'kingdom'        : update_kingdom,
    'people'         : update_people,
    'class'          : update_class,
    'profession'     : update_profession,
    'characteristic' : characteristic_update,
    'skill_label'    : select_skill
    }
    widget_data = characteristic_map.get(widget_name)
    widget_value = widget_data['var'].get()
    if widget_value != '':
        if widget_name in names_by_frame('characteristics'):
            widget_name = 'characteristic'
        elif widget_name in names_by_frame('skills'):
            widget_name = 'skill_label'
        widget_function_mapping[widget_name](widget_data, widget_value)


#This map should contain data and pointers to the widgets
characteristic_map = {
    'character_name': {'frame': 'vitals'},
    'kingdom'       : {'frame': 'vitals', 'options': kingdom_options},
    'people'        : {'frame': 'vitals', 'options': people_options},
    'profession'    : {'frame': 'vitals', 'options': profession_options},
    'class'         : {'frame': 'vitals', 'options': class_options},
    'strength'      : {'frame': 'characteristics', 'name' : 'strength',      'value' :  5, 'type' : 'int', 'order' : 0},
    'agility'       : {'frame': 'characteristics', 'name' : 'agility',       'value' :  5, 'type' : 'int', 'order' : 1},
    'dexterity'     : {'frame': 'characteristics', 'name' : 'dexterity',     'value' :  5, 'type' : 'int', 'order' : 2},
    'resistance'    : {'frame': 'characteristics', 'name' : 'resistance',    'value' : 10, 'type' : 'int', 'order' : 3},
    'perception'    : {'frame': 'characteristics', 'name' : 'perception',    'value' :  5, 'type' : 'int', 'order' : 4},
    'communication' : {'frame': 'characteristics', 'name' : 'communication', 'value' :  5, 'type' : 'int', 'order' : 5},
    'culture'       : {'frame': 'characteristics',                           'value' :  5, 'type' : 'int', 'order' : 6},
    'appearance'    : {'frame': 'characteristics',                           'value' :  15, 'type' : 'int'},

    'IRR'           : {'frame': 'derived',                           'value' :  50, 'type' : 'int', 'derived' : ['RR']},
    'RR'            : {'frame': 'derived',                           'value' :  50, 'type' : 'int', 'derived' : ['IRR']},
    'luck'          : {'frame': 'derived',                           'value' :  15, 'type' : 'int', 'derived' : ['culture', 'perception', 'communication']},
    'LP'            : {'frame': 'derived',                           'value' :  10, 'type' : 'int', 'derived' : ['resistance']}
}

#Layout map

frame_map = {
    'controls'        :{
        'self_config' : {'padding' : "8 0 0 0" },
        'grid_config' : {'row' : 0, 'column': 0, 'sticky' : 'N, W', 'columnspan': 5},
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
        if 'appearance' not in label:
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
                    'self_config' : {'width' : len(name)+2, 'text' : beautify_text(name)}
                    },
                 'spinbox' : {
                     'grid_config' : {'row' :  0 + ((idx % rows)), 'column' :  1 + ((idx / cols)*2), 'sticky' : "W"},
                     'self_config' : {'width' : 3, 'textvariable' : None, 'from' : 0 , 'to' : 200 }
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
    if 'spinbox' in content_type:
        return Spinbox(frame)


def populate_frame(frame_name, configs):
    print "populating: {}".format(frame_name)
    frame = frame_map.get(frame_name).get('frame')
    for content_name , content_config in configs.items():
        if content_name not in characteristic_map.keys():
            characteristic_map[content_name] = {}
        content_data = characteristic_map.get(content_name)
        content_data['var'] = get_tk_var(content_data.get('type', ''))
        content_data['var'].set(content_data.get('value', '0'))
        content_data['frame'] = frame_name
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
            if 'label' in content_type:
                new_content.bind('<Button-1>', focus_out_handler)
            if 'option_menu' in content_type:
                content_data['var'].trace("w", trace_handler)
            elif 'entry' in content_type:
                new_content.bind('<FocusOut>', focus_out_handler)
            elif 'spinbox' in content_type:
                if 'characteristics' in frame_name:
                    new_content.bind('<FocusOut>', focus_out_handler)
                    new_content.config(command=lambda: characteristic_update("",""))

            if new_content is not None :
                new_content.grid(**content_configs.get('grid_config', {}))
                new_content.configure(**content_configs.get('self_config', {}))
                content_data[content_type] = new_content

def create_frames (master, name, configs):
    new_frame = Labelframe(master, text=beautify_text(name), **configs.get('self_config', {}))
    new_frame.columnconfigure(0,weight=1)
    new_frame.rowconfigure(0, weight=1)
    new_frame.grid(**configs.get('grid_config',{}))
    frame_map[name]['frame'] = new_frame
    #master.add(new_frame, text=name)

if __name__ == "__main__":
    #Place vitals

    root = Tk()
    print root['background']
    root.title("Aqualarre Character sheet")

    #p = Notebook(root)
    #p.grid(row=0, column=0)
    for name, configs in frame_map.items():
        create_frames(root, name, configs)


    #characteristic_label_strings = sorted([key for key, val in characteristic_map.items() if 'characteristics' in val.get('frame','')], key= lambda key_val: )
    characteristic_label_strings = get_subdict(characteristic_map, 'characteristics', 'frame')
    characteristic_label_strings = ordered_list_from_dict(characteristic_label_strings, 'order')
    pprint (characteristic_label_strings)
    derived_label_strings = [key for key, val in characteristic_map.items() if 'derived' in val.get('frame','')]


    create_frame_content('language_skills', sorted(language_skills_data), 2,2)
    create_frame_content('arms_skills', sorted(arms_skills_data), 2,2)
    create_frame_content('characteristics', characteristic_label_strings, 8, 8)
    create_frame_content('derived', derived_label_strings, 7, 7)
    create_frame_content('skills', sorted(skills_data), 7, 7)

    for frame_name, configs in frame_map.items():
        populate_frame(frame_name, configs.get('content_config', {}))

    for key, val in frame_map.items():
        for child in val['frame'].winfo_children():
            child.grid_configure(padx=2, pady=2)

    root.mainloop()
