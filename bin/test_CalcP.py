from CalcP import *
import py_accessories
from numpy.testing import assert_array_equal, assert_allclose


def test_empP():

    taus = [0, 1, 0.2, 0.5]
    emps = [0.1, 0.2, 0.3, 0.4, 0.6]

    exp = [ 6.0/6.0, 1/6.0, 5.0/6.0, 2/6.0 ]

    res = empP(taus, emps)

    assert_array_equal(exp, res)



