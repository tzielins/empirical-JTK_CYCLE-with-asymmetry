import numpy as np
import scipy.special as special

def tomcio(x):
    return x * 100


def farctanh(x):
    if x > 0.99:
        return np.arctanh(0.99)
    elif x < -0.99:
        return np.arctanh(-0.99)
    else:
        return np.arctanh(x)


def periodic(x):
    while x > 12:
        x = x - 24.
    while x <= -12:
        x = x + 24.
    return x


def pick_best_match(res):

    res = np.array(res)
    taus = res[:,0]
    #maxtau = max(taus)
    tau_mask = (max(taus)==taus)
    if np.sum(tau_mask)==1:
        ind = list(tau_mask).index(True)
        #print res[ind]
        return res[ind]

    res = res[tau_mask]
    phases = np.abs(res[:,3]-res[:,5])
    #print phases
    #minphasediff = min(phases)
    phasemask = (min(phases)==phases)
    if np.sum(phasemask)==1:
        ind = list(phasemask).index(True)
        return res[ind]

    res = res[phasemask]
    diffs = np.abs(res[:,4]-res[:,6])
    diffmask = (min(diffs)==diffs)
    if np.sum(diffmask)==1:
        ind = list(diffmask).index(True)
        return res[ind]

    ### If we've gotten down here everything has failed
    #print 'Ties remain...',res
    return res[np.random.randint(len(res))]


def kt(x, y, initial_lexsort=True):
    """
    Calculates Kendall's tau, a correlation measure for ordinal data.

    Kendall's tau is a measure of the correspondence between two rankings.
    Values close to 1 indicate strong agreement, values close to -1 indicate
    strong disagreement.  This is the tau-b version of Kendall's tau which
    accounts for ties.

    Parameters
    ----------
    x, y : array_like
        Arrays of rankings, of the same shape. If arrays are not 1-D, they will
        be flattened to 1-D.
    initial_lexsort : bool, optional
        Whether to use lexsort or quicksort as the sorting method for the
        initial sort of the inputs. Default is lexsort (True), for which
        `kendalltau` is of complexity O(n log(n)). If False, the complexity is
        O(n^2), but with a smaller pre-factor (so quicksort may be faster for
        small arrays).

    Returns
    -------
    Kendall's tau : float
       The tau statistic.
    p-value : float
       The two-sided p-value for a hypothesis test whose null hypothesis is
       an absence of association, tau = 0.

    Notes
    -----
    The definition of Kendall's tau that is used is::

      tau = (P - Q) / sqrt((P + Q + T) * (P + Q + U))

    where P is the number of concordant pairs, Q the number of discordant
    pairs, T the number of ties only in `x`, and U the number of ties only in
    `y`.  If a tie occurs for the same pair in both `x` and `y`, it is not
    added to either T or U.

    References
    ----------
    W.R. Knight, "A Computer Method for Calculating Kendall's Tau with
    Ungrouped Data", Journal of the American Statistical Association, Vol. 61,
    No. 314, Part 1, pp. 436-439, 1966.

    Examples
    --------
    >>> import scipy.stats as stats
    >>> x1 = [12, 2, 1, 12, 2]
    >>> x2 = [1, 4, 7, 1, 0]
    >>> tau, p_value = stats.kendalltau(x1, x2)
    >>> tau
    -0.47140452079103173
    >>> p_value
    0.24821309157521476

    """

    x = np.asarray(x).ravel()
    y = np.asarray(y).ravel()

    if not x.size or not y.size:
        return (np.nan, np.nan)  # Return NaN if arrays are empty

    n = np.int64(len(x))
    temp = list(range(n))  # support structure used by mergesort

    # this closure recursively sorts sections of perm[] by comparing
    # elements of y[perm[]] using temp[] as support
    # returns the number of swaps required by an equivalent bubble sort

    def mergesort(offs, length):

        exchcnt = 0
        if length == 1:
            return 0
        if length == 2:
            if y[perm[offs]] <= y[perm[offs + 1]]:
                return 0
            t = perm[offs]
            perm[offs] = perm[offs + 1]
            perm[offs + 1] = t
            return 1
        length0 = length // 2
        length1 = length - length0
        middle = offs + length0
        exchcnt += mergesort(offs, length0)
        exchcnt += mergesort(middle, length1)
        if y[perm[middle - 1]] < y[perm[middle]]:
            return exchcnt
        # merging
        i = j = k = 0
        while j < length0 or k < length1:
            if k >= length1 or (j < length0 and y[perm[offs + j]] <=
                                y[perm[middle + k]]):
                temp[i] = perm[offs + j]
                d = i - j
                j += 1
            else:
                temp[i] = perm[middle + k]
                d = (offs + i) - (middle + k)
                k += 1
            if d > 0:
                exchcnt += d
            i += 1
        perm[offs:offs + length] = temp[0:length]
        return exchcnt


    # initial sort on values of x and, if tied, on values of y
    if initial_lexsort:
        # sort implemented as mergesort, worst case: O(n log(n))
        perm = np.lexsort((y, x))
    else:
        # sort implemented as quicksort, 30% faster but with worst case: O(n^2)
        perm = list(range(n))
        perm.sort(key=lambda a: (x[a], y[a]))

    # compute joint ties
    first = 0
    t = 0
    for i in xrange(1, n):
        if x[perm[first]] != x[perm[i]] or y[perm[first]] != y[perm[i]]:
            t += ((i - first) * (i - first - 1)) // 2
            first = i
    t += ((n - first) * (n - first - 1)) // 2

    # compute ties in x
    first = 0
    u = 0
    for i in xrange(1, n):
        if x[perm[first]] != x[perm[i]]:
            u += ((i - first) * (i - first - 1)) // 2
            first = i
    u += ((n - first) * (n - first - 1)) // 2

    # count exchanges
    exchanges = mergesort(0, n)
    # compute ties in y after mergesort with counting
    first = 0
    v = 0
    for i in xrange(1, n):
        if y[perm[first]] != y[perm[i]]:
            v += ((i - first) * (i - first - 1)) // 2
            first = i
    v += ((n - first) * (n - first - 1)) // 2

    tot = (n * (n - 1)) // 2
    if tot == u or tot == v:
        return (np.nan, np.nan)  # Special case for all ties in both ranks

    # Prevent overflow; equal to np.sqrt((tot - u) * (tot - v))
    denom = np.exp(0.5 * (np.log(tot - u) + np.log(tot - v)))
    tau = ((tot - (v + u - t)) - 2.0 * exchanges) / denom

    # what follows reproduces the ending of Gary Strangman's original
    # stats.kendalltau() in SciPy
    svar = (4.0 * n + 10.0) / (9.0 * n * (n - 1))
    z = tau / np.sqrt(svar)
    prob = special.erfc(np.abs(z) / 1.4142136)

    return tau, prob


