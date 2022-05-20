import numpy as np
import scipy.linalg


def multitransp(A):
    """Vectorized matrix transpose.

    A is assumed to be an array containing M matrices, each of which has
    dimension N x P.
    That is, A is an M x N x P array. Multitransp then returns an array
    containing the M matrix transposes of the matrices in A, each of which will
    be P x N.
    """
    if A.ndim == 2:
        return A.T
    return np.transpose(A, (0, 2, 1))


def multihconj(A):
    """Vectorized matrix conjugate transpose."""
    return np.conjugate(multitransp(A))


def multisym(A):
    """Vectorized matrix symmetrization.

    Given an array ``A`` of matrices (represented as an array of shape ``(k, n,
    n)``), returns a version of ``A`` with each matrix symmetrized, i.e.,
    every matrix ``A[i]`` satisfies ``A[i] == A[i].T``.
    """
    return 0.5 * (A + multitransp(A))


def multiskew(A):
    """Vectorized matrix skew-symmetrization.

    Similar to :func:`multisym`, but returns an array where each matrix
    ``A[i]`` is skew-symmetric, i.e., the components of ``A`` satisfy ``A[i] ==
    -A[i].T``.
    """
    return 0.5 * (A - multitransp(A))


def multieye(k, n):
    """Array of ``k`` ``n x n`` identity matrices."""
    return np.tile(np.eye(n), (k, 1, 1))


def multilogm(A, *, positive_definite=False):
    """Vectorized matrix logarithm."""
    if not positive_definite:
        return np.vectorize(scipy.linalg.logm, signature="(m,m)->(m,m)")(A)

    w, v = np.linalg.eigh(A)
    w = np.expand_dims(np.log(w), axis=-1)
    logmA = v @ (w * multihconj(v))
    if np.isrealobj(A):
        return np.real(logmA)
    return logmA


def multiexpm(A, *, symmetric=False):
    """Vectorized matrix exponential."""
    if not symmetric:
        return np.vectorize(scipy.linalg.expm, signature="(m,m)->(m,m)")(A)

    w, v = np.linalg.eigh(A)
    w = np.expand_dims(np.exp(w), axis=-1)
    expmA = v @ (w * multihconj(v))
    if np.isrealobj(A):
        return np.real(expmA)
    return expmA


def multiqr(A):
    """Vectorized QR decomposition."""
    q, r = np.vectorize(np.linalg.qr, signature="(m,n)->(m,k),(k,n)")(A)

    # Compute signs or unit-modulus phase of entries of diagonal of r.
    diagonal = np.diagonal(r, axis1=-2, axis2=-1).copy()
    diagonal[diagonal == 0] = 1
    s = diagonal / np.abs(diagonal)

    if A.ndim == 3:
        s = np.expand_dims(s, axis=1)
    q = q * s
    r = multitransp(multitransp(r) * np.conjugate(s))
    return q, r
