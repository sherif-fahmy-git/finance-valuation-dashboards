# Finance Valuation Dashboards

Four interactive Streamlit apps covering the core discounted cash flow methods
used in investment research: time value of money, bond pricing, equity
valuation, and capital budgeting.

Every formula is written from scratch in plain Python, so the math stays
visible and auditable.

## Live demo

**[Open the live app](LIVE_DEMO_URL)**

All four models in one place, no install needed. Pick a model from the sidebar.

## Run locally

Requires Python 3.13.

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Each model also runs on its own. Those commands are listed below.

## Time Value of Money

PV or FV across any number of growth phases, ending in an annuity or a growing
perpetuity.

```bash
streamlit run time_value_of_money.py
```

![Time Value of Money](screenshots/time_value_of_money.png)

*$1,000 growing 5% for 5 years, then a 3% perpetuity, discounted at 12%.*

## Bond Valuation

Prices a coupon bond at any compounding frequency, reports Macaulay and
modified duration, and plots the price yield curve.

```bash
streamlit run bond_valuation.py
```

![Bond Valuation](screenshots/bond_valuation.png)

*6% semiannual coupon, 10 years, 8% yield. Prices at $864.10 with 7.17 modified duration.*

## Equity DDM Valuation

Two stage dividend discount model: explicit dividend forecast plus a Gordon
growth terminal value, with support for a partial first period. Returns a
BUY, HOLD, or SELL call against market price.

```bash
streamlit run equity_ddm_valuation.py
```

![Equity DDM Valuation](screenshots/equity_ddm_valuation.png)

*KO with a 3 year dividend forecast, 3% terminal growth, 9% discount rate. Intrinsic value $33.46 against a $62 price, so SELL.*

## Capital Budgeting

Builds a full FCFF pro forma from revenue growth, margins, capex, working
capital, and tax, then scores it on NPV, IRR, and payback.

```bash
streamlit run capital_budgeting.py
```

![Capital Budgeting inputs](screenshots/capital_budgeting_inputs.png)

![Capital Budgeting results](screenshots/capital_budgeting_results.png)

*$750M capex project at 15.5% WACC. NPV $58.1M and IRR 17.7% both say GO, payback of 4.0 years says NO-GO against a 3 year target.*

## Modelling notes

- **Compounding is explicit.** Annual coupon and yield inputs are converted to
  per period figures, so semiannual and monthly bonds price correctly.
- **Dividends can arrive mid year.** The first forecast period may be
  fractional and is discounted accordingly.
- **Working capital is a cash flow, not an expense.** The change in net
  working capital is modelled each period and released in the final year.
- **Terminal assumptions are guarded.** Perpetuity and Gordon growth formulas
  diverge when growth meets the discount rate, so those cases report the
  problem instead of returning a meaningless number.

## Built with

Python, Streamlit, pandas, matplotlib, NumPy Financial.