def get_matches(kkey,triple,d_ref,new_header):

    #print("K {} {}".format(type(kkey), kkey))
    #print("T {} {}".format(type(triple), triple))
    #print("d {} {}".format(type(d_ref), d_ref))
    #print("nh {} {}".format(type(new_header), new_header))
    #raise Exception("On purpose");

    reference = d_ref[tuple(triple)]
    period,phase,width = triple
    nadir = (phase+width)%period
    #print kkey
    #print reference
    reference = map(float,reference)
    kkey = map(float,kkey)
    tau,p = kt(reference,kkey)#generate_mod_series(reference,serie)
    #print period,phase,nadir,tau,p
    #print reference, kkey
    #print kt(map(float,reference),map(float,kkey))
    serie = map(float,list(kkey)    )
    p = p/2.0
    #tau = farctanh(tau)
    maxloc = new_header[serie.index(max(serie))]
    minloc = new_header[serie.index(min(serie))]
    #print tau
    r =  [tau,p,period,phase,nadir,maxloc,minloc]
    #print r
    if float(tau) < 0:
        #print r
        r = [float(np.abs(tau)),p,period,nadir,phase,maxloc,minloc]
        #print r
    #print r
    #print ''
    return r


def generate_base_reference(header, waveform="cosine", period = 24.,
                            phase = 0., width = 12.):
    """
    This will generate a waveform with a given phase and period based on the header,
    """

    ZTs = np.array(header, dtype=float)
    coef = 2.0 * np.pi / period
    w = width * coef
    tpoints = (ZTs - phase) * coef
    if waveform == 'cosine':

        def cosine(x, w):
            x = x % (2 * np.pi)
            w = w % (2 * np.pi)
            if x <= w:
                y = np.cos(x / (w / np.pi))
            elif x > w:
                y = np.cos((x + 2. * (np.pi - w)) * np.pi / (2 * np.pi - w))
            return y
        f_wav = cosine
    elif waveform == 'trough':

        def trough(x, w):
            x = x % (2 * np.pi)
            w = w % (2 * np.pi)
            if x <= w:
                y = 1 + -x / w
            elif x > w:
                y = (x - w) / (2 * np.pi - w)
            return y
        f_wav = trough

    reference = [f_wav(tpoint, w) for tpoint in tpoints]
    return reference


def make_references(new_header, triples, waveform='cosine'):  # ,period,phase,width):
    dref = {}
    # print new_header
    for triple in triples:
        period, phase, width = triple

        reference = generate_base_reference(new_header, waveform, period, phase, width)
        dref[(period, phase, width)] = reference
    return dref

def get_waveform_list(periods,phases,widths):
    lper = len(periods)
    lpha = len(phases)
    lwid = len(widths)
    #cdef np.ndarray
    triples = [] # np.zeros((1+int(lper*lpha*lwid/2),3))

    # print("T{}".format((int(lper*lpha*lwid/2),3)))
    k = 0
    for i,period in enumerate(periods):
        j = 0
        pairs = [] # [[0,0]]*(1+int(lpha*lwid/2))
        # print("P{}".format(int(lpha*lwid/2)))
        phases1 = [phase for phase in phases if phase <=period]
        widths1 = [width for width in widths if width < period]
        master_pairs = [[phase,(phase+width)%period] for phase in phases1 for width in widths1]
        #print len(master_pairs),master_pairs
        for phase in phases:
            if phase <= period:
                for width in widths:
                    if width < period:
                        nadir = (phase+width)%period
                        pair = [nadir,phase]
                        if pair not in pairs and pair[::-1] in master_pairs:
                            #pairs[j] = [phase,nadir]
                            #triples[k] = np.array([period,phase,width])
                            pairs.append([phase,nadir])
                            triples.append(np.array([period,phase,width]))
                            #print pairs[j]
                            j+=1
                            k+=1
    triples = np.array(triples,dtype=float)
    #triples = triples[:k,:]
    return triples

def get_best_match(serie,waveform,triples,dref,new_header):

    lamb_get_matches = lambda triple: get_matches(serie[1:],triple,dref,new_header)
    ### This 'res' is the array with the p-values we want
    res = np.array(map(lamb_get_matches,triples))
    r = pick_best_match(res)
    best = [serie[0],waveform,r[2],r[3],r[4],r[5],r[6],r[0],r[1]]
    #print best
    return best