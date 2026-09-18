"""Combined entry point for the four valuation dashboards.

Single app for Streamlit Community Cloud deployment. Each model still runs on
its own, for example `streamlit run bond_valuation.py`.

Run with:

    streamlit run streamlit_app.py
"""

import streamlit as st

import bond_valuation
import capital_budgeting
import equity_ddm_valuation
import time_value_of_money

st.set_page_config(page_title="Finance Valuation Dashboards", page_icon="📈", layout="centered")


def home():
    st.title("Finance Valuation Dashboards")
    st.write(
        "Four interactive discounted cash flow models covering time value of "
        "money, bond pricing, equity valuation, and capital budgeting. Pick a "
        "model from the sidebar to get started."
    )

    st.divider()

    st.subheader("Time Value of Money")
    st.write("PV or FV across any number of growth phases, ending in an annuity or a growing perpetuity.")

    st.subheader("Bond Valuation")
    st.write("Prices a coupon bond at any compounding frequency, reports Macaulay and modified duration, and plots the price yield curve.")

    st.subheader("Equity DDM Valuation")
    st.write("Two stage dividend discount model returning a BUY, HOLD, or SELL call against market price.")

    st.subheader("Capital Budgeting")
    st.write("Builds a full FCFF pro forma, then scores the project on NPV, IRR, and payback.")

    st.divider()

    st.caption("Every formula is written from scratch in plain Python, so the math stays visible and auditable.")
    st.caption("Source: [github.com/sherif-fahmy-git/finance-valuation-dashboards](https://github.com/sherif-fahmy-git/finance-valuation-dashboards)")


pages = [
    st.Page(home, title="Home", icon="🏠", default=True),
    st.Page(time_value_of_money.render, title="Time Value of Money", icon="🕒", url_path="time-value-of-money"),
    st.Page(bond_valuation.render, title="Bond Valuation", icon="📊", url_path="bond-valuation"),
    st.Page(equity_ddm_valuation.render, title="Equity DDM Valuation", icon="💵", url_path="equity-ddm-valuation"),
    st.Page(capital_budgeting.render, title="Capital Budgeting", icon="🏗️", url_path="capital-budgeting"),
]

st.navigation(pages).run()
