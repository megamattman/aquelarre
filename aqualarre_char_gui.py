# #!/usr/bin/python
import yaml
from Tkinter import *
from ttk import *
from pprint import pprint
kingdom_options = []
people_options = []
#import aquallarre data

imported_data = {}
with open("data/AquallarreData.yaml", 'r') as stream:
    data = yaml.load(stream)


skills = data.get('skills', {})
kingdoms = data.get('kingdoms', {})
people = data.get('people', {})

kingdom_options = [kingdom for kingdom in kingdoms.keys()]
people_options = [option for option in people.keys()]

#Layout map
layout_map = {
    'kingdom_label'           : {'row' : 1 , 'col' : 0},
    'kingdom_options'         : {'row' : 1 , 'col' : 1},
    'people_label'            : {'row' : 1 , 'col' : 2},
    'people_options'            : {'row' : 1 , 'col' : 3},
    'characteristics_labels'  : {'row' : 2, 'col' : 0},
    'characteristics_entries' : {'row' : 2, 'col' : 1},
    'skills_labels'             : {'row' : 2, 'col' : 4},
    'skills_entries'            : {'row' : 2, 'col' : 5},
}
#Our string map
characteristic_map = {
    'kingdom'       : {                           'options': kingdom_options, 'var':None},
    'people'        : {                           'options': people_options, 'var':None},
    'Strength'      : {'Name' : 'Strength',      'value' : 0, 'var':None},
    'Agility'       : {'Name' : 'Agility',       'value' : 0, 'var':None},
    'Dexterity'     : {'Name' : 'Dexterity',     'value' : 0, 'var':None},
    'Resistance'    : {'Name' : 'Resistance',    'value' : 0, 'var':None},
    'Perception'    : {'Name' : 'Perception',    'value' : 0, 'var':None},
    'Communication' : {'Name' : 'Communication', 'value' : 0, 'var':None},
    'Culture'       : {'Name' : 'Culture',       'value' : 0, 'var':None},

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
vitals_label_strings = [
    'kingdom',
    'people'
]


root = Tk()

root.title("Aquallare Character sheet")

mainframe = Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0,weight=1)
mainframe.rowconfigure(0, weight=1)

def print_characteristics():
    #for label in characteristic_label_strings:
    #    print "{} = {}".format(label, characteristic_map[label]['var'].get())
    total_points=StringVar()
    total_points.set( "Total points: {}".format(total_characteristics()))
    Label(mainframe, text=total_points.get()).grid(column=4,row=1,sticky=(E))

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

#Place vitals
for vitals_label in vitals_label_strings:
    vitals = characteristic_map[vitals_label]
    characteristic_map[vitals_label]['var'] = StringVar()
    Label(mainframe, text=vitals_label).grid(column=layout_map[vitals_label+'_label']['col'],row=layout_map[vitals_label+'_label']['row'],sticky=(W))
    print vitals_label
    print vitals['options']
    OptionMenu(mainframe, characteristic_map[vitals_label]['var'],  vitals['options'][0], *vitals['options']).grid(column=layout_map[vitals_label+'_options']['col'], row=layout_map[vitals_label+'_options']['row'],sticky=W)

#Place characteristic labels and entries
for idx, label_string in enumerate (characteristic_label_strings):
    characteristic_map[label_string]['var'] = IntVar()
    label_row = layout_map['characteristics_labels']['row'] + idx
    label_col = layout_map['characteristics_labels']['col']
    entry_col = layout_map['characteristics_entries']['col']
    entry_row = layout_map['characteristics_entries']['row'] +idx
    Label(mainframe, text=label_string).grid(column=label_col,row=label_row,sticky=(W))
    Entry(mainframe, width=3, textvariable=characteristic_map[label_string]['var']).grid(column=entry_col, row=entry_row,sticky=(W))

#Place skill label and entries
for idx, skill in enumerate(skills):
    #assumes {skill_name : {characteristic : XXX}}
    label_string, _ = skill.items()[0]
    skill['var'] = IntVar()
    label_row = layout_map['skills_labels']['row'] + idx % 10
    label_col = layout_map['skills_labels']['col'] + ((idx / 10)*2)
    entry_col = layout_map['skills_entries']['col'] + ((idx / 10)*2)
    entry_row = layout_map['skills_entries']['row'] + idx % 10
    Label(mainframe, text=label_string).grid(column=label_col,row=label_row,sticky=(E))
    Entry(mainframe, width=3, textvariable=skill['var']).grid(column=entry_col, row=entry_row,sticky=(E))

total_points=StringVar()
total_points.set( "{}".format(total_characteristics()))

Label(mainframe, textvariable=total_points).grid(column=4,row=1,sticky=(E))

Button(mainframe, text="Update", command=print_characteristics).grid(column=0,row=0, sticky=(N, E))
#feet = StringVar()
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

mainframe.bind("<Key>", pop)

for child in mainframe.winfo_children():
    child.grid_configure(padx=1, pady=1)

#root.bind('<Return>', calculate)



root.mainloop()
