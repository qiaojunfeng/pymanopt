import numpy as np
import numpy.testing as np_testing
from nose2.tools import params

import pymanopt
from pymanopt.optimizers import ConjugateGradient

from .._test import TestCase


class TestConjugateGradient(TestCase):
    def setUp(self):
        n = 32
        matrix = np.random.normal(size=(n, n))
        matrix = 0.5 * (matrix + matrix.T)

        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        self.dominant_eigenvector = eigenvectors[:, np.argmax(eigenvalues)]

        self.manifold = manifold = pymanopt.manifolds.Sphere(n)

        @pymanopt.function.autograd(manifold)
        def cost(point):
            return -point.T @ matrix @ point

        self.problem = pymanopt.Problem(manifold, cost)

    @params(
        "FletcherReeves",
        "HagerZhang",
        "HestenesStiefel",
        "PolakRibiere",
        "LiuStorey",
    )
    def test_beta_rules(self, beta_rule):
        optimizer = ConjugateGradient(beta_rule=beta_rule, verbosity=0)
        result = optimizer.run(self.problem)
        estimated_dominant_eigenvector = result.point
        if np.sign(self.dominant_eigenvector[0]) != np.sign(
            estimated_dominant_eigenvector[0]
        ):
            estimated_dominant_eigenvector = -estimated_dominant_eigenvector
        np_testing.assert_allclose(
            self.dominant_eigenvector,
            estimated_dominant_eigenvector,
            atol=1e-6,
        )

    def test_beta_invalid_rule(self):
        with self.assertRaises(ValueError):
            ConjugateGradient(beta_rule="SomeUnknownBetaRule")
