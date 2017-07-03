from pprint import pprint
try:
    # Python2
    from Tkinter import *
    from ttk import *
except ImportError:
    # Python3
    import tkinter as tk

default_self_config = {'width' : 15, 'text': 'default_sc'}
default_grid_config = {'row': 0, 'column': 0}


class AqWidget (object):
    def __init__(self, name, config_list, frame):
        self.name = name
        self.tk_widgets = {}
        self.frame = frame

    def create_tk_widgets(self):
        for config in self.widgets:
            key = config.iterkeys().next()
            widget_configs = get_configs(config)
            self.tk_widgets[key] = (
                (create_tk_widget(
                        config.get('type'),
                        widget_configs.get('self_config', {}),
                        widget_configs.get('grid_config', {}),
                        self.frame)))


class AqCharacteristic(AqWidget):
    def __init__(self, name, frame, location, **kwargs):
        self.curr_val = IntVar()
        self.min_val = 0
        self.min_val_string = StringVar()
        self.min_val_string.set("min_val")
        self.curr_val.set(0)
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
                'self_config': {'text': name, 'anchor': 'e', 'width': 18},
                'grid_config': derive_location(location), 'sticky': 'e'}},
            {'type': Spinbox, 'spinbox_val': {
                'self_config': {'text': '', 'width': 3, 'textvariable': self.curr_val},
                'grid_config': derive_location(location, column_offset=1)}}
        ]
        config_list = create_widget_configs(self.widgets)
        AqWidget.__init__(self, name, config_list, frame)


class AqVital(AqWidget):
    def __init__(self, name, frame, location, **kwargs):
        self.curr_val = StringVar()
        self.widgets = [
            {'type': Label, 'name_label': {
                'self_config': {'text': name},
                'grid_config': derive_location(location)}}
        ]
        next_location = derive_location(location, column_offset=1)
        self.widgets.append(derive_config_from_kwargs(self.curr_val, next_location, **kwargs))
        pprint(self.widgets)
        config_list = create_widget_configs(self.widgets)
        AqWidget.__init__(self, name, config_list, frame)


def derive_config_from_kwargs(curr_val, location, **kwargs):
    if 'options' in kwargs:
        name = 'options'
        widget_type = OptionMenu
        self_config = {'variable': curr_val, 'value': 'select', 'values' : tuple(kwargs.get('options'))}
    elif 'entry':
        name = 'entry'
        widget_type = Entry
        self_config = {'textvariable': curr_val, 'width': 20}
    else:
        return {}

    grid_config = location
    return {'type': widget_type, name: {'self_config': self_config, 'grid_config': grid_config}}


def create_config(default_config, widget_config):
    new_config = dict(default_config)
    new_config.update(widget_config)
    return new_config


def create_widget_config(config):
    config['self_config'] = create_config(default_self_config, config.get('self_config'))
    config['grid_config'] = create_config(default_grid_config, config.get('grid_config'))


def get_configs(item):
    for _, value in item.items():
        if type(value) is dict:
            if 'self_config' in value:
                return value


def create_widget_configs(widgets):
    config_list = []
    for item in widgets:
        configs = get_configs(item)
        pprint(configs)
        create_widget_config(configs)
        config_list.append(item)
    return config_list


def derive_location(base_location, row_offset=0, column_offset=0):
    return dict({'row': base_location['row'] + row_offset, 'column': base_location['column'] + column_offset,})


def create_tk_widget( widget_type, self_config, grid_config, frame):
    print widget_type
    if widget_type == OptionMenu:
        new_widget = widget_type(frame, self_config.get('variable'), self_config.get('value'), self_config.get('values'))
    else:
        new_widget = widget_type(frame)
        new_widget.configure(**self_config)
    new_widget.grid(**grid_config)
    return new_widget
