from collections import namedtuple
import ipyvuetify as v
import ipywidgets as w
import bqplot.pyplot as plt
from helpers import moving_average

__plts__ = [None]
__data__ = [None]
__widgets__ = [None]
#
def make_widgets(country_large):

    radio_new_cases = v.Radio(label='Cases')
    radion_new_deaths = v.Radio(label='Mortality')
    widgets = namedtuple('Widget',
                         ['chk_mov_ave',
                         'slider_mov_ave',
                          'rad_cases',
                         'sel_country'])(
        v.Checkbox(v_model='default', label='moving average'),
        v.Slider(min=2, max=10, class_='px-4', v_model='default', thumb_label=True, ticks=True),
        v.RadioGroup(children=[radio_new_cases, radion_new_deaths],
                     row=True,
                     mandatory=False,
                     v_model='ex2'),
        v.Select(items=country_large, v_model='default')
    )
    return widgets


def draw():
    return v.Layout(children=[
        v.Flex(children=[
            __widgets__.sel_country,
            __widgets__.rad_cases,
            __widgets__.chk_mov_ave,
            __widgets__.slider_mov_ave,
            __plts__.fig
        ],
        )
    ])


# helpers
def set_all_visible_except(value):
    for _, h in __plts__.handles.plts.items():
        h.visible = True
    __plts__.handles.plts[value].visible = False


def set_ylim_bottom():
    _, y_axis = __plts__.fig.axes
    y_axis.scale.min = 0.0


def set_ylim_top(name):
    _, y_axis = __plts__.fig.axes
    y_axis.scale.max = __data__.dfs[name]['new_cases'].max() * 1.1



def update_ylim(name):
    set_ylim_bottom()
    set_ylim_top(name)

# callbacks
def update_mov_ave(name, n):
    __plts__.handles.mov_ave.y = moving_average(__data__.dfs[name]['new_cases'], n)


def update_slider_mov_ave(value):
    name = __widgets__.sel_country.v_model
    update_mov_ave(name, value)

def update_chk_mov_ave(value):
    if value:
        name = __widgets__.sel_country.v_model
        n_day = __widgets__.slider_mov_ave.v_model
        update_mov_ave(name, n_day)
        __plts__.handles.mov_ave.visible = True
    else:
        __plts__.handles.mov_ave.visible = False


def update_sel_country(value):
    df = __data__.dfs[value]
    __plts__.handles.bar.y = df['new_cases']
    set_all_visible_except(value)
    update_ylim(value)
    update_chk_mov_ave(__widgets__.chk_mov_ave.v_model)

def observe():
    __widgets__.chk_mov_ave.observe(lambda x: update_chk_mov_ave(x.new), names='v_model')
    __widgets__.slider_mov_ave.observe(lambda x: update_slider_mov_ave(x.new), names='v_model')
    __widgets__.sel_country.observe(lambda x: update_sel_country(x.new), names='v_model')

def set_default():
    __widgets__.chk_mov_ave.v_model = False
    update_chk_mov_ave(False)
    __widgets__.sel_country.v_model = __data__.country_large[0]
    update_sel_country(__widgets__.sel_country.v_model)
    __widgets__.slider_mov_ave.v_model = 5

def init(data, plts):
    global __plts__
    global __data__
    global __widgets__
    #
    __plts__ = plts
    __data__ = data
    __widgets__ = make_widgets(__data__.country_large)
    set_default()
    observe()
