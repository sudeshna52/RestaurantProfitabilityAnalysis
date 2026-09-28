import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Restaurant Profitability Analysis",
    page_icon="🍽️",
    layout="wide"
)
# ---------------------------------------------------------
# CUSTOM DASHBOARD STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.75;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .insight-box {
        padding: 18px;
        border-radius: 10px;
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.20);
        margin-bottom: 12px;
    }

    .insight-title {
        font-size: 17px;
        font-weight: 650;
        margin-bottom: 6px;
    }

    .insight-text {
        font-size: 14px;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():

    file_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "SkyCity Auckland Restaurants & Bars.csv"
    )

    df = pd.read_csv(file_path)

    return df


df = load_data()


# ---------------------------------------------------------
# CREATE ANALYTICAL METRICS
# ---------------------------------------------------------

df["TotalRevenue"] = (
    df["InStoreRevenue"]
    + df["UberEatsRevenue"]
    + df["DoorDashRevenue"]
    + df["SelfDeliveryRevenue"]
)

df["TotalNetProfit"] = (
    df["InStoreNetProfit"]
    + df["UberEatsNetProfit"]
    + df["DoorDashNetProfit"]
    + df["SelfDeliveryNetProfit"]
)

df["OverallProfitMargin"] = (
    df["TotalNetProfit"] /
    df["TotalRevenue"]
)

df["NetProfitPerOrder"] = (
    df["TotalNetProfit"] /
    df["MonthlyOrders"]
)

df["UberEatsCommissionCost"] = (
    df["UberEatsRevenue"] *
    df["CommissionRate"]
)

df["DoorDashCommissionCost"] = (
    df["DoorDashRevenue"] *
    df["CommissionRate"]
)

df["TotalCommissionCost"] = (
    df["UberEatsCommissionCost"]
    + df["DoorDashCommissionCost"]
)

df["CommissionDragIndex"] = (
    df["TotalCommissionCost"] /
    df["TotalRevenue"]
)

df["SelfDeliveryCostRatio"] = (
    df["SD_DeliveryTotalCost"] /
    df["SelfDeliveryRevenue"]
)

df["SelfDeliveryROI"] = (
    df["SelfDeliveryNetProfit"] /
    df["SD_DeliveryTotalCost"]
)

# ---------------------------------------------------------
# DASHBOARD HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">'
    '🍽️ Multi-Channel Restaurant Profitability Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Cost Structure and Channel-Wise Profitability Analysis | '
    'SkyCity Auckland Restaurants & Bars'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Interactive profitability analysis across In-Store, Uber Eats, "
    "DoorDash, and Self-Delivery channels."
)


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.title("Dashboard Filters")

st.sidebar.info(
    "Tip: Remove individual selections using the × button "
    "inside each filter."
)
st.sidebar.caption(
    "Use the filters below to explore profitability by "
    "cuisine and business segment."
)

cuisine_options = sorted(df["CuisineType"].dropna().unique())

segment_options = sorted(df["Segment"].dropna().unique())

selected_cuisines = st.sidebar.multiselect(
    "Cuisine Type",
    cuisine_options,
    default=cuisine_options
)

selected_segments = st.sidebar.multiselect(
    "Business Segment",
    segment_options,
    default=segment_options
)

# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_df = df.copy()

if selected_cuisines:
    filtered_df = filtered_df[
        filtered_df["CuisineType"].isin(selected_cuisines)
    ]

if selected_segments:
    filtered_df = filtered_df[
        filtered_df["Segment"].isin(selected_segments)
    ]
st.sidebar.divider()

st.sidebar.subheader("Current Selection")

st.sidebar.metric(
    "Restaurants",
    f"{len(filtered_df):,}"
)

st.sidebar.metric(
    "Orders",
    f"{filtered_df['MonthlyOrders'].sum():,.0f}"
)

# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

total_revenue = filtered_df["TotalRevenue"].sum()

total_profit = filtered_df["TotalNetProfit"].sum()

total_orders = filtered_df["MonthlyOrders"].sum()

net_profit_per_order = (
    total_profit / total_orders
    if total_orders != 0
    else 0
)

overall_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0
    else 0
)

total_commission = filtered_df["TotalCommissionCost"].sum()

commission_drag = (
    total_commission / total_revenue * 100
    if total_revenue != 0
    else 0
)

