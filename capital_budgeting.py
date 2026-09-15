#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import streamlit as st
import numpy_financial as npf

st.title("Project Evaluation and Capital Budgeting")
st.divider()

term = st.number_input("Project Term (years)", min_value = 0, value = 6, step = 1)
initial_revenue = st.number_input("Initial Revenues", min_value = 0.00, value = 1000000000.00, step = 10000000.00)
growth_rate = st.number_input("Sales Growth Rate (%)", min_value = 0.00, value = 7.50, step = 0.50) / 100
capex = st.number_input("Initial Capital Expenditure", min_value = 0.00, value = 750000000.00, step = 10000000.00)
residual = st.number_input("Residual Value of Capex (assuming Straight-Line Depreciation)", min_value = 0.00, step = 1000000.00)
gross_margin = st.number_input("Gross Margin (excluding Depreciation)", min_value = 0.00, value = 40.00, step = 1.00) / 100
opex = st.number_input("Operating Expenses", min_value = 0.00, value = 200000000.00, step = 10000000.00)
change_opex = st.selectbox("Will Opex increase?", ['Yes', 'No'], index = 0)
if change_opex == 'Yes':
    threshold = st.number_input("Opex increases if revenues exceed...", min_value = 0.00, value = 1250000000.00, step = 10000000.00)
    opex_rate = st.number_input("Opex will increase by... (%)", min_value = 0.00, value = 10.00, step = 1.00) / 100
nwc = st.number_input("Net Working Capital Requirement (% of Sales)", min_value = 0.00, value = 10.00, step = 1.00) / 100
tax = st.number_input("Corporate Tax Rate (%)", min_value = 0.00, value = 21.00, step = 1.00) / 100
discount = st.number_input("WACC (Discount Rate) (%)", min_value = 0.00, value = 15.50, step = 0.50) / 100
payback = st.number_input("Preferred Payback Period (years)", min_value = 0, value = 3, step = 1)

periods = []
for period in range(term + 1):
    periods.append(period)

revenues = []
for period in periods:
    if period == 0:
        revenues.append(0)
    else:
        revenues.append(initial_revenue * ((1 + growth_rate) ** (period - 1)))

cogs = []
for period in periods:
    cogs.append(-((1 - gross_margin) * revenues[period]))

gross_profits = []
for period in periods:
    gross_profits.append(revenues[period] + cogs[period])

opex_list = []
for period in periods:
    if period == 0:
        opex_list.append(-0)
    elif change_opex != 'Yes':
        opex_list.append(-opex)
    else:
        if revenues[period] <= threshold:
            opex_list.append(-opex)
        else:
            opex_list.append(-opex * (1 + opex_rate))

depex_list = []
for period in periods:
    if period == 0:
        depex_list.append(-0)
    else:
        depex_list.append(-(capex / term))

operating_profits = []
for period in periods:
    operating_profits.append(gross_profits[period] + opex_list[period] + depex_list[period])

taxes = []
for period in periods:
    taxes.append(-(operating_profits[period] * tax))

nopat = []
for period in periods:
    nopat.append(operating_profits[period] + taxes[period])

capex_list = []
for period in periods:
    if period == 0:
        capex_list.append(-capex)
    else:
        capex_list.append(-0)

addback_depex = []
for period in periods:
    addback_depex.append(-depex_list[period])

change_in_onwc = []
for period in periods:
    if period != term:
        change_in_onwc.append(-(nwc * (revenues[period + 1] - revenues[period])))
    else:
        change_in_onwc.append(-(nwc * (0 - revenues[period])))

fcff = []
for period in periods:
    fcff.append(nopat[period] + capex_list[period] - depex_list[period] + change_in_onwc[period])

pv = []
npv = 0
for period in periods:
    pv.append(fcff[period] / ((1 + discount) ** period))
    npv += pv[period]

irr = npf.irr(fcff)

cumulative_cf = []
for period in periods:
    if period == 0:
        cumulative_cf.append(fcff[period])
    else:
        cumulative_cf.append(cumulative_cf[period - 1] + fcff[period])
relevant_period = 0
for period in periods:
    if cumulative_cf[period] >= 0:
        relevant_period = period
        break
pbb = (relevant_period - 1) + (abs(cumulative_cf[relevant_period - 1]) / fcff[period])

st.subheader("RESULTS")
st.divider()

data = pd.DataFrame({
    "Periods": periods,
    "Revenues": revenues,
    "Less COGS": cogs,
    "Gross Profit": gross_profits,
    "Less Opex": opex_list,
    "Less Depex": depex_list,
    "Operating Profit": operating_profits,
    "Less Taxes": taxes,
    "NOPAT": nopat,
    "Less Capex": capex_list,
    "Addback Depex": addback_depex,
    "Less Change in ONWC": change_in_onwc,
    "FCFF": fcff
})

st.table(data.T)
st.divider()

st.write(f"Net Present Value: ${npv:,.2f}")
if npv > 0:
    st.write("Recommendation based on NPV: GO")
else:
    st.write("Recommendation based on NPV: NO-GO")

st.write(f"Internal Rate of Return: {(irr * 100):.4f}%")
if irr > discount:
    st.write("Recommendation based on IRR: GO")
else:
    st.write("Recommendation based on IRR: NO-GO")

st.write(f"Payback Period: {pbb:.4f} years")
if pbb <= payback:
    st.write("Recommendation based on PBB: GO")
else:
    st.write("Recommendation based on PBB: NO-GO")






# In[ ]:




