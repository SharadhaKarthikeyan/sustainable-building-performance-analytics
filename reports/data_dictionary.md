# Data Dictionary

This document details the database schema, table structures, and columns for the **Sustainable Building Performance Analytics Dashboard** project.

---

## Table 1: `building_design`
*Physical and design parameters of the buildings in the portfolio.*

| Column Name | Data Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `building_id` | VARCHAR | Unique identifier for the building (Primary Key) | `BLDG_1001` |
| `building_name` | VARCHAR | Human-readable name of the building | `Summit 42 (BLDG_1001)` |
| `building_type` | VARCHAR | Building category classification | `Office` |
| `location_city` | VARCHAR | City where the building is located | `Seattle` |
| `climate_zone` | VARCHAR | US climate zone classification | `4C (Marine)` |
| `year_built` | INTEGER | Year the building was constructed | `1995` |
| `floor_area_sqft` | NUMERIC | Total gross floor area in square feet | `125500` |
| `number_of_floors` | INTEGER | Number of stories above ground | `12` |
| `occupancy_type` | VARCHAR | Primary occupancy classification | `Office` |
| `average_occupancy_rate` | NUMERIC | Average occupancy percentage | `0.85` |
| `primary_material` | VARCHAR | Primary structural/facade material | `Steel` |
| `facade_type` | VARCHAR | Exterior wall classification | `Curtain Wall` |
| `window_to_wall_ratio` | NUMERIC | Ratio of window area to gross wall area | `0.45` |
| `insulation_level` | VARCHAR | Overall thermal insulation tier | `Medium` |
| `hvac_system_type` | VARCHAR | Primary heating, ventilation, air conditioning system | `Heat Pump` |
| `lighting_system_type` | VARCHAR | Primary interior lighting technology | `LED` |
| `renewable_energy_flag` | BOOLEAN | Indicates presence of solar or local green energy | `TRUE` |
| `solar_panel_capacity_kw` | NUMERIC | Peak solar power capacity in kilowatts | `85.0` |
| `green_roof_flag` | BOOLEAN | Indicates presence of vegetated green roof | `FALSE` |
| `leed_certification_level`| VARCHAR | LEED certification level | `Silver` |
| `data_source` | VARCHAR | Indication of synthetic or real data baseline | `Seattle Open Data (2020)` |
| `building_age` | INTEGER | Age of building in years as of 2024 | `29` |
| `sustainability_score_band`| VARCHAR | Categorized sustainability band (High, Moderate, Low) | `Moderate` |
| `building_performance_risk_score` | INTEGER | Calculated 12-factor performance risk score (0 to 12) | `4` |
| `building_performance_risk_category`| VARCHAR | Categorized risk rating (Low, Medium, High, Critical) | `Medium Risk` |
| `lifecycle_cost_estimate` | NUMERIC | 30-year lifecycle cost estimate (CapEx + 30 * OpEx) | `42850300` |
| `lifecycle_cost_per_sqft` | NUMERIC | Lifecycle cost normalized per square foot | `341.44` |

---

## Table 2: `construction_costs`
*Financial and timeline tracking of the building construction.*

| Column Name | Data Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `cost_id` | VARCHAR | Unique identifier for cost record (Primary Key) | `COST_1001` |
| `building_id` | VARCHAR | Foreign key referencing `building_design.building_id` | `BLDG_1001` |
| `estimated_construction_cost` | NUMERIC | Planned construction budget | `35140000` |
| `actual_construction_cost` | NUMERIC | Final construction cost after overruns | `38654000` |
| `cost_overrun_amount` | NUMERIC | Dollar value excess of actual cost over budget | `3514000` |
| `cost_overrun_percentage` | NUMERIC | Percentage overrun | `0.10` |
| `material_cost` | NUMERIC | Total spending on structural materials | `17394300` |
| `labor_cost` | NUMERIC | Total spending on labor forces | `13528900` |
| `equipment_cost` | NUMERIC | Total spending on heavy equipment leasing/use | `3865400` |
| `design_consulting_cost`| NUMERIC | Total spending on architecture & design consulting | `2319200` |
| `permit_cost` | NUMERIC | Total spending on zoning, building permits, compliance | `1546200` |
| `contractor_name` | VARCHAR | General contractor responsible for building | `Apex Builders` |
| `project_start_date` | DATE | Official construction commencement date | `1993-04-12` |
| `planned_completion_date`| DATE | Planned project completion date | `1994-10-18` |
| `actual_completion_date` | DATE | Real project completion date | `1995-01-22` |
| `planned_duration_days` | INTEGER | Budgeted schedule duration in days | `554` |
| `actual_duration_days` | INTEGER | Real schedule duration in days | `650` |
| `delay_days` | INTEGER | Number of schedule delay days | `96` |
| `delay_reason` | VARCHAR | Primary driver behind project delay | `Material Shortage` |
| `cost_per_sqft` | NUMERIC | Actual construction cost normalized by floor area | `308.00` |
| `construction_delay_flag`| BOOLEAN | True if delay days > 0 | `TRUE` |
| `cost_overrun_flag` | BOOLEAN | True if actual cost > estimated cost | `TRUE` |

