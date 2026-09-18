"""Present value / future value calculator.

Discounts or compounds a discrete cash-flow forecast across any number of
growth phases, closing with either an annuity or a growing perpetuity.

Run standalone with:

    streamlit run time_value_of_money.py

or reach it from the combined app:

    streamlit run streamlit_app.py
"""

import streamlit as st


def render():
    st.title("Present Value / Future Value Calculator")

    # get inputs
    calculation_type = st.selectbox("Calculation Type", ["PV", "FV"])

    discrete_cash_flows = []
    number_of_periods = st.number_input("Number of Discrete Forecast Periods", min_value = 0, step = 1)
    if number_of_periods != 0:
        for period in range(number_of_periods):
            cf = st.number_input(f"Cash Flow for Period {period+1}", value = 1000.0, step = 100.00)
            discrete_cash_flows.append(cf)
        cash_flow = discrete_cash_flows[-1]
    else:
        cash_flow = st.number_input("Starting Cash Flow", value = 1000.0, step = 100.00)

    number_of_phases = st.number_input("Number of Growth Phases", min_value = 0, step = 1)

    discount_rate = st.number_input("Discount Rate (%)", value = 12.0, step = 1.00) / 100

    growth_rate = []
    length_of_phase = []

    for phase in range(number_of_phases):
        st.subheader(f"Phase {phase+1}")
        if phase == (number_of_phases - 1):
            if calculation_type == 'PV':
                last_phase = st.selectbox("Last Phase Type", ["Annuity", "Perpetuity"])
            else:
                last_phase = "Annuity"

        if (phase != (number_of_phases - 1)) or ((phase == (number_of_phases - 1)) and (last_phase == 'Annuity')):
            growth = st.number_input(f"Growth Rate Phase {phase+1} (%)", key = f"growth{phase}", step = 1.00) / 100
            length = st.number_input(f"Length of Phase {phase+1} (Years)", min_value = 1, key = f"length{phase}")

            growth_rate.append(growth)
            length_of_phase.append(length)

        elif ((phase == (number_of_phases - 1)) and (last_phase == 'Perpetuity')):
            growth = st.number_input(f"Perpetuity Growth Rate (%)", value = 10.0, step = 1.00) / 100
            growth_rate.append(growth)

    # define functions
    def update_cf(cf, g, t):
        return cf * ((1+g) ** t)

    def pv_from_fv(fv, r, t):
        return fv / ((1+r) ** t)

    def fv_from_pv(pv, r, t):
        return pv * ((1+r) ** t)

    def pv_annuity(cf, g, r, t):
        if abs(r - g) < 1e-12:
            return cf * t / (1 + r)
        return (cf / (r-g)) * (1 - ((1+g)/(1+r)) ** t)

    def pv_perpetuity(cf, g, r):
        if g >= r:
            st.error("Perpetuity growth rate must be less than the discount rate.")
            st.stop()
        return cf / (r-g)

    # create logic
    if st.button("Calculate"):
        st.subheader("Results")
        if calculation_type == 'PV':
            present_value = 0
            total_present_value = 0
            total_time = number_of_periods

            if number_of_periods != 0:
                for period in range(number_of_periods):
                    cash_flow = discrete_cash_flows[period]
                    present_value = pv_from_fv(cash_flow, discount_rate, period+1)
                    total_present_value += present_value
                st.write(f"PV Discrete Forecast: ${total_present_value:.2f}")

            for phase in range(number_of_phases):
                if phase == 0:
                    cash_flow = update_cf(cash_flow, growth_rate[phase], 1)
                else:
                    cash_flow = update_cf(update_cf(cash_flow, growth_rate[phase - 1], length_of_phase[phase - 1] - 1), growth_rate[phase], 1)

                if (phase != (number_of_phases - 1)) or ((phase == (number_of_phases - 1)) and (last_phase == 'Annuity')):
                    present_value = pv_annuity(cash_flow, growth_rate[phase], discount_rate, length_of_phase[phase])
                    present_value = pv_from_fv(present_value, discount_rate, total_time)
                    total_present_value += present_value
                    total_time += length_of_phase[phase]
                    st.write(f"PV Annuity Phase {phase+1}: ${present_value:.2f}")

                elif ((phase == (number_of_phases - 1)) and (last_phase == 'Perpetuity')):
                    present_value = pv_perpetuity(cash_flow, growth_rate[phase], discount_rate)
                    present_value = pv_from_fv(present_value, discount_rate, total_time)
                    total_present_value += present_value
                    st.write(f"PV Perpetuity: ${present_value:.2f}")

            st.divider()
            st.write(f"TOTAL PV = ${total_present_value:.2f}")

        elif calculation_type == 'FV':
            future_value = 0
            total_future_value = 0
            total_time = number_of_periods

            for phase in range(number_of_phases):
                total_time += length_of_phase[phase]

            if number_of_periods != 0:
                for period in range(number_of_periods):
                    cash_flow = discrete_cash_flows[period]
                    future_value = fv_from_pv(cash_flow, discount_rate, total_time)
                    total_future_value += future_value
                st.write(f"FV Discrete Forecast: ${total_future_value:.2f}")

            for phase in range(number_of_phases):
                if phase == 0:
                    cash_flow = update_cf(cash_flow, growth_rate[phase], 1)
                else:
                    cash_flow = update_cf(update_cf(cash_flow, growth_rate[phase - 1], length_of_phase[phase - 1] - 1), growth_rate[phase], 1)

                future_value = fv_from_pv(pv_annuity(cash_flow, growth_rate[phase], discount_rate, length_of_phase[phase]), discount_rate, length_of_phase[phase])
                future_value = fv_from_pv(future_value, discount_rate, total_time - length_of_phase[phase])
                total_future_value += future_value
                total_time -= length_of_phase[phase]

                st.write(f"FV Annuity Phase {phase+1}: ${future_value:.2f}")

            st.divider()
            st.write(f"FV TOTAL = ${total_future_value:.2f}")


if __name__ == "__main__":
    render()
