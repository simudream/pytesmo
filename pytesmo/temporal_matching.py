'''
Created on Apr 12, 2013

Provides a temporal matching function

@author: Sebastian Hahn Sebastian.Hahn@geo.tuwien.ac.at
'''
import numpy as np
import scipy.interpolate as sc_int
import pandas as pd


def df_match(reference, *args, **kwds):
    '''
    Finds temporal match between the reference pandas.DataFrame (index has to
    be datetime) and n other pandas.DataFrame (index has to be datetime).

    Parameters
    ----------
    reference : pandas.DataFrame
        The index of this dataframe will be the reference.
    *args : pandas.DataFrame
        The index of this dataframe(s) will be matched.
    window : float
        Fraction of days of the maximum pos./neg. distance allowed, i.e. the
        value of window represents the half-winow size (e.g. window=0.5, will
        search for matches between -12 and +12 hours) (default: None)
    dropna : boolean
        Drop rows containing only NaNs (default: False)
    dropduplicates : boolean
        Drop duplicated temporal matched (default: False)

    Returns
    -------
    temporal_matched_args : pandas.DataFrame or tuple of pandas.DataFrame
        Dataframe with index from matched reference index
    '''
    if "window" in kwds:
        window = kwds['window']
    else:
        window = None

    temporal_matched_args = []
    ref_step = reference.index.values - reference.index.values[0]

    for arg in args:
        comp_step = arg.index.values - reference.index.values[0]
        matched = sc_int.griddata(comp_step, np.arange(comp_step.size),
                                  ref_step, "nearest")

        distance = np.zeros_like(matched)
        distance.fill(np.nan)
        valid_match = np.invert(np.isnan(matched))

        distance[valid_match] = \
            (arg.index.values[np.int32(matched[valid_match])] -
             reference.index.values[valid_match]) / np.timedelta64(1, 'D')

        arg['index'] = arg.index.values
        arg['merge_key'] = np.arange(len(arg))

        arg_matched = pd.DataFrame({'merge_key': matched,
                                    'distance': distance,
                                    'ref_index': reference.index.values})
        arg_matched = arg_matched.merge(arg, on="merge_key", how="left")
        arg_matched.index = arg_matched['ref_index'].values
        arg_matched = arg_matched.sort_index()

        if window is not None:
            invalid_dist = arg_matched['distance'].abs() > window
            arg_matched.loc[invalid_dist] = np.nan

        if "dropna" in kwds and kwds['dropna']:
            arg_matched = arg_matched.dropna()

        if "dropduplicates" in kwds and kwds['dropduplicates']:
            arg_matched = arg_matched.dropna()
            g = arg_matched.groupby('merge_key')
            min_dists = g.distance.apply(lambda x: x.abs().idxmin())
            arg_matched = arg_matched.ix[min_dists]

        temporal_matched_args.append(\
                arg_matched.drop(['merge_key', 'ref_index'], axis=1))

    if len(temporal_matched_args) == 1: return temporal_matched_args[0]    
    else: return tuple(temporal_matched_args)
