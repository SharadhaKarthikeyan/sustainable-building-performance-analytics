-- SQL Script to Load/Insert Data into Tables
-- Explains how to load processed CSV files into PostgreSQL and SQLite

-- ==========================================
-- METHOD A: POSTGRESQL (Using COPY command)
-- ==========================================
-- Run these commands as superuser or a user with file privileges.
-- Replace file paths with absolute paths to your data folder.

/*
-- Load Building Design
COPY building_design (
    building_id, building_name, building_type, location_city, climate_zone, 
    year_built, floor_area_sqft, number_of_floors, occupancy_type, average_occupancy_rate, 
    primary_material, facade_type, window_to_wall_ratio, insulation_level, hvac_system_type, 
    lighting_system_type, renewable_energy_flag, solar_panel_capacity_kw, green_roof_flag, 
    leed_certification_level, data_source, building_age, sustainability_score_band, 
    building_performance_risk_score, building_performance_risk_category, 
    lifecycle_cost_estimate, lifecycle_cost_per_sqft
)
FROM '/path/to/sustainable-building-performance-analytics/data/processed/building_design_clean.csv' 
DELIMITER ',' CSV HEADER;

-- Load Construction Costs
COPY construction_costs (
    cost_id, building_id, estimated_construction_cost, actual_construction_cost, 
    cost_overrun_amount, cost_overrun_percentage, contractor_name, project_start_date, 
    planned_duration_days, delay_days, delay_reason, planned_completion_date, 
    actual_duration_days, actual_completion_date, material_cost, labor_cost, 
    equipment_cost, design_consulting_cost, permit_cost, cost_per_sqft, 
    construction_delay_flag, cost_overrun_flag
)
FROM '/path/to/sustainable-building-performance-analytics/data/processed/construction_costs_clean.csv' 
DELIMITER ',' CSV HEADER;

-- Load Building Operations
COPY building_operations (
    operation_id, building_id, reporting_year, annual_energy_use_kbtu, 
    energy_use_intensity_kbtu_sqft, annual_electricity_cost, annual_water_cost, 
    annual_maintenance_cost, annual_operating_cost, carbon_emissions_metric_tons, 
    energy_star_score, peak_demand_kw, water_use_gallons, operating_cost_per_sqft, 
    emissions_intensity, energy_efficiency_rating, energy_cost_per_sqft, 
    emissions_per_sqft, high_energy_use_flag, high_emissions_flag, retrofit_needed_flag
)
FROM '/path/to/sustainable-building-performance-analytics/data/processed/building_operations_clean.csv' 
DELIMITER ',' CSV HEADER;

-- Load Retrofit Recommendations
COPY retrofit_recommendations (
    recommendation_id, building_id, recommended_action, estimated_retrofit_cost, 
    estimated_annual_savings, payback_period_years, estimated_emissions_reduction_percent, 
    retrofit_priority, implementation_complexity
)
FROM '/path/to/sustainable-building-performance-analytics/data/processed/retrofit_recommendations_clean.csv' 
DELIMITER ',' CSV HEADER;

-- Load Flat Dashboard Data
COPY building_performance_dashboard (
    building_id, building_name, building_type, location_city, climate_zone, 
    year_built, building_age, floor_area_sqft, number_of_floors, occupancy_type, 
    average_occupancy_rate, primary_material, facade_type, window_to_wall_ratio, 
    insulation_level, hvac_system_type, lighting_system_type, renewable_energy_flag, 
    solar_panel_capacity_kw, green_roof_flag, leed_certification_level, 
    estimated_construction_cost, actual_construction_cost, cost_overrun_amount, 
    cost_overrun_percentage, cost_per_sqft, contractor_name, delay_days, 
    delay_reason, construction_delay_flag, annual_energy_use_kbtu, 
    energy_use_intensity_kbtu_sqft, annual_electricity_cost, annual_water_cost, 
    annual_maintenance_cost, annual_operating_cost, operating_cost_per_sqft, 
    carbon_emissions_metric_tons, emissions_intensity, energy_star_score, 
    energy_efficiency_rating, recommended_action, estimated_retrofit_cost, 
    estimated_annual_savings, payback_period_years, estimated_emissions_reduction_percent, 
    retrofit_priority, implementation_complexity, lifecycle_cost_estimate, 
    lifecycle_cost_per_sqft, building_performance_risk_score, building_performance_risk_category
)
FROM '/path/to/sustainable-building-performance-analytics/dashboard/building_performance_dashboard_data.csv' 
DELIMITER ',' CSV HEADER;
*/


-- ==========================================
-- METHOD B: SQLITE (Using CLI commands)
-- ==========================================
-- In the SQLite CLI interface, run these commands to set mode and import the CSVs directly:

/*
.mode csv

-- Load Building Design
.import data/processed/building_design_clean.csv building_design

-- Load Construction Costs
.import data/processed/construction_costs_clean.csv construction_costs

-- Load Building Operations
.import data/processed/building_operations_clean.csv building_operations

-- Load Retrofit Recommendations
.import data/processed/retrofit_recommendations_clean.csv retrofit_recommendations

-- Load Flat Dashboard Data
.import dashboard/building_performance_dashboard_data.csv building_performance_dashboard

-- Verify counts
SELECT 'building_design count:', COUNT(*) FROM building_design;
SELECT 'construction_costs count:', COUNT(*) FROM construction_costs;
SELECT 'building_operations count:', COUNT(*) FROM building_operations;
SELECT 'retrofit_recommendations count:', COUNT(*) FROM retrofit_recommendations;
SELECT 'building_performance_dashboard count:', COUNT(*) FROM building_performance_dashboard;
*/
