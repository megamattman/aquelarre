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


class AqWidgetCollectino (object):
    def __init__(self, name):
        pass


class AqWidget (object):
    def __init__(self, name, config_list, frame):
        self.name = name
        self.tk_widgets = {}
        self.frame = frame
        self.create_tk_widgets()

    def create_tk_widgets(self):
        for widget in self.widgets:
            config = widget.get('configs')
            key = widget.get('name')
            #widget_configs = get_configs(config)
            self.tk_widgets[key] = (
                (self.build_tk_widget(
                        widget.get('type'),
                        config.get('self_config', {}),
                        config.get('grid_config', {}),
                        self.frame)))
        print "hello"

    def build_tk_widget(self, widget_type, self_config, grid_config, frame):
        # print widget_type
        if widget_type == OptionMenu:
            new_widget = widget_type(frame, self_config.get('variable'), self_config.get('value'),
                                     *self_config.get('values'))
        else:
            new_widget = widget_type(frame)
            new_widget.configure(**self_config)
            # Will not accept being set as part of **self_config
            if 'textvariable' in self_config:
                new_widget.configure(textvariable=self_config['textvariable'])

        new_widget.grid(**grid_config)
        return new_widget


    @property
    def curr_val(self):
        return self._curr_val.get()

    @curr_val.setter
    def curr_val(self, value):
        self._curr_val.set(value)


class AqCharacteristic(AqWidget):
    def __init__(self, name, frame, location, **kwargs):
        self.min_val = kwargs['min_val']
        command = lambda x=self: kwargs.get['event_handler'](x, kwargs.get('command', ''))
        self.min_val_string = StringVar()
        self.min_val_string.set("min_val : {}".format(self.min_val))
        self.player_points = 0
        self._curr_val = IntVar()
        self._curr_val.set(self.min_val)
        self.widgets = [
            {'type': Label, 'name': 'name_label', 'configs': {
                'self_config': {'text': name},
                'grid_config': derive_location(location)}},
            {'type': Spinbox, 'name': 'spinbox_val', 'configs': {
                'self_config':
                    {'text': '', 'width': 3, 'textvariable':  self._curr_val, 'from_': self.min_val, 'to': 20, 'command': command},
                'grid_config': derive_location(location, column_offset=1)}},
            {'type': Label, 'name': 'min_val_string_label', 'configs': {
                'self_config': {'text': '', 'textvariable': self.min_val_string},
                'grid_config': derive_location(location, column_offset=2)}}
        ]
        config_list = create_widget_configs(self.widgets)
        AqWidget.__init__(self, name, config_list, frame)

class AqSkill(AqWidget):
    def __init__(self, name, frame, location, **kwargs):
        command = lambda x=self: kwargs['event_handler'](x, kwargs.get('command', ''))
        self._curr_val = IntVar()
        self.widgets = [
            {'type': Label, 'name':'name_label', 'configs': {
                'self_config': {'text': name, 'anchor': 'e', 'width': 18},
                'grid_config': derive_location(location), 'sticky': 'e'}},
            {'type': Spinbox, 'name': 'spinbox_val', 'configs': {
                'self_config': {'text': '', 'width': 3, 'textvariable': self._curr_val, 'from_': 0, 'to': 200, 'command':command},
                'grid_config': derive_location(location, column_offset=1)}}
        ]
        self.characteristic = kwargs.get('characteristic')
        self.player_points = 0
        self.multiplier = 1
        config_list = create_widget_configs(self.widgets)
        AqWidget.__init__(self, name, config_list, frame)


class AqVital(AqWidget):
    def __init__(self, name, frame, location, **kwargs):
        self._curr_val = StringVar()

        def focus_out_handler(a,b,c, widget=self, command=kwargs.get('command', ''), handler=kwargs['event_handler']):
            return handler(widget,command)
        self._curr_val.trace('w', focus_out_handler)
        self.type = kwargs.get('widget')
        self.widgets = [
            {'type': Label, 'name': 'name_label', 'configs': {
                'self_config': {'text': name},
                'grid_config': derive_location(location)}}
        ]
        for idx, widget in enumerate(kwargs.get('widget')):
            next_location = derive_location(location, column_offset=idx+1)
            extra_widgets = derive_config_from_kwargs(self._curr_val, next_location, widget, kwargs)
            self.widgets.append(extra_widgets)

        config_list = create_widget_configs(self.widgets)
        AqWidget.__init__(self, name, config_list, frame)

    def update_options(self, options):
        pprint(self.tk_widgets)
        if 'options' in self.type:
            widget_to_modify = self.get_options_widget()
            widget_to_modify['menu'].delete(0, 'end')
            for option in options:
                widget_to_modify['menu'].add_command(label=option,
                                             command=lambda v=option: self._curr_val.set(v))

    def get_options_widget(self):
        print self.tk_widgets
        for _, tk_widget in self.tk_widgets.items():
            if isinstance(tk_widget, OptionMenu):
                return tk_widget
        return None

class AqPeopleVital(AqVital):

    def set_society (self, value):


def derive_config_from_kwargs(curr_val, location, widget_type_name, kwargs):
    if 'options' in widget_type_name:
        name = 'options'
        widget_type = OptionMenu
        self_config = {'variable': curr_val, 'value': 'select', 'values' : kwargs.get('options')}
    elif 'entry' in widget_type_name:
        name = 'entry'
        widget_type = Entry
        self_config = {'textvariable': curr_val, 'width': 20}
    elif 'label' in widget_type_name:
        name = 'label'
        widget_type = Label
        self_config = {'textvariable': curr_val, 'width': 20}
    else:
        return {}

    grid_config = location
    return dict({'type': widget_type, 'name': name, 'configs': {'self_config': self_config, 'grid_config': grid_config}})


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
        #pprint(configs)
        create_widget_config(configs)
        config_list.append(item)
    return config_list


def derive_location(base_location, row_offset=0, column_offset=0):
    return dict({'row': base_location['row'] + row_offset, 'column': base_location['column'] + column_offset,})


