"""Bond value and duration calculator.

Prices a coupon bond at annual, semiannual, quarterly or monthly compounding,
reports Macaulay and modified duration, and plots the price-yield curve.

Run with:

    streamlit run bond_valuation.py

then open the local URL it prints.
"""

import matplotlib.pyplot as plt
import streamlit as st

st.title("Bond Value and Duration Calculator")

anncprate = st.number_input("Coupon Rate (% in APR)", min_value = 0.0, step = 1.0) / 100
annttm = st.number_input("Term to Maturity (in years)", min_value = 0.0, step = 1.0)
annytm = st.number_input("Yield to Maturity (% in APR)", min_value = 0.0, step = 1.0) / 100
parval = st.number_input("Par Value ($)", min_value = 0.0, value = 1000.0, step = 100.0)
freq = st.selectbox("Compounding Frequency", ["Annual", "Semiannual", "Quarterly", "Monthly"], index = 1)

if freq == "Annual":
    freq = 1
elif freq == "Semiannual":
    freq = 2
elif freq == "Quarterly":
    freq = 4
elif freq == "Monthly":
    freq = 12

def calculate_CFs(ttm, cprate, par):
    CFs = []
    for period in range(int(ttm) + 1):
        if period == 0:
            CFs.append(0)
        elif period < ttm:
            CFs.append(cprate * par)
        else:
            CFs.append((cprate * par) + par)
    return CFs

def calculate_PVCFs(cfs, ytm, frequency):
    PVCFs = []
    for period in range(len(cfs)):
        PVCFs.append(cfs[period] / (1 + (ytm / frequency)) ** period)
    return PVCFs
    
def calculate_bondprice(pvcfs):
    price = 0
    for pvcf in pvcfs:
        price += pvcf
    return price


if st.button("Calculate Bond Value and Duration"):
    CF = calculate_CFs(annttm * freq, anncprate / freq, parval)
    PVCF = calculate_PVCFs(CF, annytm, freq)
    bondprice = calculate_bondprice(PVCF)
    
    permacaulay = 0
    for period in range(int(annttm * freq) + 1):
        permacaulay += (period * PVCF[period]) / bondprice
    macaulay = permacaulay / freq
    modified = macaulay / (1 + (annytm / freq))

    st.write(f"Bond Value = ${bondprice:.2f}")
    st.write(f"Macaulay Duration = {macaulay:.4f} years")
    st.write(f"Modified Duration = {modified:.4f} years")
    

YTMs = []
for i in range(100):
    YTMs.append(i)
    YTMs.append(i+0.5)

values = []
for ytm in YTMs:
    values.append(calculate_bondprice(calculate_PVCFs(calculate_CFs(annttm*freq, anncprate/freq, parval), ytm/100, freq)))

fig, ax = plt.subplots()
ax.plot(YTMs, values)
ax.set_title("Bond Value vs. YTM")
ax.set_xlabel("Yield to Maturity (%)")
ax.set_ylabel("Bond Value ($)")

st.pyplot(fig)




