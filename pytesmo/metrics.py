# Copyright (c) 2013,Vienna University of Technology,
# Department of Geodesy and Geoinformation
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Vienna University of Technology,
#      Department of Geodesy and Geoinformation nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
Created on Apr 17, 2013

@author: Christoph Paulik christoph.paulik@geo.tuwien.ac.at
@author: Sebastian Hahn sebastian.hahn@geo.tuwien.ac.at
@author: Alexander Gruber alexander.gruber@geo.tuwien.ac.at
'''
import numpy as np
import scipy.stats as sc_stats


def bias(x, y):
    """Bias
    """
    return np.mean(x) - np.mean(y)


def rmsd(x, y):
    """Root-mean-square deviation
    """
    return np.sqrt(RSS(x, y) / len(x))


def nrmsd(x, y):
    """Normalized root-mean-square deviation
    """
    return rmsd(x, y) / (np.max([x, y]) - np.min([x, y]))


def ubrmsd(x, y):
    """Unbiased root-mean-square deviation
    """
    return np.sqrt(np.sum(((x - np.mean(x)) - (y - np.mean(y))) ** 2) / len(x))


def mse(x, y):
    """Mean square error (MSE) as a decomposition of the RMSD into
    individual error components

    """
    MSEcorr = 2 * np.std(y) * np.std(x) * (1 - sc_stats.pearsonr(x, y)[0])
    MSEbias = bias(x, y) ** 2
    MSEvar = (np.std(x) - np.std(y)) ** 2
    MSE = MSEcorr + MSEbias + MSEvar

    return MSE, MSEcorr, MSEbias, MSEvar


def tcol_error(x, y, z):
    """Triple collocation error estimate

    Parameters
    ----------
    x : numpy.array
        1D numpy array to calculate the errors
    y : numpy.array
        1D numpy array to calculate the errors
    z : numpy.array
        1D numpy array to calculate the errors

    Returns
    -------
    triple collocation error for x : float
    triple collocation error for y : float
    triple collocation error for z : float
    """
    e_x = np.sqrt(np.abs(np.mean((x - y) * (x - z))))
    e_y = np.sqrt(np.abs(np.mean((y - x) * (y - z))))
    e_z = np.sqrt(np.abs(np.mean((z - x) * (z - y))))

    return e_x, e_y, e_z


def nash_sutcliffe(x, y):
    """Nash Sutcliffe model efficiency coefficient

    Parameters
    ----------
    x : numpy.array
        1D numpy array to calculate the metric
    y : numpy.array
        1D numpy array to calculate the metric

    Returns
    -------
    Nash Sutcliffe coefficient : float
         Nash Sutcliffe model efficiency coefficient
    """
    return 1 - (np.sum((x - y) ** 2)) / (np.sum((x - np.mean(x)) ** 2))


def RSS(x, y):
    """Redidual sum of squares

    Parameters
    ----------
    x : numpy.array
        1D numpy array to calculate the metric
    y : numpy.array
        1D numpy array to calculate the metric

    Returns
    -------
    Residual sum of squares
    """
    return np.sum((x - y) ** 2)


def pearsonr(x, y):
    """
    Wrapper for scipy.stats.pearsonr

    Parameters
    ----------
    x : numpy.array
        1D numpy array to calculate the metric
    y : numpy.array
        1D numpy array to calculate the metric

    Returns
    -------
    Pearson's r : float
        Pearson's correlation coefficent
    p-value : float
        2 tailed p-value

    See Also
    --------
    scipy.stats.pearsonr
    """
    return sc_stats.pearsonr(x, y)


def spearmanr(x, y):
    """
    Wrapper for scipy.stats.spearmanr

    Parameters
    ----------
    x : numpy.array
        1D numpy array to calculate the metric
    y : numpy.array
        1D numpy array to calculate the metric

    Returns
    -------
    rho : float
        Spearman correlation coefficient
    p-value : float
        The two-sided p-value for a hypothesis test whose null hypothesis
        is that two sets of data are uncorrelated

    See Also
    --------
    scipy.stats.spearmenr
    """
    return sc_stats.spearmanr(x, y)


def kendalltau(x, y):
    """
    Wrapper for scipy.stats.kendalltau

    Parameters
    ----------
    x : numpy.array
        1D numpy array to calculate the metric
    y : numpy.array
        1D numpy array to calculate the metric

    Returns
    -------
    Kendall's tau : float
        The tau statistic
    p-value : float
        The two-sided p-value for a hypothesis test whose null hypothesis
        is an absence of association, tau = 0.

    See Also
    --------
    scipy.stats.kendalltau
    """
    return sc_stats.kendalltau(x.tolist(), y.tolist())
