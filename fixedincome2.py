import pandas as pd
import scipy.optimize as opt


class TVM:
    def __init__(self, cf, r, n, m=1, g=0, m_precision=2, p_precision=4, series=0):
        self.series = series

        if self.series == 1:
            self.cf = cf[0]
            self.r = r
        elif self.series == 2:
            self.cf = cf[0]
            self.r = r[0]
        else:
            self.cf = cf
            self.r = r

        self.n = n
        self.m = m
        self.g = g

        self.r_m = self.r / m
        self.n_m = n * m
        self.g_m = g / m

        self.m_precision = m_precision
        self.p_precision = p_precision

        self.fv = self.future_value()
        self.fv_a = self.annuity()
        self.fv_a_pmt = self.find_pmt()
        self.fv_grad = self.gradient()
        self.fv_grow = round(self.inc_dec()[0], self.m_precision)
        self.fv_p = self.fv_a

        self.pv = self.present_value()
        self.pv_a = round(self.annuity() / self.calc(), self.m_precision)
        self.pv_a_pmt = round(self.find_pmt() * self.calc(), self.m_precision)
        self.pv_grad = round(self.gradient() * self.calc(), self.m_precision)
        self.pv_grow = round(self.inc_dec()[1], self.m_precision)
        self.pv_p = self.cf / self.r_m

        self.pmt_grad = self.find_grad()

        if self.series != 0:
            """ lets calculations happen as if cf and/or r were not lists, to avoid errors """
            """ after calculations, if there are cf and/or r lists, recalculate as series """
            self.cf = cf
            self.r = r
            self.fv_s = self.calc_series()[0]
            self.pv_s = self.calc_series()[1]

    def __repr__(self):
        return "cf=%s [cash flow], r=%s [rate], n=%s [years], m=%s[compounds], g=%s [growth] \n" \
               "m_precision=%s [decimal precision of values returned as money] \n" \
               "p_precision=%s [decimal precision of values returned as percentages] \n" \
               "series=%s [0 = no cf or r lists; 1 = cf list; 2 = cf and r lists] \n" \
               "----------------------------------------------------------------------------\n" % \
               (self.cf, self.r, self.n, self.m, self.g, self.m_precision, self.p_precision, self.series)

    def calc(self):
        return (1 + self.r_m) ** self.n_m

    def present_value(self):
        return round(self.cf * (self.calc() ** -1), self.m_precision)

    def future_value(self):
        return round(self.cf * self.calc(), self.m_precision)

    def annuity(self):
        return round(self.cf * (self.calc() - 1) * (self.r_m ** -1), self.m_precision)

    def find_pmt(self):
        return round(self.cf * ((self.calc() - 1) ** -1) * self.r_m, self.m_precision)

    def gradient(self):
        return round(self.cf * (self.calc() - (self.r_m * self.n_m) - 1) * (self.r_m ** -2), self.m_precision)

    def find_grad(self):
        return round(self.cf * ((self.r_m ** -1) - (self.n_m * ((self.calc() - 1) ** -1))), self.m_precision)

    def inc_dec(self):
        if self.r == self.g:
            factor = self.cf * self.n_m * ((1 + self.g_m) ** -1)
            return [factor, factor * self.calc()]
        else:
            factor = (self.g_m - self.r_m) ** -1
            fv_i_d = ((1 + self.g_m) ** self.n_m - self.calc()) * factor
            pv_i_d = ((((1 + self.g_m) / (1 + self.r_m)) ** self.n_m) - 1) * factor
            return [fv_i_d, pv_i_d]

    def calc_series(self):
        pv_value = 0
        fv_value = 0
        period = 1
        if type(self.r) == list:
            zipped = list(zip(self.cf, self.r))
            for pair in zipped:
                if period <= self.n:
                    pv_value += pair[0] * (((1 + (pair[1] / self.m)) ** (period * self.m)) ** -1)
                    fv_value += pair[0] * ((1 + (pair[1] / self.m)) ** (period * self.m))
                period += 1
        elif type(self.cf) == list:
            for cf_val in self.cf:
                if period <= self.n:
                    pv_value += cf_val * (((1 + self.r_m) ** (period * self.m)) ** -1)
                    fv_value += cf_val * ((1 + self.r_m) ** (period * self.m))
                period += 1
        else:
            pv_value += self.present_value()
            fv_value += self.future_value()
        return [round(fv_value, self.m_precision), round(pv_value, self.m_precision)]

    def yield_eff_annu(self):
        return round(((1 + self.r_m) ** self.m) - 1, self.p_precision)

    def yield_rate(self, inv_cf):
        return round(((inv_cf / self.cf) ** (1 / self.r_m)) - 1, self.p_precision)

    def periodic_rate(self, annual_yield):
        return round(((1 + annual_yield) ** (1 / self.m)) - 1, self.p_precision)


