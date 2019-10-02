
import numpy as np
import statsmodels.stats.multitest as ssm

def _ecdf(x):
    '''no frills empirical cdf used in fdrcorrection
    '''
    nobs = len(x)
    return np.arange(1,nobs+1)/float(nobs)

def fdr(pvals, alpha=0.05, is_sorted=False):

    pvals = np.asarray(pvals)

    if not is_sorted:
        pvals_sortind = np.argsort(pvals)
        pvals_sorted = np.take(pvals, pvals_sortind)
    else:
        pvals_sorted = pvals  # alias

    ecdffactor = _ecdf(pvals_sorted)

    # reject = pvals_sorted <= ecdffactor*alpha
    #if reject.any():
    #    rejectmax = max(np.nonzero(reject)[0])
    #    reject[:rejectmax] = True

    pvals_corrected_raw = pvals_sorted / ecdffactor
    pvals_corrected = np.minimum.accumulate(pvals_corrected_raw[::-1])[::-1]

    # del pvals_corrected_raw
    pvals_corrected[pvals_corrected>1] = 1
    if not is_sorted:
        pvals_corrected_ = np.empty_like(pvals_corrected)
        pvals_corrected_[pvals_sortind] = pvals_corrected
        del pvals_corrected
        #reject_ = np.empty_like(reject)
        #reject_[pvals_sortind] = reject
        #return reject_, pvals_corrected_
    else:
        return pvals_corrected, pvals_corrected_raw

def test_test():

    mmax = 12
    assert mmax == 12

def test_fdr_output():

    vals = [0.001, 0.0012, 0.0015, 0.002, 0.0021, 0.0029, 0.003, 0.004, 0.005, 0.0055, 0.0056, 0.0057, 0.01, 0.01, 0.012]

    pvals_corrected, raw = fdr(vals, is_sorted= True)

    print(pvals_corrected)
    print('raw')
    print(raw)
    print('raw-1')
    print(raw[::-1])
    print('raw acc')
    print(np.minimum.accumulate(raw[::-1]))
    print(np.minimum.accumulate(raw[::-1])[::-1])

    exp = [0.0063,     0.0063,     0.0063,     0.0063,     0.0063,     0.00642857,
     0.00642857, 0.007125,   0.007125,   0.007125,   0.007125,   0.007125,
     0.01071429, 0.01071429, 0.012]
    # exp = [0.001, 0.0012, 0.0015, 0.002, 0.0021, 0.0029, 0.003, 0.004, 0.005, 0.0055, 0.0056, 0.0057, 0.01, 0.01, 0.012]

    #assert list(pvals_corrected) == list(exp)
    np.testing.assert_allclose(exp, pvals_corrected, rtol=1e-6)

    reject2, pvals_corrected2, alphacSidak2, alphacBonf2 =ssm.multipletests(vals, method='fdr_bh')
    np.testing.assert_allclose(pvals_corrected2, pvals_corrected, rtol=1e-6)

    assert list(pvals_corrected) == list(pvals_corrected2)
    #assert False

def test_ecdf():

    vals = [0.001, 0.0012, 0.0015, 0.002, 0.0021, 0.0029, 0.003, 0.004, 0.005, 0.0055, 0.0056, 0.0057, 0.01, 0.01, 0.012]
    res = _ecdf(vals)
    print(res)

    exp = [1.0/15.0, 2.0/15.0, 3.0/15.0, 4.0/15.0, 5.0/15.0, 6.0/15.0, 7.0/15.0, 8.0/15.0,
           9.0/15.0, 10.0/15.0, 11.0/15.0, 12.0/15.0,  13.0/15.0, 14.0/15.0, 15.0/15.0,]

    np.testing.assert_allclose(res, exp, rtol=1e-6)

def test_ssm_multipletests():

    vals = [0.001, 0.1012, 0.0015, 0.002, 0.00021, 0.0029, 0.0015, 0.013, 0.0004]


    exp =  [0.0027,     0.1012,     0.0027,     0.003,      0.0018,     0.00372857,
            0.0027,     0.014625,   0.0018    ]

    reject2, pvals_corrected2, alphacSidak2, alphacBonf2 =ssm.multipletests(vals, method='fdr_bh')

    print(pvals_corrected2)
    np.testing.assert_allclose(pvals_corrected2, exp, rtol=1e-6)

    # assert False

def test_ssm_multipletests2():

    vals = [0.001, 0.001, 0.02, 0.021, 0.01]


    exp =  [0.0025,     0.0025,     0.021,      0.021 ,     0.01666667    ]

    reject2, pvals_corrected2, alphacSidak2, alphacBonf2 =ssm.multipletests(vals, method='fdr_bh')

    print(pvals_corrected2)
    np.testing.assert_allclose(pvals_corrected2, exp, rtol=1e-6)