self_delivery_profit = (
    filtered_df["SelfDeliveryNetProfit"].sum()
)

self_delivery_cost = (
    filtered_df["SD_DeliveryTotalCost"].sum()
)

self_delivery_roi = (
    self_delivery_profit /
    self_delivery_cost * 100
    if self_delivery_cost != 0
    else 0
)

# ---------------------------------------------------------
# BREAK-EVEN METRICS
# ---------------------------------------------------------

# Weighted break-even commission rate for Uber Eats
uber_break_even_commission = (
    (
        filtered_df["UberEatsRevenue"]
        * (1 - filtered_df["COGSRate"] - filtered_df["OPEXRate"])
    ).sum()
    / filtered_df["UberEatsRevenue"].sum()
    * 100
    if filtered_df["UberEatsRevenue"].sum() != 0
    else 0
)

# Weighted break-even commission rate for DoorDash
doordash_break_even_commission = (
    (
        filtered_df["DoorDashRevenue"]
        * (1 - filtered_df["COGSRate"] - filtered_df["OPEXRate"])
    ).sum()
    / filtered_df["DoorDashRevenue"].sum()
    * 100
    if filtered_df["DoorDashRevenue"].sum() != 0
    else 0
)

# Current average delivery cost per order
current_delivery_cost = (
    filtered_df["SD_DeliveryTotalCost"].sum()
    / filtered_df["SelfDeliveryOrders"].sum()
    if filtered_df["SelfDeliveryOrders"].sum() != 0
    else 0
)

# Break-even delivery cost per order
break_even_delivery_cost = (
    (
        filtered_df["SelfDeliveryRevenue"]
        * (1 - filtered_df["COGSRate"] - filtered_df["OPEXRate"])
    ).sum()
    / filtered_df["SelfDeliveryOrders"].sum()
    if filtered_df["SelfDeliveryOrders"].sum() != 0
    else 0
)

# ---------------------------------------------------------
# KPI SUMMARY
# ---------------------------------------------------------

st.markdown("### Portfolio KPIs")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric(
    "Total Revenue",
    f"${total_revenue:,.0f}"
)

kpi2.metric(
    "Net Profit",
    f"${total_profit:,.0f}"
)

kpi3.metric(
    "Overall Margin",
    f"{overall_margin:.2f}%"
)

kpi4.metric(
    "Net Profit / Order",
    f"${net_profit_per_order:.2f}"
)

kpi5.metric(
    "Commission Drag",
    f"{commission_drag:.2f}%"
)



st.divider()

# ---------------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Executive Summary</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="insight-box">
        <div class="insight-title">Portfolio Profitability</div>
        <div class="insight-text">
            The selected restaurant portfolio generates
            <b>${total_revenue:,.0f}</b> in revenue and
            <b>${total_profit:,.0f}</b> in net profit,
            resulting in an overall margin of
            <b>{overall_margin:.2f}%</b>.
        </div>
    </div>

    <div class="insight-box">
        <div class="insight-title">Channel Economics</div>
        <div class="insight-text">
            In-Store and Self-Delivery maintain substantially higher
            profit margins than the two aggregator channels.
            Aggregator profitability is strongly affected by platform
            commission costs.
        </div>
    </div>

    <div class="insight-box">
        <div class="insight-title">Commission Impact</div>
        <div class="insight-text">
            The current portfolio-level commission drag is
            <b>{commission_drag:.2f}%</b> of total revenue.
            The sensitivity analysis below allows commission assumptions
            to be changed interactively.
        </div>
    </div>

    <div class="insight-box">
        <div class="insight-title">Self-Delivery Economics</div>
        <div class="insight-text">
            Self-Delivery currently generates
            <b>{self_delivery_roi:.2f}%</b> ROI based on net profit
            relative to delivery cost. Delivery-cost sensitivity can be
            tested using the interactive scenario control below.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# BREAK-EVEN ANALYSIS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Break-Even Analysis</div>',
    unsafe_allow_html=True
)

be1, be2, be3, be4 = st.columns(4)

be1.metric(
    "Uber Eats Break-Even Commission",
    f"{uber_break_even_commission:.2f}%"
)

be2.metric(
    "DoorDash Break-Even Commission",
    f"{doordash_break_even_commission:.2f}%"
)

