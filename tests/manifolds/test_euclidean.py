import autograd.numpy as np
from numpy import testing as np_testing

from pymanopt.manifolds import Euclidean

from ._manifold_tests import ManifoldTestCase


class TestEuclideanManifold(ManifoldTestCase):
    def setUp(self):
        self.m = m = 10
        self.n = n = 5
        self.manifold = Euclidean(m, n)

        super().setUp()

    def test_dim(self):
        assert self.manifold.dim == self.m * self.n

    def test_typical_dist(self):
        np_testing.assert_almost_equal(
            self.manifold.typical_dist, np.sqrt(self.m * self.n)
        )

    def test_dist(self):
        e = self.manifold
        x, y = np.random.normal(size=(2, self.m, self.n))
        np_testing.assert_almost_equal(e.dist(x, y), np.linalg.norm(x - y))

    def test_inner_product(self):
        e = self.manifold
        x = e.random_point()
        y = e.random_tangent_vector(x)
        z = e.random_tangent_vector(x)
        np_testing.assert_almost_equal(np.sum(y * z), e.inner_product(x, y, z))

    def test_projection(self):
        e = self.manifold
        x = e.random_point()
        u = e.random_tangent_vector(x)
        np_testing.assert_allclose(e.projection(x, u), u)

    def test_euclidean_to_riemannian_hessian(self):
        e = self.manifold
        x = e.random_point()
        u = e.random_tangent_vector(x)
        egrad, ehess = np.random.normal(size=(2, self.m, self.n))
        np_testing.assert_allclose(
            e.euclidean_to_riemannian_hessian(x, egrad, ehess, u), ehess
        )

    def test_retraction(self):
        e = self.manifold
        x = e.random_point()
        u = e.random_tangent_vector(x)
        np_testing.assert_allclose(e.retraction(x, u), x + u)

    def test_euclidean_to_riemannian_gradient(self):
        e = self.manifold
        x = e.random_point()
        u = e.random_tangent_vector(x)
        np_testing.assert_allclose(e.euclidean_to_riemannian_gradient(x, u), u)

    def test_euclidean_to_riemannian_gradient_from_cost(self):
        self.run_gradient_test()

    def test_norm(self):
        e = self.manifold
        x = e.random_point()
        u = np.random.normal(size=(self.m, self.n))
        np_testing.assert_almost_equal(np.sqrt(np.sum(u**2)), e.norm(x, u))

    def test_random_point(self):
        e = self.manifold
        x = e.random_point()
        y = e.random_point()
        assert np.shape(x) == (self.m, self.n)
        assert np.linalg.norm(x - y) > 1e-6

    def test_random_tangent_vector(self):
        e = self.manifold
        x = e.random_point()
        u = e.random_tangent_vector(x)
        v = e.random_tangent_vector(x)
        assert np.shape(u) == (self.m, self.n)
        np_testing.assert_almost_equal(np.linalg.norm(u), 1)
        assert np.linalg.norm(u - v) > 1e-6

    def test_transport(self):
        e = self.manifold
        x = e.random_point()
        y = e.random_point()
        u = e.random_tangent_vector(x)
        np_testing.assert_allclose(e.transport(x, y, u), u)

    def test_exp_log_inverse(self):
        s = self.manifold
        X = s.random_point()
        Y = s.random_point()
        Yexplog = s.exp(X, s.log(X, Y))
        np_testing.assert_array_almost_equal(Y, Yexplog)

    def test_log_exp_inverse(self):
        s = self.manifold
        X = s.random_point()
        U = s.random_tangent_vector(X)
        Ulogexp = s.log(X, s.exp(X, U))
        np_testing.assert_array_almost_equal(U, Ulogexp)

    def test_pair_mean(self):
        s = self.manifold
        X = s.random_point()
        Y = s.random_point()
        Z = s.pair_mean(X, Y)
        np_testing.assert_array_almost_equal(s.dist(X, Z), s.dist(Y, Z))
