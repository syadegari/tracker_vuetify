import numpy as np
import pandas as pd

from collections import namedtuple

# https://stackoverflow.com/questions/21463589/pandas-chained-assignments
pd.options.mode.chained_assignment = None


def read_data():
    return pd.read_csv("./covid-19/data/countries-aggregated.csv")


def lower_column_names(df):
    df.columns = map(str.lower, df.columns)
    return df


def get_country_names(df):
    return [name for name in list(set(df['country']))]


def aggregate_countries(df, country_list):
    return {country: df[df['country'] == country] for country in country_list}


def add_new_cases(df):
    df.loc[:, 'new_cases'] = df['confirmed'].diff().fillna(0, downcast='infer')
    return df


def add_new_death(df):
    df.loc[:, 'new_deaths'] = df['deaths'].diff().fillna(0, downcast='infer')
    return df


def add_daily_numbers(dfs):
    return {country: add_new_death(add_new_cases(df)) for country, df in dfs.items()}


def get_large_countries(dfs, country_names, max_cases=30000):
    return [name for name in country_names if dfs[name]['confirmed'].iloc[-1] > max_cases]


def moving_average(df, n):
    return df.rolling(n).mean().fillna(0).map(np.floor).map(int)


def prepare_data(max_num):
    df = read_data()
    df = lower_column_names(df)
    country_names = get_country_names(df)
    dfs = aggregate_countries(df, country_names)
    dfs = add_daily_numbers(dfs)
    country_large = get_large_countries(dfs, country_names, max_cases=max_num)
    return namedtuple('data', ['dfs', 'country_large'])(dfs, country_large)