be3.metric(
    "Current Delivery Cost / Order",
    f"${current_delivery_cost:.2f}"
)

be4.metric(
    "Break-Even Delivery Cost / Order",
    f"${break_even_delivery_cost:.2f}"
)

# ---------------------------------------------------------
# CHANNEL SUMMARY
# ---------------------------------------------------------

channel_data = pd.DataFrame({

    "Channel": [
        "In-Store",
        "Uber Eats",
        "DoorDash",
        "Self-Delivery"
    ],

    "Revenue": [
        filtered_df["InStoreRevenue"].sum(),
        filtered_df["UberEatsRevenue"].sum(),
        filtered_df["DoorDashRevenue"].sum(),
        filtered_df["SelfDeliveryRevenue"].sum()
    ],

    "Net Profit": [
        filtered_df["InStoreNetProfit"].sum(),
        filtered_df["UberEatsNetProfit"].sum(),
        filtered_df["DoorDashNetProfit"].sum(),
        filtered_df["SelfDeliveryNetProfit"].sum()
    ],

    "Orders": [
        filtered_df["InStoreOrders"].sum(),
        filtered_df["UberEatsOrders"].sum(),
        filtered_df["DoorDashOrders"].sum(),
        filtered_df["SelfDeliveryOrders"].sum()
    ]
})

channel_data["Margin"] = (
    channel_data["Net Profit"] /
    channel_data["Revenue"] *
    100
)

channel_data["Profit per Order"] = (
    channel_data["Net Profit"] /
    channel_data["Orders"]
)


# ---------------------------------------------------------
# CHANNEL COMPARISON
# ---------------------------------------------------------

