import matplotlib.pyplot as plt
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
        v.set_visible(True)
    h_plt[name].set_visible(False)

def plot_countries(ax, countries, country, dfs, kw, n_mov_ave=5):
    h_plt = {}
    for country in countries:
        df = dfs[country]
        h_plt[country], = ax.plot(df['date'], df[kw], 'b', lw=.2)

    df = dfs[country]
    h_bar = ax.bar(df['date'], df[kw])
    h_ave, = ax.plot(df['date'], moving_average(df[kw], n_mov_ave))
    set_all_visible_except(country, h_plt)
    ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    return h_plt, h_bar, h_ave

plot_countries_new_cases = partial(plot_countries, kw='new_cases')
plot_countries_new_deaths = partial(plot_countries, kw='new_deaths')


def init(data):
    global __data__
    __data__ = data
    output = ipywidgets.Output()

    with output:
        fig, ax = plt.subplots()

    fig.canvas.toolbar_position = 'bottom'
    fig.tight_layout()

    return namedtuple('Plot', ['output', 'fig', 'ax', 'handles'])(
        output,
        fig,
        ax,
        Handles(ax, __data__.country_large, 'US', __data__.dfs, 5, 'new_cases')
    )

class Handles:
    def __init__(self, ax, countries, country, dfs, n_mov_ave, kw):
        self.plts, self.bar, self.mov_ave = plot_countries(ax,
                                                           countries,
                                                           country,
                                                           dfs,
                                                           kw,
                                                           n_mov_ave)

class Plots:
    def __init__(self, ax, countries, country, dfs, n_mov, toggle):
        self.new_cases = plot_countries_new_cases(ax, countries, country, dfs, n_mov)
        self.deaths = plot_countries_new_deaths(ax, countries, country, dfs, n_mov)
        self.toggle = toggle

    def toggle(self):
        self.toggle = (1 + self.toggle) % 2

    def toggle_visibility(self):
        pass