class Bond:
    def __init__(self, par, coup_rate, req_rate, n, m=2, m_precision=2, p_precision=4):
        self.par = par
        self.coup_rate = coup_rate
        self.req_rate = req_rate
        self.n = n
        self.m = m
        self.n_m = self.n * self.m
        self.c_m = self.coup_rate / self.m
        self.r_m = self.req_rate / self.m
        self.m_precision = m_precision
        self.p_precision = p_precision
        self.coupon = self.calc_coupon()
        self.price = self.calc_price()
        self.p_curve = self.calc_p_curve()
        self.data = self.calc_price_data()
        self.ci_plus_ioi = self.calc_ci_ioi()
        self.ioi = self.calc_ioi()
        self.pdr_ioi = self.calc_pdr_ioi()
        self.yield_current = round(self.calc_yield_current(), self.p_precision)
        self.total_return = self.calc_total_return()
        self.limited_return = self.calc_limited_return()
        self.duration_mac = self.calc_dur_mac()
        self.duration_mod = round((self.duration_mac / (1 + self.r_m)), 2)
        self.dollar_duration = round(self.calc_doll_dur(), self.m_precision)
        self.convexity = self.calc_convexity()
        self.p_chg_dur = round(self.calc_chg_p_dur(), self.p_precision)
        self.p_chg_cvx = round(self.calc_chg_p_cvx(), self.p_precision)
        self.p_chg_appx = self.p_chg_dur + self.p_chg_cvx
        self.ytm = self.calc_ytm()

    def __repr__(self):
        return "\n par=%s [par value], coup_rate=%s [coupon rate],\n " \
               "req_rate=%s [required return], n=%s [years], m=%s [compounds],\n " \
               "m_precision=%s [decimal precision of values returned as money],\n " \
               "p_precision=%s [decimal precision of values returned as percentages]\n" \
               "---------------------------------------------------------------------\n" % \
               (self.par, self.coup_rate, self.req_rate, self.n, self.m, self.m_precision, self.p_precision)

    def calc_coupon(self):
        """ coupon per period """
        return round(self.par * (self.coup_rate / self.m), self.m_precision)

    def calc_price(self):
        """ price of bond; assumes semi-annual payment -- per 'm' value in Bond class __init__ """
        temp_coup = TVM(self.coupon, self.req_rate, self.n, self.m)
        temp_par = TVM(self.par, self.req_rate, self.n, self.m)
        return round(temp_coup.pv_a + temp_par.pv, self.m_precision)

    def calc_price_modified(self, rate, year):
        """ price of a bond, given a required rate of return and remaining years to maturity """
        temp_coup = TVM(self.coupon, rate, year, self.m)
        temp_par = TVM(self.par, rate, year, self.m)
        return round(temp_coup.pv_a + temp_par.pv, self.m_precision)

    def calc_p_curve(self):
        """ price over life of bond """
        price_list = [self.par]
        for i in range(1, self.n + 1):
            price_list.append(self.calc_price_modified(self.req_rate, i))
        return price_list[::-1]

    def calc_price_data(self):
        """ all data related to bond price, over life of bond """
        price_list = [[0, 0, self.par, self.par]]
        for i in range(1, self.n + 1):
            temp_coup = TVM(self.coupon, self.req_rate, i, self.m)
            temp_par = TVM(self.par, self.req_rate, i, self.m)
            temp_bond = round(temp_coup.pv_a + temp_par.pv, self.m_precision)
            price_list.append([i, temp_coup.pv_a, temp_par.pv, temp_bond])
        return price_list[::-1]

    def calc_ci_ioi(self):
        """ coupon interest plus interest on interest """
        return self.coupon * ((((1 + self.r_m) ** self.n_m) - 1) / self.r_m)

    def calc_ioi(self):
        """ interest on interest """
        return self.ci_plus_ioi - (self.n_m * self.coupon)

    def calc_pdr_ioi(self):
        """ interest on interest as a percentage of total dollar return """
        return round(self.ioi / self.ci_plus_ioi, self.p_precision)

    def calc_yield_current(self):
        """ relates the annual coupon interest (ci = par * coup_rate) to the market price (p) """
        return (self.par * self.coup_rate) / self.price

    def calc_total_return(self, price=1000):
        """ total return on a bond held to maturity """
        """ [0] = dollar return; [1] = percentage return """
        future_amt = self.ci_plus_ioi + self.par
        return_pct = (((future_amt / price) ** (1 / self.n_m)) - 1) * self.m
        return future_amt, round(return_pct, 4)

    def calc_limited_return(self, price=1000, n_used=0):
        """ total return on a bond sold prior to maturity """
        """ [0] = dollar return; [1] = percentage return """
        pv_coup_int = TVM(self.coupon, self.req_rate, self.n - n_used, self.m).pv_a
        pv_maturity = TVM(self.par, self.req_rate, self.n - n_used, self.m).pv
        future_amt = self.ci_plus_ioi + pv_coup_int + pv_maturity
        return_pct = (((future_amt / price) ** (1 / (n_used * self.m))) - 1) * self.m if n_used > 0 else 0
        return future_amt, round(return_pct, self.p_precision)

    def calc_volatility(self, bps=1):
        """ [0] = volatility of bond price, given +/- bps change in required yield """
        """ [1] = price value of a basis point, per $100 par """
        """ [2] = percent change in the price value of a basis point, per $100 par """
        par_100 = self.par / 100
        new_price = self.calc_price_modified(self.req_rate + (bps / 10000), self.n)
        pct_chg = round((new_price - self.price) / self.price, self.p_precision)
        pvbp = (self.price / par_100) - (new_price / par_100)
        pvpc = round(round(pvbp, self.m_precision) / self.price, self.p_precision)
        return pct_chg, round(pvbp, 7), pvpc

    def calc_doll_dur(self):
        return self.duration_mod * (self.price / (self.par / 100))

    def calc_hedge_ratio(self, hedge_vehicle, yield_beta=1):
        """ hedge ratio in terms of price value of bps per $100 par value of a bond and a hedging vehicle """
        """ first two args should be price_val_bps functions """
        bond_to_hedge = self.calc_volatility()
        hedge_vehicle = hedge_vehicle.calc_volatility()
        return round((bond_to_hedge[1] / hedge_vehicle[1]) * yield_beta, self.p_precision)

    def calc_dur_mac(self):
        """ self.duration_mac = Macaulay Duration, expressed in years """
        """ self.duration_mod = Modified Duration, expressed in years """
        h = TVM(self.coupon, self.req_rate, self.n, self.m).pv_a / self.price
        mac = ((((1 + self.r_m) / self.r_m) * h) + (((self.r_m - self.c_m) / self.r_m) * self.n_m * (1 - h))) / self.m
        return round(mac, 2)

    def calc_convexity(self):
        """ Convexity, expressed in years """
        pv_par = TVM(self.par, self.req_rate, self.n, self.m, m_precision=5).pv / (self.par / 100)
        temp_pvcf, temp_t_t = 0, 0
        for i in range(1, self.n_m + 1):
            new_pvcf = (self.coupon / (self.par / 100)) * TVM(1, self.req_rate, i / self.m, self.m, m_precision=5).pv
            new_t_t = new_pvcf * (i * (i + 1))
            temp_pvcf += new_pvcf
            temp_t_t += new_t_t
        max_t = self.n_m * (self.n_m + 1)
        total_pvcf = round(temp_pvcf + pv_par, 5)
        total_t_t = round(temp_t_t + (pv_par * max_t), 5)
        cvx_years = (total_t_t / (((1 + self.r_m) ** self.m) * total_pvcf)) / (self.m ** 2)
        return round(cvx_years, 2)

    def calc_chg_p_dur(self, chg_bps=1):
        return -self.duration_mod * ((self.req_rate + (chg_bps / 10000)) - self.req_rate)

    def calc_chg_p_cvx(self, chg_bps=1):
        return self.convexity * (((self.req_rate + (chg_bps / 10000)) - self.req_rate) ** 2) / 2

    def calc_ytm(self, x=0.05):
        den = [(1 + i) / self.m for i in range(self.n_m)]
        value = lambda y: sum([self.coupon / (1 + y / self.m) ** (self.m * i) for i in den]) + \
                          self.par / ((1 + y / self.m) ** self.n_m) - self.price
        return round(opt.newton(value, x), self.p_precision)