st.subheader("Channel Performance")

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        channel_data,
        x="Channel",
        y=["Revenue", "Net Profit"],
        barmode="group",
        title="Revenue vs Net Profit by Channel"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.bar(
        channel_data,
        x="Channel",
        y="Margin",
        title="Net Profit Margin by Channel",
        text="Margin"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.dataframe(
    channel_data.style.format({
        "Revenue": "${:,.0f}",
        "Net Profit": "${:,.0f}",
        "Orders": "{:,.0f}",
        "Margin": "{:.2f}%",
        "Profit per Order": "${:.2f}"
    }),
    use_container_width=True
)


# ---------------------------------------------------------
# COST BREAKDOWN
# ---------------------------------------------------------

st.subheader("Cost Component Breakdown")

cost_data = pd.DataFrame({

    "Channel": [
        "In-Store",
        "Uber Eats",
        "DoorDash",
        "Self-Delivery"
    ],

    "COGS": [
        (
            filtered_df["InStoreRevenue"]
            * filtered_df["COGSRate"]
        ).sum(),

        (
            filtered_df["UberEatsRevenue"]
            * filtered_df["COGSRate"]
        ).sum(),

        (
            filtered_df["DoorDashRevenue"]
            * filtered_df["COGSRate"]
        ).sum(),

        (
            filtered_df["SelfDeliveryRevenue"]
            * filtered_df["COGSRate"]
        ).sum()
    ],

    "OPEX": [
        (
            filtered_df["InStoreRevenue"]
            * filtered_df["OPEXRate"]
        ).sum(),

        (
            filtered_df["UberEatsRevenue"]
            * filtered_df["OPEXRate"]
        ).sum(),

        (
            filtered_df["DoorDashRevenue"]
            * filtered_df["OPEXRate"]
        ).sum(),

        (
            filtered_df["SelfDeliveryRevenue"]
            * filtered_df["OPEXRate"]
        ).sum()
    ],

    "Commission": [
        0,

        (
            filtered_df["UberEatsRevenue"]
            * filtered_df["CommissionRate"]
        ).sum(),

        (
            filtered_df["DoorDashRevenue"]
            * filtered_df["CommissionRate"]
        ).sum(),

        0
    ],

    "Delivery Cost": [
        0,
        0,
        0,
        filtered_df["SD_DeliveryTotalCost"].sum()
    ]
})

cost_long = cost_data.melt(
    id_vars="Channel",
    var_name="Cost Component",
    value_name="Cost"
)

fig = px.bar(
    cost_long,
    x="Channel",
    y="Cost",
    color="Cost Component",
    title="Cost Structure by Channel",
    barmode="stack"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------------
# WATERFALL
# ---------------------------------------------------------

st.subheader("Revenue-to-Profit Waterfall")

selected_channel = st.selectbox(
    "Select Channel",
    channel_data["Channel"]
)


channel_map = {

    "In-Store": {
        "Revenue": filtered_df["InStoreRevenue"].sum(),
        "COGS": (
            filtered_df["InStoreRevenue"]
            * filtered_df["COGSRate"]
        ).sum(),
        "OPEX": (
            filtered_df["InStoreRevenue"]
            * filtered_df["OPEXRate"]
        ).sum(),
        "Commission": 0,
        "Delivery Cost": 0,
        "Profit": filtered_df["InStoreNetProfit"].sum()
    },

    "Uber Eats": {
        "Revenue": filtered_df["UberEatsRevenue"].sum(),
        "COGS": (
            filtered_df["UberEatsRevenue"]
            * filtered_df["COGSRate"]
        ).sum(),
        "OPEX": (
            filtered_df["UberEatsRevenue"]
            * filtered_df["OPEXRate"]
        ).sum(),
        "Commission": (
            filtered_df["UberEatsRevenue"]
            * filtered_df["CommissionRate"]
        ).sum(),
        "Delivery Cost": 0,
        "Profit": filtered_df["UberEatsNetProfit"].sum()
    },

    "DoorDash": {
        "Revenue": filtered_df["DoorDashRevenue"].sum(),
        "COGS": (
            filtered_df["DoorDashRevenue"]
            * filtered_df["COGSRate"]
        ).sum(),
        "OPEX": (
            filtered_df["DoorDashRevenue"]
            * filtered_df["OPEXRate"]
        ).sum(),
        "Commission": (
            filtered_df["DoorDashRevenue"]
            * filtered_df["CommissionRate"]
        ).sum(),
        "Delivery Cost": 0,
        "Profit": filtered_df["DoorDashNetProfit"].sum()
    },

    "Self-Delivery": {
        "Revenue": filtered_df["SelfDeliveryRevenue"].sum(),
        "COGS": (
            filtered_df["SelfDeliveryRevenue"]
            * filtered_df["COGSRate"]
        ).sum(),
        "OPEX": (
            filtered_df["SelfDeliveryRevenue"]
            * filtered_df["OPEXRate"]
        ).sum(),
        "Commission": 0,
        "Delivery Cost": filtered_df["SD_DeliveryTotalCost"].sum(),
        "Profit": filtered_df["SelfDeliveryNetProfit"].sum()
    }
}


selected = channel_map[selected_channel]

fig = go.Figure(
    go.Waterfall(
        name="Profit",
        orientation="v",

        measure=[
            "absolute",
            "relative",
            "relative",
            "relative",
            "relative",
            "total"
        ],

        x=[
            "Revenue",
            "COGS",
            "OPEX",
            "Commission",
            "Delivery Cost",
            "Net Profit"
        ],

        y=[
            selected["Revenue"],
            -selected["COGS"],
            -selected["OPEX"],
            -selected["Commission"],
            -selected["Delivery Cost"],
            selected["Profit"]
        ]
    )
)

fig.update_layout(
    title=f"Revenue-to-Profit Waterfall — {selected_channel}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------------
# CUISINE HEATMAP
# ---------------------------------------------------------

st.subheader("Cuisine × Channel Profitability")

cuisine_data = filtered_df.groupby("CuisineType").agg(

    InStoreRevenue=("InStoreRevenue", "sum"),
    InStoreProfit=("InStoreNetProfit", "sum"),

    UberRevenue=("UberEatsRevenue", "sum"),
    UberProfit=("UberEatsNetProfit", "sum"),

    DoorDashRevenue=("DoorDashRevenue", "sum"),
    DoorDashProfit=("DoorDashNetProfit", "sum"),

    SelfRevenue=("SelfDeliveryRevenue", "sum"),
    SelfProfit=("SelfDeliveryNetProfit", "sum")
)

cuisine_margin = pd.DataFrame({

    "In-Store": (
        cuisine_data["InStoreProfit"] /
        cuisine_data["InStoreRevenue"] * 100
    ),

    "Uber Eats": (
        cuisine_data["UberProfit"] /
        cuisine_data["UberRevenue"] * 100
    ),

    "DoorDash": (
        cuisine_data["DoorDashProfit"] /
        cuisine_data["DoorDashRevenue"] * 100
    ),

    "Self-Delivery": (
        cuisine_data["SelfProfit"] /
        cuisine_data["SelfRevenue"] * 100
    )
})

fig = px.imshow(
    cuisine_margin,
    text_auto=".1f",
    aspect="auto",
    color_continuous_scale="RdYlGn",
    color_continuous_midpoint=0,
    title="Profit Margin by Cuisine and Channel (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------------
# SEGMENT HEATMAP
# ---------------------------------------------------------

st.subheader("Segment × Channel Profitability")

segment_data = filtered_df.groupby("Segment").agg(

    InStoreRevenue=("InStoreRevenue", "sum"),
    InStoreProfit=("InStoreNetProfit", "sum"),

    UberRevenue=("UberEatsRevenue", "sum"),
    UberProfit=("UberEatsNetProfit", "sum"),

    DoorDashRevenue=("DoorDashRevenue", "sum"),
    DoorDashProfit=("DoorDashNetProfit", "sum"),

    SelfRevenue=("SelfDeliveryRevenue", "sum"),
    SelfProfit=("SelfDeliveryNetProfit", "sum")
)

segment_margin = pd.DataFrame({

    "In-Store": (
        segment_data["InStoreProfit"] /
        segment_data["InStoreRevenue"] * 100
    ),

    "Uber Eats": (
        segment_data["UberProfit"] /
        segment_data["UberRevenue"] * 100
    ),

    "DoorDash": (
        segment_data["DoorDashProfit"] /
        segment_data["DoorDashRevenue"] * 100
    ),

    "Self-Delivery": (
        segment_data["SelfProfit"] /
        segment_data["SelfRevenue"] * 100
    )
})

fig = px.imshow(
    segment_margin,
    text_auto=".1f",
    aspect="auto",
    color_continuous_scale="RdYlGn",
    color_continuous_midpoint=0,
    title="Profit Margin by Segment and Channel (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("### Margin Resilience Interpretation")

st.info(
    "Margin resilience is assessed using channel-level profit margins. "
    "Categories with consistently positive margins across channels indicate "
    "greater margin resilience, while categories with low or negative "
    "aggregator-channel margins indicate greater margin pressure."
)
# ---------------------------------------------------------
# PROFIT VOLATILITY & RISK ANALYSIS
# ---------------------------------------------------------

st.markdown("### Profit Volatility & Risk Analysis")

st.caption(
    "Profit volatility is measured using the standard deviation of "
    "restaurant-level channel profit margins. Loss rate shows the "
    "percentage of restaurants with negative profit in each channel."
)

# Restaurant-level channel margins
risk_df = filtered_df.copy()

risk_df["InStoreMargin"] = (
    risk_df["InStoreNetProfit"] /
    risk_df["InStoreRevenue"] * 100
)

risk_df["UberEatsMargin"] = (
    risk_df["UberEatsNetProfit"] /
    risk_df["UberEatsRevenue"] * 100
)

risk_df["DoorDashMargin"] = (
    risk_df["DoorDashNetProfit"] /
    risk_df["DoorDashRevenue"] * 100
)

risk_df["SelfDeliveryMargin"] = (
    risk_df["SelfDeliveryNetProfit"] /
    risk_df["SelfDeliveryRevenue"] * 100
)


channel_risk_data = []

channel_columns = {
    "In-Store": "InStoreMargin",
    "Uber Eats": "UberEatsMargin",
    "DoorDash": "DoorDashMargin",
    "Self-Delivery": "SelfDeliveryMargin"
}

profit_columns = {
    "In-Store": "InStoreNetProfit",
    "Uber Eats": "UberEatsNetProfit",
    "DoorDash": "DoorDashNetProfit",
    "Self-Delivery": "SelfDeliveryNetProfit"
}

for channel, margin_column in channel_columns.items():

    margins = risk_df[margin_column].dropna()
    profits = risk_df[profit_columns[channel]]

    channel_risk_data.append({
        "Channel": channel,
        "Mean Margin (%)": margins.mean(),
        "Median Margin (%)": margins.median(),
        "Profit Volatility Score": margins.std(),
        "Margin Range (pp)": margins.max() - margins.min(),
        "Loss-Making Restaurants": (profits < 0).sum(),
        "Loss Rate (%)": (profits < 0).mean() * 100
    })


risk_summary = pd.DataFrame(channel_risk_data)

# Risk summary table
st.dataframe(
    risk_summary.style.format({
        "Mean Margin (%)": "{:.2f}%",
        "Median Margin (%)": "{:.2f}%",
        "Profit Volatility Score": "{:.2f}",
        "Margin Range (pp)": "{:.2f}",
        "Loss Rate (%)": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)


# Volatility chart
fig_volatility = px.bar(
    risk_summary,
    x="Channel",
    y="Profit Volatility Score",
    title="Profit Volatility by Channel",
    labels={
        "Profit Volatility Score": "Margin Standard Deviation (percentage points)"
    }
)

st.plotly_chart(
    fig_volatility,
    use_container_width=True
)


# Loss-rate chart
fig_loss_rate = px.bar(
    risk_summary,
    x="Channel",
    y="Loss Rate (%)",
    title="Loss-Making Restaurant Rate by Channel",
    labels={
        "Loss Rate (%)": "Loss Rate (%)"
    }
)

st.plotly_chart(
    fig_loss_rate,
    use_container_width=True
)


st.info(
    "Higher volatility indicates greater variation in restaurant-level "
    "profit margins. Loss rate indicates the proportion of restaurants "
    "generating negative profit through each channel."
)
# ---------------------------------------------------------
# COMMISSION SENSITIVITY
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Sensitivity Analysis</div>',
    unsafe_allow_html=True
)

st.caption(
    "Use the controls below to evaluate how changes in platform "
    "commission and self-delivery cost affect net profitability."
)
st.subheader("Commission Sensitivity")

sens_col1, sens_col2 = st.columns(2)

with sens_col1:
    commission_rate = st.slider(
        "Aggregator Commission Rate (%)",
        min_value=15.0,
        max_value=45.0,
        value=30.0,
        step=0.5
    )

with sens_col2:
    delivery_cost = st.slider(
        "Self-Delivery Cost per Order ($)",
        min_value=1.0,
        max_value=15.0,
        value=float(round(current_delivery_cost, 2)),
        step=0.10
    )

st.caption(
    "Adjust the commission assumption to evaluate how aggregator "
    "profitability changes."
)
st.info(
    f"Current assumptions: {commission_rate:.1f}% aggregator commission "
    f"and ${delivery_cost:.2f} self-delivery cost per order."
)
commission_decimal = commission_rate / 100

uber_scenario_profit = (
    filtered_df["UberEatsRevenue"]
    * (
        1
        - filtered_df["COGSRate"]
        - filtered_df["OPEXRate"]
        - commission_decimal
    )
).sum()

doordash_scenario_profit = (
    filtered_df["DoorDashRevenue"]
    * (
        1
        - filtered_df["COGSRate"]
        - filtered_df["OPEXRate"]
        - commission_decimal
    )
).sum()

# ---------------------------------------------------------
# COMMISSION SENSITIVITY SCENARIOS
# ---------------------------------------------------------

commission_scenarios = [20, 25, 30, 35, 40]

sensitivity_results = []

for rate in commission_scenarios:

    rate_decimal = rate / 100

    uber_profit = (
        filtered_df["UberEatsRevenue"]
        * (
            1
            - filtered_df["COGSRate"]
            - filtered_df["OPEXRate"]
            - rate_decimal
        )
    ).sum()

    doordash_profit = (
        filtered_df["DoorDashRevenue"]
        * (
            1
            - filtered_df["COGSRate"]
            - filtered_df["OPEXRate"]
            - rate_decimal
        )
    ).sum()

    sensitivity_results.append({
        "CommissionRate": rate,
        "UberEatsProfit": uber_profit,
        "DoorDashProfit": doordash_profit
    })


commission_sensitivity = pd.DataFrame(sensitivity_results)


# ---------------------------------------------------------
# COMMISSION SENSITIVITY LINE CHART
# ---------------------------------------------------------

commission_fig = go.Figure()

commission_fig.add_trace(
    go.Scatter(
        x=commission_sensitivity["CommissionRate"],
        y=commission_sensitivity["UberEatsProfit"],
        mode="lines+markers",
        name="Uber Eats"
    )
)

commission_fig.add_trace(
    go.Scatter(
        x=commission_sensitivity["CommissionRate"],
        y=commission_sensitivity["DoorDashProfit"],
        mode="lines+markers",
        name="DoorDash"
    )
)

commission_fig.add_hline(
    y=0,
    line_dash="dash"
)

commission_fig.update_layout(
    title="Aggregator Profit Sensitivity to Commission Rate",
    xaxis_title="Commission Rate (%)",
    yaxis_title="Net Profit ($)",
    hovermode="x unified"
)

st.plotly_chart(
    commission_fig,
    use_container_width=True
)





# ---------------------------------------------------------
# SELF-DELIVERY SENSITIVITY
# ---------------------------------------------------------

st.subheader("Self-Delivery Cost Sensitivity")

delivery_cost = st.slider(
    "Delivery Cost per Order ($)",
    min_value=1.0,
    max_value=15.0,
    value=float(round(current_delivery_cost, 2)),
    step=0.10
)

scenario_delivery_cost = (
    filtered_df["SelfDeliveryOrders"]
    * delivery_cost
).sum()

scenario_self_delivery_profit = (
    filtered_df["SelfDeliveryRevenue"]
    * (
        1
        - filtered_df["COGSRate"]
        - filtered_df["OPEXRate"]
    )
).sum() - scenario_delivery_cost

st.metric(
    "Scenario Self-Delivery Profit",
    f"${scenario_self_delivery_profit:,.0f}"
)

# ---------------------------------------------------------
# SELF-DELIVERY SENSITIVITY LINE CHART
# ---------------------------------------------------------

sensitivity_costs = [1, 3, 5, 7, 9, 11, 12, 14, 15]

self_delivery_sensitivity = []

for cost in sensitivity_costs:

    scenario_delivery_cost = (
        filtered_df["SelfDeliveryOrders"] * cost
    ).sum()

    scenario_profit = (
        filtered_df["SelfDeliveryRevenue"]
        * (
            1
            - filtered_df["COGSRate"]
            - filtered_df["OPEXRate"]
        )
    ).sum() - scenario_delivery_cost

    self_delivery_sensitivity.append({
        "DeliveryCostPerOrder": cost,
        "SelfDeliveryProfit": scenario_profit
    })


self_delivery_sensitivity_df = pd.DataFrame(
    self_delivery_sensitivity
)


# Calculate break-even delivery cost
break_even_delivery_cost = (
    (
        filtered_df["SelfDeliveryRevenue"]
        * (
            1
            - filtered_df["COGSRate"]
            - filtered_df["OPEXRate"]
        )
    ).sum()
    / filtered_df["SelfDeliveryOrders"].sum()
)


fig_self_delivery = px.line(
    self_delivery_sensitivity_df,
    x="DeliveryCostPerOrder",
    y="SelfDeliveryProfit",
    markers=True,
    title="Self-Delivery Profit Sensitivity to Delivery Cost"
)


# Zero-profit reference line
fig_self_delivery.add_hline(
    y=0,
    line_dash="dash"
)


# Break-even delivery-cost reference line
fig_self_delivery.add_vline(
    x=break_even_delivery_cost,
    line_dash="dash"
)


fig_self_delivery.update_layout(
    xaxis_title="Delivery Cost per Order ($)",
    yaxis_title="Self-Delivery Net Profit ($)"
)


st.plotly_chart(
    fig_self_delivery,
    use_container_width=True
)

# ---------------------------------------------------------
# RESTAURANT PROFITABILITY
# ---------------------------------------------------------

st.subheader("Restaurant-Level Profitability")

restaurant_summary = filtered_df[
    [
        "RestaurantName",
        "CuisineType",
        "Segment",
        "TotalRevenue",
        "TotalNetProfit",
        "OverallProfitMargin",
        "NetProfitPerOrder"
    ]
].copy()

restaurant_summary = restaurant_summary.sort_values(
    "TotalNetProfit"
)

st.dataframe(
    restaurant_summary.style.format({
        "TotalRevenue": "${:,.0f}",
        "TotalNetProfit": "${:,.0f}",
        "OverallProfitMargin": "{:.2%}",
        "NetProfitPerOrder": "${:.2f}"
    }),
    width="stretch",
    hide_index=True
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "SkyCity Auckland Restaurants & Bars | "
    "Multi-Channel Restaurant Profitability Analysis"
)
