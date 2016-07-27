# Fixed Income Mathematics

# 1. Time Value of Money

# 1(a) Future Value


def fv(p, i, n, m=1):
    """ future_value = principal * ((1 + interest_rate) ** number_periods) """
    """ assumes 1 compound period, but can be changed """
    return p * ((1 + (i / m)) ** (n * m))


def fv_annu(a, i, n, m=1):
    """ future value of an annuity """
    """ assumes one payment per period, but can be changed """
    return a * ((((1 + (i / m)) ** (n * m)) - 1) / (i / m))

# 1(b) Present Value


def pv(f, i, n, m=1):
    """ present_value = future_value * (1 / ((1 + interest_rate) ** number_periods)) """
    return f * (1 / ((1 + (i / m)) ** (n * m)))


def pv_series(f, i, n, m=1):
    """ present value of a series of future values """
    value = 0
    period = 1
    if type(i) == list:
        """ returns PV of a series of FVs (in a list) at unequal rates (in a list) """
        z = list(zip(f, i))
        for x in z:
            if period <= n:
                value += pv(x[0], x[1], period, m)
            period += 1
    elif type(f) == list:
        """ returns PV of a series of FVs (in a list) """
        for v in f:
            if period <= n:
                value += pv(v, i, period, m)
            period += 1
    else:
        """ attempts to return PV of FV if no lists are found """
        value = pv(f, i, n, m)
    return value


def pv_annu(a, i, n, m=1):
    """ present value of an annuity """
    return a * ((1 - (1 / ((1 + (i / m)) ** (n * m)))) / (i / m))


def pv_perp(a, i, m=1):
    """ present value of a perpetuity """
    return a / (i / m)

# 1(c) Yield -- Internal Rate of Return


def yield_rate(cf, p, n):
    """ yield = ((cash_flow_from_investment / amount_invested) ** (1 / periods_invested)) - 1 """
    return ((cf / p) ** (1 / n)) - 1


def yield_eff_annu(i, m):
    """ returns the effective annual yield, where i is periodic interest rate; m is annual frequency """
    return ((1 + i) ** m) - 1


def periodic_rate(y, m):
    """ returns the periodic interest rate, where y is annual yield; m is frequency of returned rate """
    return ((1 + y) ** (1 / m)) - 1

# 2. Bond Pricing and Return Analysis

# 2(a) The Price of a Bond


def coupon(par, coup_rate, m=2):
    return par * (coup_rate / m)


def bond_price(par, coup_rate, req_rate, n, m=2):
    """ price of a bond, given its par value, coupon rate, required rate of return, and tenor """
    """ assumes semi-annual payments, but can be changed """
    c = coupon(par, coup_rate, m)
    return pv_annu(c, req_rate, n, m) + pv(par, req_rate, n, m)


# 2(b) Conventional Yield Measures for Bonds


def yield_current(par, coup_rate, p):
    """ relates the annual coupon interest (ci = par * coup_rate) to the market price (p) """
    return (par * coup_rate) / p


def yield_maturity(price, par, cr, rr, n, m=2, accuracy=50):
    """ finds YTM by trial and error, within the bounds of price plus/minus an accuracy factor, default at 50 """
    bp_est = bond_price(par, cr, rr, n, m)
    if price - accuracy <= bp_est <= price + accuracy:
        return round(rr, 5)
    elif bp_est < price - accuracy:
        return yield_maturity(price, par, cr, rr - .005, n, m, accuracy)
    else:
        return yield_maturity(price, par, cr, rr + .005, n, m, accuracy)


def port_yield_wa(*args):
    """ portfolio yield weighted average """
    """ arguments in format of [coupon rate, maturity, par value, market value, YTM] """
    mkt_val = 0
    pywa = 0
    for bond in args:
        mkt_val += bond[3]
    for bond in args:
        bond.append(bond[3] / mkt_val)
        bond.append(bond[5] * bond[4])
    for bond in args:
        pywa += bond[6]
    return round(pywa, 4)


# 2(c) Potential Sources of Dollar Return


def ci_plus_ioi(par, coup_rate, reinv_rate, n, m=2):
    """ coupon interest plus interest on interest """
    return (coupon(par, coup_rate, m)) * ((((1 + (reinv_rate / m)) ** (n * m)) - 1) / (reinv_rate / m))


def int_on_int(par, coup_rate, reinv_rate, n, m=2):
    """ interest on interest """
    return ci_plus_ioi(par, coup_rate, reinv_rate, n, m) - (n * m * coupon(par, coup_rate, m))


def ioi_pdr(par, coup_rate, reinv_rate, n, m=2):
    """ interest on interest as a percentage of total dollar return """
    return round(int_on_int(par, coup_rate, reinv_rate, n, m) / ci_plus_ioi(par, coup_rate, reinv_rate, n, m), 4)


# 2(d) Total Return


def total_return(par, coup_rate, reinv_rate, n, price=1000, m=2):
    """ total return on a bond held to maturity """
    future_amt = ci_plus_ioi(par, coup_rate, reinv_rate, n, m) + par
    return_pct = (((future_amt / price) ** (1 / (n * m))) - 1) * m
    return future_amt, round(return_pct, 4)


def total_return_limit(par, coup_rate, reinv_rate, ytm_rate, n_full, n_used, price=1000, m=2):
    """ total return on a bond sold prior to maturity """
    ci_and_ioi = ci_plus_ioi(par, coup_rate, reinv_rate, n_used, m)
    pv_coup_int = pv_annu(coupon(par, coup_rate, m), ytm_rate, n_full - n_used, m)
    pv_maturity = pv(par, ytm_rate, n_full - n_used, m)
    future_amt = ci_and_ioi + pv_coup_int + pv_maturity
    return_pct = (((future_amt / price) ** (1 / (n_used * m))) - 1) * m
    return future_amt, round(return_pct, 4)


# 3. Bond Price Volatility

# 3(a) Price Volatility of Option-Free Bonds

def bp_vol(par, coup_rate, req_rate, yield_bps_chg, n, m=2):
    """ volatility of bond price, given +/- bps change in required yield """
    new = bond_price(par, coup_rate, req_rate + (yield_bps_chg / 10000), n, m)
    old = bond_price(par, coup_rate, req_rate, n, m)
    return round((new - old) / old, 4)


# 3(b) Price Volatility Measures:  PVBP and YV of a Price Change

