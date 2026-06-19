# Dashboard KPI Documentation

This document defines the 20 Key Performance Indicators (KPIs) used across the **Sustainable Building Performance Analytics Dashboard**.

---

## 1. Portfolio Size & Financial Baseline

### KPI 1: Total Buildings
- **Business Meaning**: Total assets managed in the portfolio.
- **Formula**: `COUNT(building_id)`
- **Required Columns**: `building_id`
- **Recommended Visual Type**: Card (Single value KPI)

### KPI 2: Average Construction Cost (Planned/Budgeted)
- **Business Meaning**: Average planned building construction budget.
- **Formula**: `AVERAGE(estimated_construction_cost)`
- **Required Columns**: `estimated_construction_cost`
- **Recommended Visual Type**: Card (Single value KPI)

### KPI 3: Average Actual Construction Cost
- **Business Meaning**: Average real construction cost after accounting for delays and overrun adjustments.
- **Formula**: `AVERAGE(actual_construction_cost)`
- **Required Columns**: `actual_construction_cost`
- **Recommended Visual Type**: Card (Single value KPI)

### KPI 4: Average Cost Overrun %
- **Business Meaning**: Average percentage by which projects exceeded their planned budget.
- **Formula**: `AVERAGE(cost_overrun_percentage)`
- **Required Columns**: `cost_overrun_percentage`
- **Recommended Visual Type**: Card (with comparison benchmark indicator)

### KPI 5: Total Cost Overrun Amount
- **Business Meaning**: Absolute capital loss across the portfolio due to budget overruns.
- **Formula**: `SUM(cost_overrun_amount)`
- **Required Columns**: `cost_overrun_amount`
- **Recommended Visual Type**: Card (Formatted as currency)

---

## 2. Construction Schedule Metrics

### KPI 6: Average Delay Days
- **Business Meaning**: Average number of days projects were delayed past their planned duration.
- **Formula**: `AVERAGE(delay_days)`
- **Required Columns**: `delay_days`
- **Recommended Visual Type**: Card

### KPI 7: Delayed Project Percentage
- **Business Meaning**: Proportion of construction projects that suffered any schedule overrun.
- **Formula**: `(COUNTROWS(FILTER(Table, delay_days > 0)) / COUNT(building_id)) * 100`
- **Required Columns**: `delay_days`, `building_id`
- **Recommended Visual Type**: Card or Gauge Chart

---

## 3. Energy & Carbon Footprint

### KPI 8: Average Energy Use Intensity (EUI)
- **Business Meaning**: Core energy benchmark, denoting kBtu consumed per square foot annually. Lower is more efficient.
- **Formula**: `AVERAGE(energy_use_intensity_kbtu_sqft)`
- **Required Columns**: `energy_use_intensity_kbtu_sqft`
- **Recommended Visual Type**: Card (with color thresholds: < 65 Green, > 100 Red)

### KPI 9: Average Operating Cost
- **Business Meaning**: Average annual operating expense (electricity + water + maintenance).
- **Formula**: `AVERAGE(annual_operating_cost)`
- **Required Columns**: `annual_operating_cost`
- **Recommended Visual Type**: Card

### KPI 10: Operating Cost per Sqft
- **Business Meaning**: Normalized operating cost across portfolio assets.
- **Formula**: `SUM(annual_operating_cost) / SUM(floor_area_sqft)`
- **Required Columns**: `annual_operating_cost`, `floor_area_sqft`
- **Recommended Visual Type**: Card or Bullet graph

### KPI 11: Average Carbon Emissions
- **Business Meaning**: Average annual carbon footprint in Metric Tons of CO2e.
- **Formula**: `AVERAGE(carbon_emissions_metric_tons)`
- **Required Columns**: `carbon_emissions_metric_tons`
- **Recommended Visual Type**: Card

### KPI 12: Emissions Intensity
- **Business Meaning**: Normalized environmental impact (kg CO2e emitted per square foot).
- **Formula**: `AVERAGE(emissions_intensity)`
- **Required Columns**: `emissions_intensity`
- **Recommended Visual Type**: Card

### KPI 13: Average Energy Star Score
- **Business Meaning**: Standard national energy efficiency rating (1-100). Higher is better.
- **Formula**: `AVERAGE(energy_star_score)`
- **Required Columns**: `energy_star_score`
- **Recommended Visual Type**: Gauge Chart (Target: 75+)

---

## 4. Sustainability & Risks

### KPI 14: Renewable Energy Adoption Rate
- **Business Meaning**: Percentage of building assets incorporating solar capacity or renewable energy.
- **Formula**: `(COUNTROWS(FILTER(Table, renewable_energy_flag = TRUE)) / COUNT(building_id)) * 100`
- **Required Columns**: `renewable_energy_flag`, `building_id`
- **Recommended Visual Type**: Radial Bar / Donut Chart

### KPI 15: High/Critical Risk Building Count
- **Business Meaning**: Number of buildings flagged as High Risk or Critical Risk (Risk Score >= 7).
- **Formula**: `COUNTROWS(FILTER(Table, building_performance_risk_category IN {"High Risk", "Critical Risk"}))`
- **Required Columns**: `building_performance_risk_category`
- **Recommended Visual Type**: Card (colored Red/Crimson)

### KPI 16: High/Critical Risk Building Percentage
- **Business Meaning**: Proportion of the portfolio facing severe energy, cost, or carbon compliance risks.
- **Formula**: `(High_Critical_Risk_Count / Total_Buildings) * 100`
- **Required Columns**: `building_performance_risk_category`, `building_id`
- **Recommended Visual Type**: Gauge or Card

---

## 5. Retrofit Investment Indicators

### KPI 17: Average Retrofit Cost
- **Business Meaning**: Average initial capital investment required for recommended retrofits.
- **Formula**: `AVERAGE(estimated_retrofit_cost)`
- **Required Columns**: `estimated_retrofit_cost`
- **Recommended Visual Type**: Card

### KPI 18: Estimated Annual Savings
- **Business Meaning**: Sum of annual operating cost savings generated by retrofits.
- **Formula**: `SUM(estimated_annual_savings)`
- **Required Columns**: `estimated_annual_savings`
- **Recommended Visual Type**: Card

### KPI 19: Average Payback Period
- **Business Meaning**: Time needed to recoup retrofit costs.
- **Formula**: `SUM(estimated_retrofit_cost) / SUM(estimated_annual_savings)` (Portfolio-level weighted payback)
- **Required Columns**: `estimated_retrofit_cost`, `estimated_annual_savings`
- **Recommended Visual Type**: Card (Target: < 5 Years)

### KPI 20: Estimated Emissions Reduction %
- **Business Meaning**: Average percentage carbon footprint reduction expected post-retrofit.
- **Formula**: `AVERAGE(estimated_emissions_reduction_percent)`
- **Required Columns**: `estimated_emissions_reduction_percent`
- **Recommended Visual Type**: Card (Gauge)
