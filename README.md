
# Cost Structure and Channel-Wise Profitability Analysis for Multi-Channel Restaurants

## Project Overview

This project analyzes the cost structure and profitability of restaurants operating across multiple sales and delivery channels.

The analysis uses restaurant-level data from SkyCity Auckland Restaurants & Bars to compare profitability across:

- In-Store
- Uber Eats
- DoorDash
- Self-Delivery

The project evaluates revenue, operating costs, platform commissions, delivery logistics costs, profit margins, profitability per order, and profitability risk.

An interactive Streamlit dashboard was developed to allow users to explore profitability by cuisine type, business segment, and channel.

---
## 🚀 Live Demo

🔗 **[View Live Streamlit Dashboard](https://restaurantprofitabilityanalysis-kvzscs2ydjw6rnuxebu7k6.streamlit.app/)**

Explore the interactive dashboard for channel profitability, cost breakdowns, commission sensitivity, self-delivery analysis, cuisine/segment comparisons, and profitability risk.

## Business Problem

Restaurants operating across multiple channels face different cost structures.

In-store orders generally have lower variable distribution costs, while aggregator platforms such as Uber Eats and DoorDash provide additional order volume but introduce platform commission costs.

Self-delivery provides greater control over the delivery process but introduces direct logistics expenses.

The key business challenge is therefore to understand:

- Which channels generate sustainable profit?
- How strongly do aggregator commissions affect margins?
- How sensitive is self-delivery profitability to delivery costs?
- Which cuisines and business segments are more resilient to channel-level cost pressure?
- Which restaurants and channel strategies are loss-prone?

---

## Project Objectives

1. Compare net profitability across In-Store, Uber Eats, DoorDash, and Self-Delivery channels.
2. Validate revenue, order, cost, and profit calculations.
3. Calculate channel-level profit margins and profit per order.
4. Quantify aggregator commission impact.
5. Analyze self-delivery logistics economics.
6. Evaluate commission and delivery-cost sensitivity.
7. Compare profitability across cuisine types and business segments.
8. Identify loss-making restaurants and channel strategies.
9. Measure profit volatility and channel-level risk.
10. Develop an interactive Streamlit dashboard for business analysis.

---

## Dataset

The dataset contains restaurant-level operational and financial information.

Key fields include:

- RestaurantID
- RestaurantName
- CuisineType
- Segment
- Subregion
- AOV
- MonthlyOrders
- InStoreOrders
- UberEatsOrders
- DoorDashOrders
- SelfDeliveryOrders
- InStoreRevenue
- UberEatsRevenue
- DoorDashRevenue
- SelfDeliveryRevenue
- COGSRate
- OPEXRate
- CommissionRate
- DeliveryCostPerOrder
- SD_DeliveryTotalCost
- InStoreNetProfit
- UberEatsNetProfit
- DoorDashNetProfit
- SelfDeliveryNetProfit

Dataset size:

**1,696 restaurant records and 30 variables**

---

## Methodology

### 1. Data Validation

The dataset was validated for:

- Missing values
- Duplicate records
- Duplicate Restaurant IDs
- Order reconciliation
- Revenue reconciliation
- Channel profit calculations
- Self-delivery cost calculations
- Delivery-order share calculations

All major order, revenue, profit, and cost reconciliation checks passed within the defined tolerance.

A source-data inconsistency was identified in the `InStoreShare` field. The original field was retained, while a validated in-store share was calculated for analytical purposes.

---

### 2. Derived Metrics

The following analytical metrics were created:

- Total Revenue
- Total Net Profit
- Overall Profit Margin
- Net Profit per Order
- Channel Profit Margin
- Channel Profit per Order
- Total Commission Cost
- Commission Drag Index
- Self-Delivery Cost Ratio
- Self-Delivery ROI

---

### 3. Channel Margin Analysis

Profitability was compared across:

- In-Store
- Uber Eats
- DoorDash
- Self-Delivery

Both absolute net profit and percentage margin were evaluated to distinguish revenue scale from profitability efficiency.

---

### 4. Cost Component Decomposition

Channel-level costs were separated into:

- COGS
- OPEX
- Aggregator Commission
- Self-Delivery Logistics Cost

This allows the effect of different cost structures on net profit to be evaluated.

---

### 5. Commission and Delivery-Cost Sensitivity

Aggregator profitability was tested under different commission assumptions.

Self-delivery profitability was tested under different delivery-cost-per-order assumptions.

Break-even thresholds were calculated for both:

- Aggregator commission rates
- Self-delivery delivery costs

---

### 6. Cuisine and Segment Analysis

Profit margins were compared across:

- Cuisine types
- Business segments
- Distribution channels

Heatmaps were created to identify channel combinations with relatively stronger or weaker margins.

---

### 7. Restaurant-Level Profitability

Restaurant-level profitability was analyzed using:

- Total Revenue
- Total Net Profit
- Profit Margin
- Profit per Order

Loss-making restaurants were separately identified and analyzed by cuisine and segment.

---

### 8. Profit Volatility and Risk

Channel risk was evaluated using:

- Mean profit margin
- Median profit margin
- Profit Volatility Score
- Margin range
- Loss-making restaurant count
- Loss rate

The Profit Volatility Score is defined as the standard deviation of restaurant-level channel profit margins, expressed in percentage points.

---

## Key KPIs

| KPI | Definition |
|---|---|
| Net Profit per Order | Total Net Profit / Total Monthly Orders |
| Channel Margin % | Channel Net Profit / Channel Revenue |
| Commission Drag Index | Total Aggregator Commission / Total Restaurant Revenue |
| Self-Delivery ROI | Self-Delivery Net Profit / Self-Delivery Delivery Cost |
| Profit Volatility Score | Standard deviation of restaurant-level channel margins |
| Loss Rate | Percentage of restaurants with negative channel net profit |

---

## Key Results

### Portfolio-Level Results

- Total Revenue: approximately **$77.74M**
- Total Net Profit: approximately **$7.87M**
- Overall Profit Margin: approximately **10.12%**
- Net Profit per Order: approximately **$3.90**
- Commission Drag Index: approximately **18.39%**

### Channel-Level Results

| Channel | Revenue | Net Profit | Margin |
|---|---:|---:|---:|
| In-Store | $14.28M | $3.83M | 26.80% |
| Uber Eats | $30.82M | $0.26M | 0.84% |
| DoorDash | $16.79M | $0.15M | 0.90% |
| Self-Delivery | $15.85M | $3.63M | 22.89% |

### Break-Even Analysis

- Uber Eats break-even commission: approximately **30.87%**
- DoorDash break-even commission: approximately **30.92%**
- Current average self-delivery cost: approximately **$3.12/order**
- Self-delivery break-even cost: approximately **$11.94/order**

---

## Risk Findings

The analysis identified differences in profitability stability across channels.

Uber Eats and DoorDash each have approximately **31.72% of restaurants generating negative channel-level profit**, while Self-Delivery has approximately **5.31%** and In-Store has **0%** in the analyzed dataset.

Channel-level margin volatility is approximately 12 percentage points across the analyzed channels.

---

## Interactive Dashboard

The Streamlit dashboard provides:

- Portfolio KPI cards
- Channel profitability comparison
- Cost component breakdown
- Revenue-to-profit waterfall
- Cuisine × Channel heatmap
- Segment × Channel heatmap
- Margin resilience analysis
- Profit volatility and risk analysis
- Restaurant-level profitability
- Commission sensitivity analysis
- Self-delivery cost sensitivity analysis
- Break-even indicators
- Cuisine and segment filters

---

## Dashboard Filters

Users can filter the analysis by:

- Cuisine Type
- Business Segment

The dashboard dynamically recalculates the displayed KPIs and analytical outputs based on the selected filters.

---

## Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Jupyter Notebook

---

## Project Structure

```text
restaurant-profitability-analysis/
│
├── data/
│   └── SkyCity Auckland Restaurants & Bars.csv
│
├── notebooks/
│   └── dataInspection.ipynb
│
├── dashboard/
│   └── app.py
│
├── outputs/
│
├── reports/
│
├── README.md
│
└── requirements.txt
