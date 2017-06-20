from pprint import pprint
try:
    # Python2
    from Tkinter import *
    from ttk import *
except ImportError:
    # Python3
    import tkinter as tk

default_self_config = {'width': 15, 'text': 'default_sc'}
default_grid_config = {'row': 0, 'column': 0}


class AqWidget (object):
    def __init__(self, name, config_list, frame):
        self.name = name
        self.tk_widgets = {}
        self.create_tk_widgets(config_list, frame)


    def create_tk_widgets(self, config_list, frame):
        for config in config_list:
            key = config.iterkeys().next()
            value = config.itervalues().next()
            self.tk_widgets[key] = ((create_tk_widget(config.get('type'),
                                                       value.get('self_config', {}),
                                                       value.get('grid_config', {}),
                                                       frame)))



class AqCharacteristic(AqWidget):
    def __init__(self, name, frame, location, **kwargs):
        self.curr_val = IntVar()
        self.min_val = 0
        self.min_val_string = StringVar()
        self.widgets = [
            {'type': Label, 'name_label': {
                'self_config': {'text': name},
                'grid_config': derive_location(location)}},
            {'type': Spinbox, 'spinbox_val': {
                'self_config': {'text': '', 'width': 3, 'textvariable': self.curr_val},
                'grid_config': derive_location(location, column_offset=1)}},
            {'type': Label, 'min_val_string_label': {
                'self_config': {'text': '', 'textvariable': self.min_val_string},
                'grid_config': derive_location(location, column_offset=2)}}
        ]
        config_list = create_widget_configs(self.widgets)
        AqWidget.__init__(self, name, config_list, frame)


class AqSkill(AqWidget):
    def __init__(self, name, frame, location, **kwargs):
        self.curr_val = IntVar()
        self.widgets = [
            {'type': Label, 'name_label': {
                'self_config': {'text': name, },
                'grid_config': derive_location(location)}},
            {'type': Spinbox, 'spinbox_val': {
                'self_config': {'text': '', 'width': 3, 'textvariable': self.curr_val},
                'grid_config': derive_location(location, column_offset=1)}}
        ]
        config_list = create_widget_configs(self.widgets)
        AqWidget.__init__(self, name, config_list, frame)


class AqVital(AqWidget):
    def __init__(self, name, frame, location, **kwargs):
        config_list = {}  # determine by template
        AqWidget.__init__(name, config_list, frame)


def create_config(default_config, widget_config):
    new_config = dict(default_config)
    new_config.update(widget_config)
    return new_config


def create_widget_config(config):
    config['self_config'] = create_config(default_self_config, config.get('self_config'))
    config['grid_config'] = create_config(default_grid_config, config.get('grid_config'))


def create_widget_configs(widgets):
    config_list = []
    for item in widgets:
        create_widget_config(item.itervalues().next())
        config_list.append(item)
    return config_list


def derive_location(base_location, row_offset=0, column_offset=0):
    return dict({'row': base_location['row'] + row_offset, 'column': base_location['column'] + column_offset,})


def create_tk_widget( widget_type, self_config, grid_config, frame):
    new_widget = widget_type(frame)
    new_widget.configure(**self_config)
    new_widget.grid(**grid_config)
    return new_widget
