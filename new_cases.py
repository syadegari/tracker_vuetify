from collections import namedtuple
import ipyvuetify as v
import ipywidgets as w
from helpers import moving_average

__plts__ = [None]
__data__ = [None]
__widgets__ = [None]
#
def make_widgets(country_large):

    radio_new_cases = v.Radio(label='case')
    radion_new_deaths = v.Radio(label='death')
    widgets = namedtuple('Widget',
                         ['chk_mov_ave',
                         'slider_mov_ave',
                         'chk_log_scale',
                         'rad_cases',
                         'sel_country'])(
        v.Checkbox(v_model='default', label='moving average'),
        v.Slider(min=2, max=10, class_='px-4', v_model='default', thumb_label=True, ticks=True),
        v.Checkbox(v_model='default', label='log scale'),
        v.RadioGroup(children=[radio_new_cases, radion_new_deaths],
                     row=True,
                     mandatory=False,
                     v_model='ex2'),
        v.Select(items=country_large, v_model='default')
    )
    return widgets

def draw(output):
    return v.Layout(children=[
        v.Flex(children=[
            __widgets__.sel_country,
            __widgets__.rad_cases,
            __widgets__.chk_mov_ave,
            __widgets__.slider_mov_ave,
            __widgets__.chk_log_scale,
            output
        ],
        ),
        # v.Flex(xs12=True, xl4=True, children=[output])
    ])


# helpers
def set_all_visible_except(value):
    for _, h in __plts__.handles.plts.items():
        h.set_visible(True)
    __plts__.handles.plts[value].set_visible(False)


def set_ylim_bottom():
    if __widgets__.chk_log_scale.v_model:
        __plts__.ax.set_ylim(bottom=1.0)
    else:
        __plts__.ax.set_ylim(bottom=0.0)


def set_ylim_top(name):
    __plts__.ax.set_ylim(top=__data__.dfs[name]['new_cases'].max() * 1.1)


def update_ylim(name):
    set_ylim_bottom()
    set_ylim_top(name)

# callbacks
def update_chk_log_scale(value):
    if value:
        set_ylim_bottom()
        __plts__.ax.set_yscale('log')
    else:
        __plts__.ax.set_yscale('linear')
        set_ylim_bottom()

def update_slider_mov_ave(value):
    df = __data__.dfs[__widgets__.sel_country.v_model]
    __plts__.handles.mov_ave.set_ydata(moving_average())

def update_chk_mov_ave(value):
    if value:
        __plts__.handles.mov_ave.set_visible(True)
    else:
        __plts__.handles.mov_ave.set_visible(False)

def update_sel_country(value):
    df = __data__.dfs[value]
    for h, y in zip(__plts__.handles.bar, df['new_cases']):
        h.set_height(y)
    set_all_visible_except(value)
    __plts__.ax.set_title(f'New Cases: {value}')
    update_ylim(value)
    # update_mov_ave(mov_ave.value)

def observe():
    __widgets__.chk_log_scale.observe(lambda x: update_chk_log_scale(x.new), names='v_model')
    __widgets__.chk_mov_ave.observe(lambda x: update_chk_mov_ave(x.new), names='v_model')
    __widgets__.slider_mov_ave.observe(lambda x: update_slider_mov_ave(x.new), names='v_model')
    __widgets__.sel_country.observe(lambda x: update_sel_country(x.new), names='v_model')

def set_default():
    __widgets__.chk_log_scale.v_model = False
    __widgets__.chk_mov_ave.v_model = False
    __widgets__.sel_country.v_model = __data__.country_large[0]
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
