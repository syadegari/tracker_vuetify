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

def plot_countries(countries, country, dfs, kw, n_mov_ave=5):
    xax = get_xaxis()

    df = dfs[country]
    h_bar = plt.bar(x=xax, y=df[kw])
    h_ave = plt.plot(x=xax, y=moving_average(df[kw], n_mov_ave))
    return h_bar, h_ave


def total_numbers(countries, country, dfs, kw, **kwargs):
    xax = get_xaxis()
    df = dfs[country]
    return plt.bar(x=xax, y=df[kw], **kwargs)


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
        self.bar, self.mov_ave = plot_countries(
            countries,
            country,
            dfs,
            kw,
            n_mov_ave)