class Portfolio:
    def __init__(self, bond_list, m_precision=2, p_precision=4):
        self.bond_list = bond_list
        self.m_precision = m_precision
        self.p_precision = p_precision
        self.market_value = self.calc_market_value()
        self.wt_avg_yield = self.calc_weighted_average()[0]
        self.wt_avg_duration = self.calc_weighted_average()[1]

    def calc_market_value(self):
        temp_mv = 0
        for bond in self.bond_list:
            temp_mv += bond.price
        return temp_mv

    def calc_weighted_average(self):
        """ portfolio yield & duration, weighted averages """
        temp_pdur = 0
        temp_pywa = 0
        for bond in self.bond_list:
            bond.portfolio_percentage = (bond.price / self.market_value)
            bond.portfolio_pct_yield = (bond.portfolio_percentage * bond.req_rate)
            bond.portfolio_dur_yield = (bond.portfolio_percentage * bond.duration_mod)
        for bond in self.bond_list:
            temp_pywa += bond.portfolio_pct_yield
            temp_pdur += bond.portfolio_dur_yield
        return round(temp_pywa, self.p_precision), round(temp_pdur, self.p_precision)


def generate_test_bonds():
    bond_a = Bond(1000, .09, .07, 5)
    bond_b = Bond(1000, .14, .1, 15)
    bond_c = Bond(1000, .1, .1, 30)
    return [bond_a, bond_b, bond_c]

