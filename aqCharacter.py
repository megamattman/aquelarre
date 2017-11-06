# Data object that contains methods to adjust displayed data
# I.e. update_skills will update the value of all skills
# Handles all calculations and should be aware of dependancies
# Between skills and characteristics
# When a widget's value is changed the updated value should come here and update applied

class aqCharacter (object):
    def _init__(self):
        pass

    # Call will return current state of character data
    def __call__(self):
        pass

    # update map should contain names and new values
    def update_character_data(self, update_map):
        pass

    def characteristic_update(self, widget):
        pass

    def skill_update(self, widget):
        pass

    def derived_update(self, widget):
        pass

    def vitals_upate(self, widget):
        pass

    def update(self, command, widget):
        update_method = getattr(self, command)
        update_method(widget)

if __name__ == '__main__':
    character = aqCharacter()
    character.update('derived_update', "hello")
