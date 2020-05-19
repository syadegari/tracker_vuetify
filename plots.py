from bqplot import pyplot as plt
import pandas as pd
from helpers import moving_average
from functools import partial
import ipywidgets
from collections import namedtuple


__data__ = [None]

def set_ylim_bottom():
    if log_scale.value:
        ax.set_ylim(bottom=1.0)
    else:
        ax.set_ylim(bottom=0.0)


def set_ylim_top(name):
    ax.set_ylim(top=dfs[name]['new_cases'].max() * 1.1)


def set_all_visible_except(name, h_plt):
    for _, v in h_plt.items():
        v.visible = True
    h_plt[name].visible = False


def get_xaxis():

    name = list(__data__.dfs.keys())[0]
    df = __data__.dfs[name]
    return pd.date_range(start=df['date'].values[0], periods=len(df))

def plot_countries(countries, country, dfs, kw, n_mov_ave=5):
    xax = get_xaxis()
    h_plt = {}
    for country in countries:
        df = dfs[country]
        h_plt[country] = plt.plot(x=xax, y=df[kw])

    df = dfs[country]
    h_bar = plt.bar(x=xax, y=df[kw])
    h_ave = plt.plot(x=xax, y=moving_average(df[kw], n_mov_ave))
    set_all_visible_except(country, h_plt)
    return h_plt, h_bar, h_ave

plot_countries_new_cases = partial(plot_countries, kw='new_cases')
plot_countries_new_deaths = partial(plot_countries, kw='new_deaths')

# TODO: Turn the init into a class
def init(data):
    global __data__
    __data__ = data

    fig = plt.figure()

    return namedtuple('Plot', ['fig', 'handles'])(
        fig,
        Handles(__data__.country_large, 'US', __data__.dfs, 5, 'new_cases')
    )

class Handles:
    def __init__(self, countries, country, dfs, n_mov_ave, kw):
        self.plts, self.bar, self.mov_ave = plot_countries(
                                                           countries,
                                                           country,
                                                           dfs,
                                                           kw,
                                                           n_mov_ave)
