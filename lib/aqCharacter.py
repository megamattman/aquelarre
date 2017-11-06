# Data object that contains methods to adjust displayed data
# I.e. update_skills will update the value of all skills
# Handles all calculations and should be aware of dependancies
# Between skills and characteristics
# When a widget's value is changed the updated value should come here and update applied

from pprint import pprint
import inspect


class AqCharacter (object):
    def __init__(self, gui_map, data):
        self.all_data = data
        self.character_data = {}
        #from gui_map extract references to the aqwidget and their name
        for key, val in gui_map.items():
            widgets = val.get('widgets')
            for widget in widgets:
                if key not in self.character_data:
                    self.character_data[key] = []
                aqwidget = widget.get('widget', '')
                self.character_data[key].append({aqwidget.name: aqwidget})
        pprint(self.character_data)

    def get_characteristic(self, name):
        for widget in self.character_data['characteristics']:
            if name in widget.keys():
                return widget.values()[0].curr_val

    # update map should contain names and new values
    def update_character_data(self, update_map):
        print inspect.stack()[0][3]
        pass

    def characteristic_update(self, widget):
        print inspect.stack()[0][3]
        # when characteristics are updated set the value of the characteristic AND update the skills
        complete_skills_list = (self.character_data.get('skills') +
                                self.character_data.get('language_skills') +
                                self.character_data.get('arms_skills'))
        for skill in complete_skills_list:
            if widget.name in skill.values()[0].characteristic:
                self.update_skill(skill.values()[0])

    def calculate_skill_value(self, widget, bonus=0):
        characteristic_value = self.get_characteristic(widget.characteristic)
        value = ((characteristic_value + widget.player_points) * widget.multiplier) + bonus
        return value

    # method for when widget interacted with
    def skill_update(self, widget):
        print inspect.stack()[0][3]
        widget.player_points += int(widget.curr_val) - self.calculate_skill_value(widget)
        self.update_skill(widget)

    def update_skill(self, widget, bonus=0):
        print inspect.stack()[0][3]
        characteristic_value = self.get_characteristic(widget.characteristic)
        value = ((characteristic_value + widget.player_points) * widget.multiplier) + bonus
        widget.curr_val = value

    def derived_update(self, widget):
        print inspect.stack()[0][3]
        pass

    def vitals_upate(self, widget):
        print inspect.stack()[0][3]
        pass

    def update(self, command, widget):
        update_method = getattr(self, command)
        update_method(widget)

#if __name__ == '__main__':
#    character = aqCharacter()
#    character.update('derived_update', "hello")

