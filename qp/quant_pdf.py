"""This module implements a PDT distribution sub-class using interpolated quantiles
"""


import numpy as np

from scipy.stats import rv_continuous

from qp.pdf_gen import Pdf_rows_gen

from qp.conversion_funcs import convert_using_quantiles
from qp.plotting import get_axes_and_xlims, plot_pdf_quantiles_on_axes
from qp.utils import interpolate_unfactored_multi_x_y, interpolate_unfactored_x_multi_y, interpolate_multi_x_y, interpolate_x_multi_y
from qp.test_data import QUANTS, QLOCS, TEST_XVALS
from qp.factory import add_class

class quant_gen(Pdf_rows_gen):
    """Spline based distribution

    Notes
    -----
    This implements a PDF by interpolating a set of quantile values

    It simply takes a set of x and y values and uses `scipy.interpolate.interp1d` to
    build the CDF
    """
    # pylint: disable=protected-access

    name = 'quant'
    version = 0

    _support_mask = rv_continuous._support_mask

    def __init__(self, quants, locs, *args, **kwargs):
        """
        Create a new distribution using the given values

        Parameters
        ----------
        quants : array_like
           The quantiles used to build the CDF
        locs : array_like
           The locations at which those quantiles are reached
        """
        kwargs['npdf'] = locs.shape[0]

        #kwargs['a'] = self.a = np.min(locs)
        #kwargs['b'] = self.b = np.max(locs)

        super(quant_gen, self).__init__(*args, **kwargs)

        self._quants = np.asarray(quants)
        self._nquants = self._quants.size
        if locs.shape[-1] != self._nquants:  # pragma: no cover
            raise ValueError("Number of locations (%i) != number of quantile values (%i)" % (self._nquants, locs.shape[-1]))
        self._locs = locs

        self._addmetadata('quants', self._quants)
        self._addobjdata('locs', self._locs)

    @property
    def quants(self):
        """Return quantiles used to build the CDF"""
        return self._quants

    @property
    def locs(self):
        """Return the locations at which those quantiles are reached"""
        return self._locs

    def _cdf(self, x, row):
        # pylint: disable=arguments-differ
        factored, xr, rr, _ = self._sliceargs(x, row)
        if factored:
            return interpolate_multi_x_y(xr, self._locs[rr], self._quants, bounds_error=False, fill_value=(0., 1)).reshape(x.shape)
        return interpolate_unfactored_multi_x_y(xr, rr, self._locs, self._quants, bounds_error=False, fill_value=(0., 1))

    def _ppf(self, x, row):
        # pylint: disable=arguments-differ
        factored, xr, rr, _ = self._sliceargs(x, row)
        if factored:
            return interpolate_x_multi_y(xr, self._quants, self._locs[rr], bounds_error=False, fill_value=(self.a, self.b)).reshape(x.shape)
        return interpolate_unfactored_x_multi_y(xr, rr, self._quants, self._locs, bounds_error=False, fill_value=(self.a, self.b))

    def _updated_ctor_param(self):
        """
        Set the bins as additional construstor argument
        """
        dct = super(quant_gen, self)._updated_ctor_param()
        dct['quants'] = self._quants
        dct['locs'] = self._locs
        return dct

    @classmethod
    def plot_native(cls, pdf, **kwargs):
        """Plot the PDF in a way that is particular to this type of distibution

        For a quantile this shows the quantiles points
        """
        axes, xlim, kw = get_axes_and_xlims(**kwargs)
        xvals = np.linspace(xlim[0], xlim[1], kw.pop('npts', 101))
        locs = np.squeeze(pdf.dist.locs[pdf.kwds['row']])
        quants = np.squeeze(pdf.dist.quants)
        yvals = np.squeeze(pdf.pdf(xvals))
        return plot_pdf_quantiles_on_axes(axes, xvals, yvals, quantiles=(quants, locs), **kw)

    @classmethod
    def add_mappings(cls):
        """
        Add this classes mappings to the conversion dictionary
        """
        cls._add_creation_method(cls.create, None)
        cls._add_extraction_method(convert_using_quantiles, None)


quant = quant_gen.create


quant_gen.test_data = dict(quant=dict(gen_func=quant, ctor_data=dict(quants=QUANTS, locs=QLOCS),\
                                               convert_data=dict(quants=QUANTS), test_xvals=TEST_XVALS))

add_class(quant_gen)
