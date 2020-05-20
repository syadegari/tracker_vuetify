from bqplot import pyplot as plt
import pandas as pd
from helpers import moving_average
from functools import partial
import ipywidgets
from collections import namedtuple


__data__ = [None]


def get_xaxis():

    name = list(__data__.dfs.keys())[0]
    df = __data__.dfs[name]
    return pd.date_range(start=df['date'].values[0], periods=len(df))


def new_cases(countries, country, dfs, kw, n_mov_ave=5):
    xax = get_xaxis()

    df = dfs[country]
    h_bar = plt.bar(x=xax, y=df[kw])
    h_ave = plt.plot(xax, moving_average(df[kw], n_mov_ave), 'green')
    return h_bar, h_ave


def total_numbers(countries, country, dfs, kw, **kwargs):
    xax = get_xaxis()
    df = dfs[country]
    return plt.bar(x=xax, y=df[kw], **kwargs)


# TODO: Turn the init into a class
def init(data):
    global __data__
    __data__ = data
    #
    fig1 = plt.figure()
    plt1 = namedtuple('plot', ['fig', 'handles'])(
        fig1,
        namedtuple('Handles', ['bar', 'mov_ave'])(
            *new_cases(__data__.country_large, 'US', __data__.dfs,'new_cases', 5)
        )
    )
    #
    fig2 = plt.figure()
    plt2 = namedtuple('plot', ['fig', 'handles'])(
        fig2,
        namedtuple('Handles', ['confirmed', 'recovered', 'deaths'])(
            total_numbers(__data__.country_large, 'US', __data__.dfs, 'confirmed', colors=['red']),
            total_numbers(__data__.country_large, 'US', __data__.dfs, 'recovered', colors=['green']),
            total_numbers(__data__.country_large, 'US', __data__.dfs, 'deaths', colors=['black'])
        )
    )

    return namedtuple('figs', ['fig1', 'fig2'])(plt1, plt2)
