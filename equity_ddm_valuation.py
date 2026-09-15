"""Two-stage dividend discount model.

Values a stock from an explicit dividend forecast plus a Gordon growth terminal
value, then compares intrinsic value to market price for a BUY/HOLD/SELL call.

Run with:

    streamlit run equity_ddm_valuation.py

then open the local URL it prints.
"""

import streamlit as st

st.title("Stock Valuation Calculator")
st.divider()

ticker = st.text_input("Stock Ticker")
forecast_periods = st.number_input("Number of Forecasted Annual Dividends", min_value = 0, step = 1)

annual_dividends = []
for period in range(forecast_periods):
    annual_dividends.append(st.number_input(f"Forecasted Annual Dividend for Period {period + 1} ($)", min_value = 0.00, step = 0.01))
                            
terminal_growth_rate = st.number_input("Terminal Growth Rate (%)", min_value = 0.00, max_value = 4.00, step = 0.25) / 100
discount_rate = st.number_input("Discount Rate (%)", min_value = 0.00, max_value = 100.00, step = 0.25) / 100
current_market_price = st.number_input("Current Market Price ($)", min_value = 0.00, step = 10.00)
time_to_first_payment = st.number_input("Number of Months from Valuation Date to First Forecasted Dividend Payment", min_value = 0, max_value = 12, step = 1)

periods = []
for period in range(forecast_periods):
    periods.append(period + (time_to_first_payment / 12))

forecast_horizon_dividends = []
for period in range(forecast_periods):
    if periods[period] < 1:
        forecast_horizon_dividends.append(annual_dividends[period] * periods[period])
    else:
        forecast_horizon_dividends.append(annual_dividends[period])

if forecast_periods == 0:
    st.divider()
    st.warning("Enter at least one forecasted annual dividend to calculate a valuation.")

elif discount_rate <= terminal_growth_rate:
    st.divider()
    st.warning("The discount rate must be greater than the terminal growth rate.")

else:
    terminal_value = (forecast_horizon_dividends[-1] * (1 + terminal_growth_rate)) / (discount_rate - terminal_growth_rate)

    forecast_horizon_DCFs = []
    forecast_horizon = 0
    for period in range(forecast_periods):
        forecast_horizon_DCFs.append(forecast_horizon_dividends[period] / ((1 + discount_rate) ** (periods[period])))
        forecast_horizon += forecast_horizon_DCFs[period]

    terminal_value_DCF = terminal_value / ((1 + discount_rate) ** periods[-1])

    total_value = forecast_horizon + terminal_value_DCF

    st.divider()
    st.subheader("Results:")

    st.write(f"Estimated Intrinsic Value of {ticker} Stock:  ${total_value: .2f}")

    if total_value > current_market_price:
        st.write("Recommendation:  BUY")
    elif total_value == current_market_price:
        st.write("Recommendation:  HOLD")
    else:
        st.write("Recommendation:  SELL")




