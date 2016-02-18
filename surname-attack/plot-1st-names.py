#!/usr/bin/env python

import pandas as pd
import pylab as pl

dfb = pd.read_csv("boys.csv", header=0, thousands=",")
dfg = pd.read_csv("girls.csv", header=0, thousands=",")
df = pd.concat([dfb, dfg])
df.reset_index(drop=True, inplace=True)
df.sort("count", ascending=False, inplace=True)
N = df["count"].sum()
deltas_ = df['count'].values[:-1] - df['count'].values[1:]
deltas = pl.array([deltas_[0]] + list(pl.amin([deltas_[1:], deltas_[:-1]], axis=0)) + [deltas_[-1]])
dfrac = (deltas + 1e-20) / N


def frac_leaked(q):
    attacked = dfrac * q > (2 * q * df['count'] / N) ** 0.5
    N_a = df['count'][attacked].sum()
    return float(N_a) / N


Ns = pl.logspace(0, 15, 100)
fracs = pl.array(map(frac_leaked, Ns))

pl.semilogx(Ns, fracs * 100)
pl.xlabel("Number of queries")
pl.ylabel("% of surnames revealed")
pl.yticks(range(0, 110, 10))
pl.grid(True)
pl.show()
