import numpy.testing as np_testing
import scipy.stats

from pymanopt.manifolds import PSDFixedRank

from ._manifold_tests import ManifoldTestCase


class TestPSDFixedRankManifold(ManifoldTestCase):
    def setUp(self):
        self.n = 50
        self.k = 10
        self.manifold = PSDFixedRank(self.n, self.k)

        super().setUp()

    # def test_dim(self):

    # def test_typical_dist(self):

    def test_dist(self):
        point_a = self.manifold.random_point()
        Q = scipy.stats.ortho_group.rvs(self.k)
        point_b = point_a @ Q
        np_testing.assert_almost_equal(self.manifold.dist(point_a, point_b), 0)

    # def test_inner_product(self):

    # def test_projection(self):

    # def test_euclidean_to_riemannian_hessian(self):

    # def test_retraction(self):

    def test_euclidean_to_riemannian_gradient_from_cost(self):
        self.run_gradient_test()

    # def test_norm(self):

    # def test_random_point(self):

    # def test_random_tangent_vector(self):

    # def test_transport(self):

    def test_exp_log_inverse(self):
        s = self.manifold
        X = s.random_point()
        Y = s.random_point()
        Yexplog = s.exp(X, s.log(X, Y))
        np_testing.assert_almost_equal(s.dist(Y, Yexplog), 0)

    def test_log_exp_inverse(self):
        s = self.manifold
        X = s.random_point()
        U = s.random_tangent_vector(X)
        Ulogexp = s.log(X, s.exp(X, U))
        np_testing.assert_almost_equal(s.norm(X, U - Ulogexp), 0)

    # def test_pair_mean(self):
    # s = self.manifold
    # X = s.random_point()
    # Y = s.random_point()
    # Z = s.pair_mean(X, Y)
    # np_testing.assert_array_almost_equal(s.dist(X, Z), s.dist(Y, Z))
