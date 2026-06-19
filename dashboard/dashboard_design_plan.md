# Dashboard Design Plan

## 1. Objective and Target Audience
The **Sustainable Building Performance Analytics Dashboard** is designed to help facilities managers, sustainability directors, construction executives, and real estate portfolio managers monitor their assets. It answers:
- Which buildings are underperforming and pose high compliance or operational cost risks?
- How do architectural materials and design variables affect energy and emission levels?
- Which contractors and delay causes drive construction cost overruns?
- How should retrofits be prioritized to maximize energy savings and emission reductions?

---

## 2. Page-by-Page Layout Plan

### Page 1: Executive Overview
*Focus: High-level health metrics of the entire building portfolio.*
- **Top Row - KPI Cards**:
  - Total Buildings (`total_buildings`)
  - Average Construction Cost (`avg_actual_construction_cost`)
  - Average Cost Overrun % (`avg_cost_overrun_pct`)
  - Average Energy Use Intensity (`avg_eui`)
  - Average Annual Operating Cost (`avg_operating_cost`)
  - Average Carbon Emissions (`avg_emissions`)
  - High & Critical Risk Buildings (`high_critical_risk_count`)
  - Average Energy Star Score (`avg_energy_star`)
- **Main Visuals (Grid)**:
  - **Left**: Building Count by Type (Horizontal Bar Chart)
  - **Center**: Risk Category Distribution (Donut Chart - Low, Medium, High, Critical Risk)
  - **Right**: Energy Use Intensity (EUI) by Building Type (Box Plot / Column Chart)
  - **Bottom Row**:
    - Construction Cost vs. Operating Cost (Scatter Plot)
    - Carbon Emissions by Building Type (Stacked Bar Chart)
- **Filters (Sidebar)**:
  - Building Type (Multi-select)
  - Climate Zone (Dropdown)
  - Year Built Range (Slider)

---

### Page 2: Architecture & Design Impact
*Focus: Deep-dive into design decisions and material choices.*
- **Top Row - Filters**:
  - Building Type, Climate Zone, Primary Material, HVAC Type, LEED level.
- **Main Visuals**:
  - **Top Left**: Energy Use Intensity (EUI) by Insulation Level (Low, Medium, High) (Bar Chart)
  - **Top Right**: Energy Use Intensity (EUI) by HVAC Type (Standard HVAC, Heat Pump, etc.) (Bar Chart)
  - **Middle Left**: Energy Star Score by LEED Certification Level (None, Certified, Silver, Gold, Platinum) (Line Chart showing upward trend)
  - **Middle Right**: Carbon Emissions by Primary Material (Bar Chart)
  - **Bottom Left**: Operating Cost per Sqft by Window-to-Wall Ratio (WWR) (Scatter Plot with Trendline)
  - **Bottom Right**: Renewable vs. Non-Renewable Energy Annual Cost Comparison (Clustered Column Chart)

---

### Page 3: Construction Cost & Schedule Performance
*Focus: Construction project management, contractor performance, and delay impacts.*
- **Top Row - Filters**:
  - Contractor, Delay Reason, Building Type, Project Completion Year.
- **Main Visuals**:
  - **Top Left**: Budget vs. Actual Construction Cost (Clustered Column Chart)
  - **Top Right**: Cost Overrun % by Building Type (Horizontal Bar Chart)
  - **Middle Left**: Cost Overrun % by Contractor (Clustered Column Chart)
  - **Middle Right**: Delay Days by Delay Reason (Bar Chart showing Weather, Material Shortages, etc.)
  - **Bottom Left**: Delay Days vs. Cost Overrun % (Scatter Plot with Trendline)
  - **Bottom Right**: Construction Cost per Sqft by Building Type (Bar Chart)

---

### Page 4: Sustainability & Retrofit Prioritization
*Focus: Retrofit selection, emission savings, and payback period optimization.*
- **Top Row - Filters**:
  - Risk Category, Retrofit Priority, Recommended Action, Complexity, LEED level.
- **Main Visuals**:
  - **Top Left**: Retrofit Priority Distribution (Pie Chart - Critical, High, Medium, Low)
  - **Top Right**: Total Annual Savings by Recommended Retrofit Action (Bar Chart)
  - **Middle Left**: Average Payback Period by Retrofit Action (Column Chart)
  - **Middle Right**: Estimated Emissions Reduction % by Retrofit Action (Bar Chart)
  - **Bottom Left**: Critical-Risk Buildings Table (Columns: Building ID, Name, Type, Risk Score, Energy Star, Operating Cost, Recommended Action, Payback Period)
  - **Bottom Right**: Lifecycle Cost per Sqft by Building Type (Horizontal Bar Chart)
