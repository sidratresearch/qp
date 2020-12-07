
import qp
import numpy as np
import time

from qp import plotting

import matplotlib as mpl
import matplotlib.pyplot as plt

testfile = 'qp_test_ensemble.hdf5'

def run_metrics(prefix, ens_orig, ens_test):

    t0 = time.time()
    kld = ens_orig.kld(ens_test, limits=(0.,3.))
    t1 = time.time()

    print("kld: mean %.2e, std %.2e" % (kld.mean(), kld.std()))

    fig = plt.figure()
    axes = fig.subplots()
    axes.hist(kld, bins=np.linspace(kld.min(), kld.max(), 101))
    fig.savefig("%s_kld.png" % prefix)

    

ens_orig = qp.read(testfile)

print("Running conversions for interp, quant, hist")
ens_g51 = qp.convert(ens_orig, 'interp', xvals=np.linspace(0, 3, 51))
ens_g21 = qp.convert(ens_orig, 'interp', xvals=np.linspace(0, 3, 21))
ens_q51 = qp.convert(ens_orig, 'quant', quants=np.linspace(0.01, 0.99, 51))
ens_q21 = qp.convert(ens_orig, 'quant', quants=np.linspace(0.01, 0.99, 21))
ens_h51 = qp.convert(ens_orig, 'hist', bins=np.linspace(0, 3.0, 51))
ens_h21 = qp.convert(ens_orig, 'hist', bins=np.linspace(0, 3.0, 21))

print("Running conversinos for spline, mixmod")
ens_red = ens_orig[np.arange(100)]
ens_s51 = qp.convert(ens_red, 'spline', xvals=np.linspace(0, 3.0, 51), method="xy")
ens_s21 = qp.convert(ens_red, 'spline', xvals=np.linspace(0, 3.0, 21), method="xy")
ens_m3 = qp.convert(ens_red, 'mixmod', xvals=np.linspace(0, 3.0, 301), ncomps=3)
ens_m5 = qp.convert(ens_red, 'mixmod', xvals=np.linspace(0, 3.0, 301), ncomps=3)

label_list = ['g51', 'g21', 'q51', 'q21', 'h51', 'h21']
label_list2 = ['s51', 's21', 'm3', 'm5']
ens_list = [ens_g51, ens_g21, ens_q51, ens_q21, ens_h51, ens_h21]
ens_list2 = [ens_s51, ens_s21, ens_m3, ens_m5]

for label, ens in zip(label_list, ens_list):
    print("Running metrics for %s" % label)
    run_metrics(label, ens_orig, ens)

for label, ens in zip(label_list2, ens_list2):
    print("Running metrics for %s" % label)
    run_metrics(label, ens_red, ens)