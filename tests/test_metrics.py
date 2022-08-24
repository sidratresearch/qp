"""
Unit tests for PDF class
"""

import unittest
import qp
import numpy as np

from qp import test_funcs
from qp.utils import epsilon


class MetricTestCase(unittest.TestCase):
    """ Tests for the metrics """

    def setUp(self):
        """
        Make any objects that are used in multiple tests.
        """
        self.ens_n = test_funcs.build_ensemble(qp.stats.norm_gen.test_data['norm'])  #pylint: disable=no-member
        self.ens_n_shift = test_funcs.build_ensemble(qp.stats.norm_gen.test_data['norm_shifted'])  #pylint: disable=no-member

        locs = 2* (np.random.uniform(size=(10,1))-0.5)
        scales = 1 + 0.2*(np.random.uniform(size=(10,1))-0.5)
        self.ens_n_plus_one = qp.Ensemble(qp.stats.norm, data=dict(loc=locs, scale=scales)) #pylint: disable=no-member

        bins = np.linspace(-5, 5, 11)
        self.ens_s = self.ens_n.convert_to(qp.spline_gen, xvals=bins, method="xy")

    def tearDown(self):
        """ Clean up any mock data files created by the tests. """

    def test_kld(self):
        """ Test the calculate_kld method """
        kld = qp.metrics.calculate_kld(self.ens_n, self.ens_n_shift, limits=(0.,2.5))
        assert np.all(kld == 0.)

    def test_kld_alternative_ensembles(self):
        """ Test the calculate_kld method against different types of ensembles """
        bins = np.linspace(-5, 5, 11)
        quants = np.linspace(0.01, 0.99, 7)

        ens_h = self.ens_n[0].convert_to(qp.hist_gen, bins=bins)
        ens_h_shift = self.ens_n_shift[0].convert_to(qp.hist_gen, bins=bins)

        ens_i = self.ens_n[0].convert_to(qp.interp_gen, xvals=bins)
        ens_i_shift = self.ens_n_shift[0].convert_to(qp.interp_gen, xvals=bins)

        ens_s = self.ens_n[0].convert_to(qp.spline_gen, xvals=bins, method="xy")
        ens_s_shift = self.ens_n_shift[0].convert_to(qp.spline_gen, xvals=bins, method="xy")

        ens_q = self.ens_n[0].convert_to(qp.quant_piecewise_gen, quants=quants)
        ens_q_shift = self.ens_n_shift[0].convert_to(qp.quant_piecewise_gen, quants=quants)

        kld_histogram = qp.metrics.calculate_kld(ens_h, ens_h_shift, limits=(0.,2.5))
        assert np.all(kld_histogram == 0.)

        kld_interp = qp.metrics.calculate_kld(ens_i, ens_i_shift, limits=(0.,2.5))
        assert np.all(kld_interp == 0.)

        kld_spline = qp.metrics.calculate_kld(ens_s, ens_s_shift, limits=(0.,2.5))
        assert np.all(kld_spline == 0.)

        kld_quants = qp.metrics.calculate_kld(ens_q, ens_q_shift, limits=(0.,2.5))
        assert np.all(kld_quants == 0.)

    def test_kld_different_shapes(self):
        """ Ensure that the kld function fails when trying to compare ensembles of different sizes. """
        with self.assertRaises(ValueError) as context:
            qp.metrics.calculate_kld(self.ens_n, self.ens_n_plus_one, limits=(0.,2.5))

        self.assertTrue('Cannot calculate KLD between two ensembles with different shapes' in str(context.exception))

    def test_broken_kld(self):
        """ Test to see if the calculate_kld function responds appropriately to negative results """
        kld = qp.metrics.calculate_kld(self.ens_n, self.ens_s, limits=(0.,2.5))

        assert np.all(kld == epsilon)
        

    def test_rmse(self):
        """ Test the calculate_rmse method """
        rmse = qp.metrics.calculate_rmse(self.ens_n, self.ens_n_shift, limits=(0.,2.5))
        assert np.all(rmse == 0.)

    def test_rmse_alternative_ensembles(self):
        """ Test the calculate_rmse method against different types of ensembles """
        bins = np.linspace(-5, 5, 11)
        quants = np.linspace(0.01, 0.99, 7)

        ens_h = self.ens_n[0].convert_to(qp.hist_gen, bins=bins)
        ens_h_shift = self.ens_n_shift[0].convert_to(qp.hist_gen, bins=bins)

        ens_i = self.ens_n[0].convert_to(qp.interp_gen, xvals=bins)
        ens_i_shift = self.ens_n_shift[0].convert_to(qp.interp_gen, xvals=bins)

        ens_s = self.ens_n[0].convert_to(qp.spline_gen, xvals=bins, method="xy")
        ens_s_shift = self.ens_n_shift[0].convert_to(qp.spline_gen, xvals=bins, method="xy")

        ens_q = self.ens_n[0].convert_to(qp.quant_piecewise_gen, quants=quants)
        ens_q_shift = self.ens_n_shift[0].convert_to(qp.quant_piecewise_gen, quants=quants)

        rmse_histogram = qp.metrics.calculate_rmse(ens_h, ens_h_shift, limits=(0.,2.5))
        assert np.all(rmse_histogram == 0.)

        rmse_interp = qp.metrics.calculate_rmse(ens_i, ens_i_shift, limits=(0.,2.5))
        assert np.all(rmse_interp == 0.)

        rmse_spline = qp.metrics.calculate_rmse(ens_s, ens_s_shift, limits=(0.,2.5))
        assert np.all(rmse_spline == 0.)

        rmse_quants = qp.metrics.calculate_rmse(ens_q, ens_q_shift, limits=(0.,2.5))
        assert np.all(rmse_quants == 0.)

    def test_rmse_different_shapes(self):
        """ Ensure that the rmse function fails when trying to compare ensembles of different sizes. """
        with self.assertRaises(ValueError) as context:
            qp.metrics.calculate_rmse(self.ens_n, self.ens_n_plus_one, limits=(0.,2.5))

        self.assertTrue('Cannot calculate RMSE between two ensembles with different shapes' in str(context.exception))

    def test_rpbe(self):
        """ Test the risk_based_point_estimate method """
        rpbe = qp.metrics.risk_based_point_estimate(self.ens_n, limits=(0.,2.5))
        assert np.all(rpbe >= 0.)
        assert np.all(rpbe <= 2.5)

    def test_rpbe_alternative_ensembles(self):
        """ Test the risk_based_point_estimate method against different types of ensembles """
        bins = np.linspace(-5, 5, 11)
        quants = np.linspace(0.01, 0.99, 7)

        ens_h = self.ens_n[0].convert_to(qp.hist_gen, bins=bins)
        ens_i = self.ens_n[0].convert_to(qp.interp_gen, xvals=bins)
        ens_s = self.ens_n[0].convert_to(qp.spline_gen, xvals=bins, method="xy")
        ens_q = self.ens_n[0].convert_to(qp.quant_piecewise_gen, quants=quants)
        ens_m = self.ens_n[0].convert_to(qp.mixmod_gen, samples=1000, ncomps=3)

        rpbe_histogram = qp.metrics.risk_based_point_estimate(ens_h, limits=(0.,2.5))
        assert np.all(rpbe_histogram >= 0.)
        assert np.all(rpbe_histogram <= 2.5)

        rpbe_interp = qp.metrics.risk_based_point_estimate(ens_i, limits=(0.,2.5))
        assert np.all(rpbe_interp >= 0.)
        assert np.all(rpbe_interp <= 2.5)

        rpbe_spline = qp.metrics.risk_based_point_estimate(ens_s, limits=(0.,2.5))
        assert np.all(rpbe_spline >= 0.)
        assert np.all(rpbe_spline <= 2.5)

        rpbe_quants = qp.metrics.risk_based_point_estimate(ens_q, limits=(0.,2.5))
        assert np.all(rpbe_quants >= 0.)
        assert np.all(rpbe_quants <= 2.5)

        rpbe_mixmod = qp.metrics.risk_based_point_estimate(ens_m, limits=(0.,2.5))
        assert np.all(rpbe_mixmod >= 0.)
        assert np.all(rpbe_mixmod <= 2.5)
        

    def test_quick_rpbe(self):
        """ Test the quick_rpbe method """
        rpbe = qp.metrics.quick_rbpe(self.ens_n[0], limits=(0.,2.5))
        assert np.all(rpbe >= 0.)
        assert np.all(rpbe <= 2.5)

    def test_quick_rpbe_multiple_pdfs(self):
        """ Ensure that the quick_rpbe function fails when trying to evaluate an ensemble with more than one pdf. """
        with self.assertRaises(ValueError) as context:
            qp.metrics.quick_rbpe(self.ens_n, limits=(0.,2.5))

        error_msg = 'quick_rbpe only handles Ensembles with a single PDF'
        self.assertTrue(error_msg in str(context.exception))


if __name__ == '__main__':
    unittest.main()