test_port = Portfolio(generate_test_bonds())


class DayCount:
    def __init__(self, start_month, start_day, start_year, end_month, end_day, end_year, basis):
        self.start_month = start_month
        self.start_day = start_day
        self.start_year = start_year
        self.end_month = end_month
        self.end_day = end_day
        self.end_year = end_year
        self.basis = basis
        self.leap = [self.is_leap(self.start_year), self.is_leap(self.end_year)]
        self.actual_days = self.find_days()[2]
        self.actual_list = self.find_days()[3]
        self.days = self.chg_basis()
        self.list_years = [(self.start_year + i) for i in range(self.end_year - self.start_year + 1)]
        self.list_days = self.populate_day_list()

    @staticmethod
    def is_leap(year):
        leap = 0.
        if year % 4 == 0:
            if year % 100 == 0 & year % 400 != 0:
                leap = 0
            else:
                leap += 1
        return int(leap)

    def find_days(self):
        day_list = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.leap[0] == 1:
            if self.start_month <= 2:
                day_list[2] = 29
        if self.leap[1] == 1:
            if self.end_month >= 3:
                day_list[2] = 29
            elif self.end_month == 2 & self.end_day == 29:
                day_list[2] = 29
        partial_1 = (sum(day_list[self.start_month:]) - self.start_day + 1)
        partial_2 = (sum(day_list[:self.end_month]) + self.end_day)
        return partial_1, partial_2, partial_1 + partial_2, day_list

    def populate_day_list(self):
        d_list = [365 + self.is_leap(self.start_year + i) for i in range(self.end_year - self.start_year + 1)]
        d_list[0], d_list[-1] = self.find_days()[0], self.find_days()[1]
        return d_list

    def chg_basis(self):
        start = self.start_day
        end = self.end_day
        if self.basis == 1:
            return [self.actual_days, sum(self.actual_list)]
        if self.basis == 2:
            return [self.actual_days, 365]
        if self.basis == 3:
            return [self.actual_days, sum(self.actual_list)]
        if self.basis == 4:
            return [self.actual_days, 360]
        if self.basis == 5:
            if self.start_day == 31:
                start = 30
                if self.end_day == 31:
                    end = 30
            if self.end_day == 31 & self.start_day == 30:
                    end = 30
            chg_year = (self.end_year - self.start_year)
            chg_month = (self.end_month - self.start_month)
            return [(chg_year * 360) + (chg_month * 30) + (end - start), 360]
        if self.basis == 6:
            if self.start_day == 31:
                start = 30
            if self.end_day == 31:
                end = 30
            chg_year = (self.end_year - self.start_year)
            chg_month = (self.end_month - self.start_month)
            return [(chg_year * 360) + (chg_month * 30) + (end - start), 360]


