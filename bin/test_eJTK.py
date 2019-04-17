from eJTK import *
import py_accessories
from numpy.testing import assert_array_equal, assert_allclose


def test_analyse_serie():
    waveform = 'cosine'
    periods = [24.0]
    phases = [0., 2., 4., 6., 8., 10., 12., 14., 16., 18., 20., 22. ]
    widths = [2., 4., 6., 8., 10., 12., 14., 16., 18., 20., 22. ]

    zts = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46]
    serie = [0, 11.107065893,	10.9211912641,	10.4284953962,	10.0221371518,	9.56233368036,	9.16896033359,	8.90766774023,
             9.13833340962,	9.31200433802,	9.9778723997,	10.5917027748,	11.0382275396,	11.1006004486,	10.8794966822,
             10.5669050707, 9.86872396309,	9.41080481503,	8.97557609507,	8.96361955699,	9.23074455334,	9.64306081922,
             9.94917580124,	10.5906506647,	10.7983645048]

    triples = py_accessories.get_waveform_list(periods, phases, widths)
    dref = py_accessories.make_references(zts, triples, waveform)

    out = analyse_serie(serie, zts, waveform, triples, dref)
    assert out is not None

    print("{}".format(out))
    assert out[0] == 1
    assert out[1] == 'cosine'
    assert out[2] == 24.0
    assert out[14] == 0.8519551539622261
    assert out[15] == 2.7301861885389218e-09
    assert out[16] == 1.8019228844356883e-07

def test_analyse_set():

    assert analyse_set is not None

