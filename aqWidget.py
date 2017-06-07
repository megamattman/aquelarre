#An aqWidget is a collection of tk widgets which are grouped together and
#share information, there will be a few which should be genreric, the purpose
#of these is to keep the functional code within the realms of each widget class
#Each flavour of aqWidget will have implicit knowledge of the relationship of
#its own tk widgets
class aqWidgetBase (object):
    def __init__ (self, name, config_list):
        self.name = name
        self.tk_widget_map = {}
        self.config_list = []

    def create_tk_widgets(self):
        for item_config in self.config_list:
            for _, __ in item_config:
                continue
                #here iterate through the config list
                #format should be:
                #{'widget_type' : 'self_config', 'grid_config'}

    def set_tk_widget_value(self, name, value):
        self.tk_widget_map.get(name).get('var').set(value)

    def get_tk_widget_value(self, name):
        return self.tk_widget_map.get(name).get('var').get()

    def get_tk_widget(self, name):
        return self.tk_widget_map.get(name)

#characteristics opject should get a name, a starting position
#the object know about where to place the items relative to the
#start position
#output of create: |name_label| |spinbox| |min_val_label|
class aqCharacteristic (aqWidgetBase):
    def __init__ (self, name, config_list):
        self.config_list = config_list
        self.widget_name_list = ['name_label', 'val_spinbox, min_label']
        #do charactersitc specific work here
        aqWidgetBase.__init__(name, self.config_list)

    def set_min_val(self, value):
        return self.set_tk_widget_value('min_label', value)

    def get_min_val(self):
        return self.get_tk_widget_value('min_label')

    def get_val_spinbox(self):
        return self.get_tk_widget_value('val_spinbox')

    def get_name_label(self):
        return self.get_tk_widget_value('name_label')

#skill object should output: |skill_name| |spinbox|
#Each skill should know its type, default tertiary
class aqSkill (aqWidgetBase):
    def __init__ (self, name, config_list):
        aqWidgetBase.__init__(name, config_list)
        self.skill_type = 'tertiary'

#vitals are different, they can be either of the follwing:
# |vital_label| |vital_entry|
# |vital_label| |vital_entry| |vital_label|
# |vital_label| |vital_options|
class aqVitals (aqWidgetBase):
    def __init__ (self, name, config_list):
        aqWidgetBase.__init__(name, config_list)