class Mortgage:
    def __init__(self, amount, rate, term, amort, d_year, d_month, d_day, x_pmt=0, freq=12, io_pds=0, m_p=2, p_p=4):
        self.l_amt = amount
        self.l_rate = rate
        self.l_term = term
        self.l_amort = amort
        self.d_year = d_year
        self.d_month = d_month
        self.d_day = d_day
        self.l_x_pmt = x_pmt
        self.l_freq = freq
        self.l_io_pds = io_pds
        self.m_prec = m_p
        self.p_prec = p_p
        self.f_rate = (1 + (self.l_rate / self.l_freq)) ** self.l_amort
        self.r = self.l_rate / self.l_freq
        self.p_and_i = round(self.calc_pmt(), self.m_prec)
        self._y_list = [(int(self.d_year) + i) for i in range(int(self.l_term / self.l_freq))]
        self._table = self.make_table()

    def month_list(self):
        _m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        skip_dict = {1: 12, 2: 6, 4: 3, 6: 2, 12: 1}

        def generate_list(base_list, skip):
            return base_list[::skip]

        _m_stub_1 = generate_list(_m[self.d_month - 1:], skip_dict[self.l_freq])
        _m_stub_2 = generate_list(_m[:self.d_month - 1], skip_dict[self.l_freq])
        print(_m_stub_1, _m_stub_2)
        _m_middle = generate_list(_m[:self.d_month - 1] + _m[self.d_month - 1:], skip_dict[self.l_freq])
        return _m_stub_1, _m_middle, _m_stub_2

    def make_table(self):
        """ generates amortization table """
        paid = 0
        am_table = [['DATE', 'BEG BALANCE', 'PAYMENT', 'INTEREST ', 'PRINCIPAL', 'END BALANCE']]

        def am(tot_paid, prin, pmt, rate_freq, m_var, d_var, y_var, m_prec):
            """ calculates all values and appends them to the amortization table """
            bal_end = round(prin - tot_paid, m_prec)
            bal_beg = round(bal_end, m_prec)
            col_1 = m_var + ' ' + str(d_var) + ' ' + str(y_var)                         # Date of payment
            # col_2 is not used -- bal_beg used instead                                 # Beginning principal balance
            col_3 = round(pmt, m_prec) if bal_end >= pmt else round(bal_end, m_prec)    # Total payment due
            col_4 = round(bal_end * rate_freq, m_prec)                                  # Interest due
            col_5 = round(col_3 - col_4, m_prec)                                        # Principal due
            col_6 = round(bal_beg - col_5, m_prec) if bal_beg > col_3 else 0            # Ending principal balance
            am_table.append([col_1, bal_beg, col_3, col_4, col_5, col_6])
            tot_paid += col_5
            return tot_paid

        for m1 in self.month_list()[0]:
            paid = am(paid, self.l_amt, self.p_and_i, self.r, m1, self.d_day, self.d_year, self.m_prec)
        for year in self._y_list[1:]:
            for m2 in self.month_list()[1]:
                paid = am(paid, self.l_amt, self.p_and_i, self.r, m2, self.d_day, year, self.m_prec)
        for m3 in self.month_list()[2]:
            paid = am(paid, self.l_amt, self.p_and_i, self.r, m3, self.d_day, self._y_list[-1] + 1, self.m_prec)
        return am_table

    def calc_pmt(self):
        return ((((self.l_rate * self.l_amt) * self.f_rate) / (self.f_rate - 1)) / self.l_freq) + self.l_x_pmt


