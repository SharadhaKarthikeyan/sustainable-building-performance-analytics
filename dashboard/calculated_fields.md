# Calculated Fields: Power BI DAX & Tableau Formulas

This reference guide provides the exact formulas to implement portfolio KPIs in both Power BI (DAX) and Tableau.

---

## 1. Portfolio Size & Baseline

### Total Buildings
* **Power BI DAX**:
  ```dax
  Total Buildings = DISTINCTCOUNT(building_performance_dashboard_data[building_id])
  ```
* **Tableau**:
  ```tableau
  COUNTD([Building Id])
  ```

### Average Construction Cost
* **Power BI DAX**:
  ```dax
  Avg Construction Cost = AVERAGE(building_performance_dashboard_data[estimated_construction_cost])
  ```
* **Tableau**:
  ```tableau
  AVG([Estimated Construction Cost])
  ```

---

## 2. Construction Overruns & Delays

### Cost Overrun %
* **Power BI DAX**:
  ```dax
  Cost Overrun % = DIVIDE(
      SUM(building_performance_dashboard_data[cost_overrun_amount]),
      SUM(building_performance_dashboard_data[estimated_construction_cost]),
      0
  )
  ```
* **Tableau**:
  ```tableau
  SUM([Cost Overrun Amount]) / SUM([Estimated Construction Cost])
  ```

### Cost Overrun Flag
* **Power BI DAX**:
  ```dax
  Cost Overrun Flag = IF(building_performance_dashboard_data[cost_overrun_amount] > 0, 1, 0)
  ```
* **Tableau**:
  ```tableau
  IF [Cost Overrun Amount] > 0 THEN 1 ELSE 0 END
  ```

### Average Delay Days
* **Power BI DAX**:
  ```dax
  Avg Delay Days = AVERAGE(building_performance_dashboard_data[delay_days])
  ```
* **Tableau**:
  ```tableau
  AVG([Delay Days])
  ```

### Delayed Project %
* **Power BI DAX**:
  ```dax
  Delayed Project % = DIVIDE(
      CALCULATE(COUNTROWS(building_performance_dashboard_data), building_performance_dashboard_data[delay_days] > 0),
      [Total Buildings],
      0
  )
  ```
* **Tableau**:
  ```tableau
  SUM(IF [Delay Days] > 0 THEN 1 ELSE 0 END) / COUNTD([Building Id])
  ```

---

## 3. Energy & Carbon Footprint

### Average EUI
* **Power BI DAX**:
  ```dax
  Avg EUI = AVERAGE(building_performance_dashboard_data[energy_use_intensity_kbtu_sqft])
  ```
* **Tableau**:
  ```tableau
  AVG([Energy Use Intensity Kbtu Sqft])
  ```

### Average Operating Cost
* **Power BI DAX**:
  ```dax
  Avg Operating Cost = AVERAGE(building_performance_dashboard_data[annual_operating_cost])
  ```
* **Tableau**:
  ```tableau
  AVG([Annual Operating Cost])
  ```

### Operating Cost per Sqft
* **Power BI DAX**:
  ```dax
  Operating Cost per Sqft = DIVIDE(
      SUM(building_performance_dashboard_data[annual_operating_cost]),
      SUM(building_performance_dashboard_data[floor_area_sqft]),
      0
  )
  ```
* **Tableau**:
  ```tableau
  SUM([Annual Operating Cost]) / SUM([Floor Area Sqft])
  ```

### Average Carbon Emissions
* **Power BI DAX**:
  ```dax
  Avg Carbon Emissions = AVERAGE(building_performance_dashboard_data[carbon_emissions_metric_tons])
  ```
* **Tableau**:
  ```tableau
  AVG([Carbon Emissions Metric Tons])
  ```

### Emissions Intensity
* **Power BI DAX**:
  ```dax
  Avg Emissions Intensity = AVERAGE(building_performance_dashboard_data[emissions_intensity])
  ```
* **Tableau**:
  ```tableau
  AVG([Emissions Intensity])
  ```

---

## 4. Sustainability & Portfolio Risks

### Renewable Energy Adoption Rate
* **Power BI DAX**:
  ```dax
  Renewable Adoption Rate = DIVIDE(
      CALCULATE(COUNTROWS(building_performance_dashboard_data), building_performance_dashboard_data[renewable_energy_flag] = TRUE),
      [Total Buildings],
      0
  )
  ```
* **Tableau**:
  ```tableau
  SUM(IF [Renewable Energy Flag] = TRUE THEN 1 ELSE 0 END) / COUNTD([Building Id])
  ```

### High Risk Building Count
* **Power BI DAX**:
  ```dax
  High Risk Buildings = CALCULATE(
      DISTINCTCOUNT(building_performance_dashboard_data[building_id]),
      building_performance_dashboard_data[building_performance_risk_category] = "High Risk"
  )
  ```
* **Tableau**:
  ```tableau
  COUNTD(IF [Building Performance Risk Category] = "High Risk" THEN [Building Id] END)
  ```

### Critical Risk Building Count
* **Power BI DAX**:
  ```dax
  Critical Risk Buildings = CALCULATE(
      DISTINCTCOUNT(building_performance_dashboard_data[building_id]),
      building_performance_dashboard_data[building_performance_risk_category] = "Critical Risk"
  )
  ```
* **Tableau**:
  ```tableau
  COUNTD(IF [Building Performance Risk Category] = "Critical Risk" THEN [Building Id] END)
  ```

### High/Critical Risk Percentage
* **Power BI DAX**:
  ```dax
  High or Critical Risk % = DIVIDE(
      [High Risk Buildings] + [Critical Risk Buildings],
      [Total Buildings],
      0
  )
  ```
* **Tableau**:
  ```tableau
  COUNTD(IF [Building Performance Risk Category] = "High Risk" OR [Building Performance Risk Category] = "Critical Risk" THEN [Building Id] END) / COUNTD([Building Id])
  ```

---

## 5. Retrofits & Investment Performance

### Average Retrofit Cost
* **Power BI DAX**:
  ```dax
  Avg Retrofit Cost = AVERAGE(building_performance_dashboard_data[estimated_retrofit_cost])
  ```
* **Tableau**:
  ```tableau
  AVG([Estimated Retrofit Cost])
  ```

### Estimated Annual Savings
* **Power BI DAX**:
  ```dax
  Total Annual Savings = SUM(building_performance_dashboard_data[estimated_annual_savings])
  ```
* **Tableau**:
  ```tableau
  SUM([Estimated Annual Savings])
  ```

### Average Payback Period (Weighted)
* **Power BI DAX**:
  ```dax
  Avg Payback Years (Weighted) = DIVIDE(
      SUM(building_performance_dashboard_data[estimated_retrofit_cost]),
      SUM(building_performance_dashboard_data[estimated_annual_savings]),
      0
  )
  ```
* **Tableau**:
  ```tableau
  SUM([Estimated Retrofit Cost]) / SUM([Estimated Annual Savings])
  ```

### Lifecycle Cost per Sqft
* **Power BI DAX**:
  ```dax
  Lifecycle Cost per Sqft = DIVIDE(
      SUM(building_performance_dashboard_data[lifecycle_cost_estimate]),
      SUM(building_performance_dashboard_data[floor_area_sqft]),
      0
  )
  ```
* **Tableau**:
  ```tableau
  SUM([Lifecycle Cost Estimate]) / SUM([Floor Area Sqft])
  ```