---

## Table 3: `building_operations`
*Energy, water, carbon emissions, and operational cost metrics for the reporting year (2024).*

| Column Name | Data Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `operation_id` | VARCHAR | Unique identifier for operations record (Primary Key) | `OP_1001` |
| `building_id` | VARCHAR | Foreign key referencing `building_design.building_id` | `BLDG_1001` |
| `reporting_year` | INTEGER | Year operational data was logged | `2024` |
| `annual_energy_use_kbtu` | NUMERIC | Total annual energy consumption in kBtu | `7113958` |
| `energy_use_intensity_kbtu_sqft`| NUMERIC | Site Energy Use Intensity (EUI) in kBtu/sqft/year | `61.7` |
| `annual_electricity_cost`| NUMERIC | Annual electricity utility expense | `213000` |
| `annual_water_cost` | NUMERIC | Annual water utility expense | `28500` |
| `annual_maintenance_cost`| NUMERIC | Annual building maintenance and facility upkeep | `150600` |
| `annual_operating_cost` | NUMERIC | Total operational cost (Electricity + Water + Maintenance) | `392100` |
| `carbon_emissions_metric_tons`| NUMERIC | Annual carbon emissions in metric tons CO2e | `263.3` |
| `energy_star_score` | INTEGER | EPA Energy Star score (1 to 100) | `59` |
| `peak_demand_kw` | NUMERIC | Highest electricity demand peak in kilowatts | `412.5` |
| `water_use_gallons` | NUMERIC | Annual water volume consumed in gallons | `1900000` |
| `operating_cost_per_sqft`| NUMERIC | Total annual operating cost per square foot | `3.12` |
| `emissions_intensity` | NUMERIC | Carbon intensity (kg CO2e emitted per square foot) | `2.09` |
| `energy_efficiency_rating`| VARCHAR | Efficiency rating (Excellent, Good, Fair, Poor) | `Fair` |
| `energy_cost_per_sqft` | NUMERIC | Annual energy cost per square foot | `1.70` |
| `emissions_per_sqft` | NUMERIC | Emissions per square foot in metric tons | `0.0021` |
| `high_energy_use_flag` | BOOLEAN | True if building EUI is in top 20% of its type | `FALSE` |
| `high_emissions_flag` | BOOLEAN | True if emissions intensity is in top 20% of its type | `FALSE` |
| `retrofit_needed_flag` | BOOLEAN | True if Energy Star score < 60 | `TRUE` |

---

## Table 4: `retrofit_recommendations`
*Optimized capital retrofit recommendations to improve energy efficiency.*

| Column Name | Data Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `recommendation_id` | VARCHAR | Unique identifier for recommendation (Primary Key) | `REC_1001` |
| `building_id` | VARCHAR | Foreign key referencing `building_design.building_id` | `BLDG_1001` |
| `recommended_action` | VARCHAR | Targeted energy upgrade action | `HVAC Upgrade` |
| `estimated_retrofit_cost`| NUMERIC | Initial capital expenditure (CapEx) for retrofit | `195000` |
| `estimated_annual_savings`| NUMERIC | Annual operational cost reduction post-upgrade | `46860` |
| `payback_period_years` | NUMERIC | Number of years to recover investment (Cost / Savings) | `4.16` |
| `estimated_emissions_reduction_percent`| NUMERIC | Anticipated carbon footprint reduction percentage | `22.5` |
| `retrofit_priority` | VARCHAR | Prioritized urgency (Critical, High, Medium, Low) | `Critical` |
| `implementation_complexity`| VARCHAR | Complexity scale (Low, Medium, High) | `Medium` |