def loan():
    """ creates a new loan -- asks for user input to fill the args in the Mortgage class """
    freq_dict = {'annually': 1,
                 'annual': 1,
                 'years': 1,
                 'year': 1,
                 'semi-annually': 2,
                 'semi-annual': 2,
                 'semiannually': 2,
                 'semiannual': 2,
                 'quarterly': 4,
                 'quarters': 4,
                 'quarter': 4,
                 'monthly': 12,
                 'months': 12,
                 'month': 12}

    translate = {'annually': 'years',
                 'annual': 'years',
                 'years': 'years',
                 'year': 'years',
                 'semi-annually': 'half-years',
                 'semi-annual': 'half-years',
                 'semiannually': 'half-years',
                 'semiannual': 'half-years',
                 'quarterly': 'quarters',
                 'quarters': 'quarters',
                 'quarter': 'quarters',
                 'monthly': 'months',
                 'months': 'months',
                 'month': 'months'}

    _p = float(str(input('Loan Amount: ')).strip('$').replace(',', ''))
    _r = float(str(input('Interest Rate: ')).strip('%')) / 100
    _f = str(input('Payment Frequency [annual/semi-annual/quarterly/monthly]: ')).lower()
    _t = str(input('Loan Maturity [### years or ### months]: ')).lower().split()
    _t[0], _t[1] = float(_t[0]), freq_dict[_t[1]]
    _a_f = str(input('Fully Amortizing [y/n]: ')).lower()
    _a_f = 'y' if _a_f == 'yes' else 'n' if _a_f == 'no' else _a_f
    _n = _t[0] / _t[1] * freq_dict[_f]
    _a = float(input('Amortization [### ' + translate[_f] + ']: ')) if _a_f == 'n' else _n
    _d = str(input('Date of First Payment [mm/dd/yyyy]: ')).split('/')

    return Mortgage(_p, _r, _n, _a, int(_d[2]), int(_d[0]), int(_d[1]), freq=freq_dict[_f])

testloan = loan()

# make test mortgage
mtest1 = Mortgage(200000, .065, 360, 360, 2015, 1, 15)
mtest2 = Mortgage(200000, .065, 360, 360, 2015, 12, 15)
mtest3 = Mortgage(200000, .065, 360, 360, 2015, 7, 15)

