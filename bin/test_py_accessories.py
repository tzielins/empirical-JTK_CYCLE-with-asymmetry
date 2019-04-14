from py_accessories import *
from numpy.testing import assert_array_equal, assert_allclose

def test_tomcio():
    assert tomcio(3) == 300

def test_farctanh():

    assert farctanh(2) == 2.6466524123622457
    assert farctanh(1) == 2.6466524123622457
    assert farctanh(-1) == -2.6466524123622457
    assert farctanh(0) == 0
    assert farctanh(0.5) == 0.5493061443340548

def test_periodic():

    assert periodic(0) == 0
    assert periodic(-1.1) == -1.1
    assert periodic(12) == 12.0
    assert periodic(12.0) == 12.0
    assert periodic(24) == 0
    assert periodic(24.0) == 0
    assert periodic(25.1) == 1.1000000000000014
    assert periodic(-12.0) == 12.0
    assert periodic(-12.1) == 11.9
    assert periodic(50) == 2.0
    assert periodic(-60) == 12


def test_pick_best_match():

    #   tau,  ?,  ?, ph1, d1, ph2, d2
    tab = [
        [0.5, 24, 24, 1,  2.1, 3,  0.1 ]
    ]

    exp = [0.5, 24, 24, 1,  2.1, 3,  0.1 ]
    best = pick_best_match(tab)
    assert_array_equal(best,exp)


    tab = [
        [0.1, 24, 24, 1,  2.1, 3,  0.1 ],
        [0.6, 24, 24, 1,  2.1, 3,  0.1 ],
        [0.4, 24, 24, 1,  2.1, 3,  0.1 ]
    ]

    exp = [0.6, 24, 24, 1,  2.1, 3,  0.1 ]
    best = pick_best_match(tab)
    assert_array_equal(best,exp)

    tab = [
        [0.1, 24, 24, 1,  2.1, 3,  0.1 ],
        [0.1, 25, 24, 4,  2.1, 2,  0.1 ],
        [0.1, 26, 24, 1.5,  2.1, 3,  0.1 ]
    ]

    exp = [0.1, 26, 24, 1.5,  2.1, 3,  0.1 ]
    best = pick_best_match(tab)
    assert_array_equal(best,exp)

def test_kt():

    x = [12, 2, 1, 12, 2]
    y = [1, 4, 7, 1, 0]

    tau, p_value = kt(x, y)
    assert tau == -0.47140452079103173
    assert p_value == 0.24821309157521476

def test_get_matches():

    kkey = [1, 4, 7, 1, 0]
    triple = [24.,  0.,  2.]

    d_ref = { tuple(triple): [12, 2, 1, 12, 2]}
    new_header = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0, 46.0]

    res = get_matches(kkey,triple,d_ref,new_header)

    assert res[0] == 0.47140452079103173
    assert res[1] == 0.24821309157521476 / 2.0
    assert res[2] == 24
    assert res[3] == 2
    assert res[4] == 0
    assert res[5] == 4
    assert res[6] == 8

def test_generate_base_reference():
    header = [0., 2., 8., 16]
    waveform = "cosine"
    period = 24.
    phase = 1.
    width = 10.

    res = generate_base_reference(header,waveform,period,phase,width)

    exp = [ 0.974928,  0.951057, -0.587785, -0.433884]
    assert_allclose(res, exp, rtol=1e-5, atol=0)

    waveform = 'trough'
    res2 = generate_base_reference(header,waveform,period,phase,width)

    exp = [0.928571, 0.9     , 0.3     , 0.357143]
    assert_allclose(res2, exp, rtol=1e-5, atol=0)


def test_make_references():
    new_header = [0., 2., 8., 16]
    triples = [[24, 1, 10], [26, 1, 3]]
    waveform = 'cosine'

    res = make_references(new_header, triples, waveform)
    assert len(res) == 2;

    exp = [ 0.974928,  0.951057, -0.587785, -0.433884]
    assert_allclose(res[(24,1,10)], exp, rtol=1e-5, atol=0)


def test_get_waveform_list():
    periods = [24]
    phases = [1]
    widths = [4]

    res = get_waveform_list(periods,phases,widths)

    assert_array_equal(res,[(24,1,4)])

    periods = [24, 26]
    phases = [1, 2]
    widths = [4]

    res = get_waveform_list(periods,phases,widths)
    assert len(res) == 4