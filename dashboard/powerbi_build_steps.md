# Power BI Build Steps

This guide provides step-by-step instructions to build the **Sustainable Building Performance Analytics Dashboard** in Power BI Desktop.

---

## Step 1: Import and Clean Data
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Locate and select: `dashboard/building_performance_dashboard_data.csv`.
4. Click **Transform Data** to open the **Power Query Editor**.
5. Verify column data types:
   - `building_id`, `building_name`, `building_type`, `location_city`, `primary_material`, etc. should be **Text**.
   - `floor_area_sqft`, `average_occupancy_rate`, `window_to_wall_ratio`, `estimated_construction_cost`, `actual_construction_cost`, `annual_energy_use_kbtu`, etc. should be **Decimal Number** or **Fixed Decimal Number** (Currency).
   - `year_built`, `building_age`, `number_of_floors`, `delay_days`, `energy_star_score`, `building_performance_risk_score` should be **Whole Number**.
   - `renewable_energy_flag`, `green_roof_flag`, `construction_delay_flag`, etc. should be **True/False** (Boolean).
6. Click **Close & Apply** to load the dataset.

---

## Step 2: Implement Calculated Fields (Measures)
Create a new measure table or create the following DAX measures directly in the loaded table (see `dashboard/calculated_fields.md` for exact formulas):
1. Right-click the table name and select **New Measure**.
2. Enter the formulas for:
   - `Total Buildings`
   - `Avg Construction Cost`
   - `Cost Overrun %`
   - `Avg Delay Days`
   - `Delayed Project %`
   - `Avg EUI`
   - `Avg Operating Cost`
   - `Operating Cost per Sqft`
   - `Avg Carbon Emissions`
   - `Renewable Adoption Rate`
   - `High Risk Buildings`
   - `Critical Risk Buildings`
   - `High or Critical Risk %`
   - `Avg Payback Years (Weighted)`

---

## Step 3: Design Report Page Layouts

### Page 1: Executive Overview
1. Add a **Card** visual for each top-level KPI:
   - `Total Buildings`
   - `Avg Construction Cost`
   - `Cost Overrun %`
   - `Avg EUI`
   - `Avg Operating Cost`
   - `Avg Carbon Emissions`
   - `High or Critical Risk %`
   - `Avg Energy Star Score`
2. Add a **Horizontal Bar Chart**:
   - Axis: `building_type`
   - Value: `Total Buildings` (set to count of `building_id`)
3. Add a **Donut Chart**:
   - Legend: `building_performance_risk_category`
   - Value: `Total Buildings`
4. Add a **Clustered Column Chart** (EUI by Type):
   - Axis: `building_type`
   - Value: `Avg EUI`
5. Add a **Scatter Chart**:
   - X Axis: `actual_construction_cost`
   - Y Axis: `annual_operating_cost`
   - Legend: `building_performance_risk_category`
6. Add **Slicers** for: `building_type`, `climate_zone`, `year_built`.

---

### Page 2: Architecture & Design Impact
1. Add a **Clustered Column Chart** (EUI by Insulation):
   - Axis: `insulation_level` (sort Low, Medium, High)
   - Value: `Avg EUI`
2. Add a **Clustered Column Chart** (EUI by HVAC):
   - Axis: `hvac_system_type`
   - Value: `Avg EUI`
3. Add a **Line Chart** (Energy Star by LEED):
   - Axis: `leed_certification_level`
   - Value: `Avg Energy Star Score`
4. Add a **Clustered Column Chart** (Emissions by Material):
   - Axis: `primary_material`
   - Value: `Avg Carbon Emissions`
5. Add a **Scatter Chart**:
   - X Axis: `window_to_wall_ratio`
   - Y Axis: `operating_cost_per_sqft`
6. Add **Slicers**: `building_type`, `climate_zone`, `primary_material`.

---

### Page 3: Construction Cost & Schedule Performance
1. Add a **Clustered Column Chart** (Budget vs. Actual Cost):
   - Axis: `building_type`
   - Values: `estimated_construction_cost`, `actual_construction_cost`
2. Add a **Horizontal Bar Chart** (Cost Overrun % by Type):
   - Axis: `building_type`
   - Value: `Cost Overrun %`
3. Add a **Horizontal Bar Chart** (Overrun % by Contractor):
   - Axis: `contractor_name`
   - Value: `Cost Overrun %`
4. Add a **Clustered Column Chart** (Delay Days by Reason):
   - Axis: `delay_reason` (filter out 'None')
   - Value: `Avg Delay Days`
5. Add a **Scatter Chart** (Delay vs. Overrun):
   - X Axis: `delay_days`
   - Y Axis: `cost_overrun_percentage`
6. Add **Slicers**: `contractor_name`, `delay_reason`, `building_type`.

---

### Page 4: Sustainability & Retrofit Prioritization
1. Add a **Donut Chart**:
   - Legend: `retrofit_priority`
   - Value: `Total Buildings`
2. Add a **Clustered Column Chart** (Savings by Action):
   - Axis: `recommended_action`
   - Value: `estimated_annual_savings` (Sum)
3. Add a **Clustered Column Chart** (Payback by Action):
   - Axis: `recommended_action`
   - Value: `Avg Payback Years (Weighted)`
4. Add a **Clustered Column Chart** (Emissions Reduction %):
   - Axis: `recommended_action`
   - Value: `estimated_emissions_reduction_percent` (Average)
5. Add a **Table** visual for Critical-Risk assets:
   - Columns: `building_id`, `building_name`, `building_type`, `building_performance_risk_score`, `energy_star_score`, `annual_operating_cost`, `recommended_action`, `payback_period_years`.
   - Apply a Visual Level Filter: `building_performance_risk_category` is `Critical Risk`.
6. Add **Slicers**: `building_performance_risk_category`, `retrofit_priority`, `recommended_action`.

---

## Step 4: Formatting & Visual Theme
1. Go to the **View** tab and select a professional theme (such as **Executive** or a custom Slate theme).
2. Set colors for Risk Categories to be consistent across all pages:
   - `Low Risk`: **Green** (`#2e7d32`)
   - `Medium Risk`: **Yellow** (`#fbc02d`)
   - `High Risk`: **Orange** (`#f57c00`)
   - `Critical Risk`: **Red** (`#d32f2f`)
3. Format all KPI numbers to show thousand separators and appropriate decimals (e.g. 1 decimal for percentages, 0 decimals for whole currencies).
