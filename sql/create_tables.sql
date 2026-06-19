-- SQL Script to Create Tables for Sustainable Building Performance Analytics Project
-- Compatible with SQLite and PostgreSQL

-- Drop tables if they exist to allow clean re-runs
DROP TABLE IF EXISTS building_performance_dashboard;
DROP TABLE IF EXISTS retrofit_recommendations;
DROP TABLE IF EXISTS building_operations;
DROP TABLE IF EXISTS construction_costs;
DROP TABLE IF EXISTS building_design;

-- 1. Create Building Design Table
CREATE TABLE building_design (
    building_id VARCHAR(50) PRIMARY KEY,
    building_name VARCHAR(150),
    building_type VARCHAR(100),
    location_city VARCHAR(100),
    climate_zone VARCHAR(100),
    year_built INTEGER,
    floor_area_sqft NUMERIC,
    number_of_floors INTEGER,
    occupancy_type VARCHAR(100),
    average_occupancy_rate NUMERIC,
    primary_material VARCHAR(100),
    facade_type VARCHAR(100),
    window_to_wall_ratio NUMERIC,
    insulation_level VARCHAR(50),
    hvac_system_type VARCHAR(100),
    lighting_system_type VARCHAR(100),
    renewable_energy_flag BOOLEAN,
    solar_panel_capacity_kw NUMERIC,
    green_roof_flag BOOLEAN,
    leed_certification_level VARCHAR(50),
    data_source VARCHAR(100),
    building_age INTEGER,
    sustainability_score_band VARCHAR(50),
    building_performance_risk_score INTEGER,
    building_performance_risk_category VARCHAR(50),
    lifecycle_cost_estimate NUMERIC,
    lifecycle_cost_per_sqft NUMERIC
);

-- 2. Create Construction Costs Table
CREATE TABLE construction_costs (
    cost_id VARCHAR(50) PRIMARY KEY,
    building_id VARCHAR(50) REFERENCES building_design(building_id),
    estimated_construction_cost NUMERIC,
    actual_construction_cost NUMERIC,
    cost_overrun_amount NUMERIC,
    cost_overrun_percentage NUMERIC,
    material_cost NUMERIC,
    labor_cost NUMERIC,
    equipment_cost NUMERIC,
    design_consulting_cost NUMERIC,
    permit_cost NUMERIC,
    contractor_name VARCHAR(150),
    project_start_date DATE,
    planned_completion_date DATE,
    actual_completion_date DATE,
    planned_duration_days INTEGER,
    actual_duration_days INTEGER,
    delay_days INTEGER,
    delay_reason VARCHAR(100),
    cost_per_sqft NUMERIC,
    construction_delay_flag BOOLEAN,
    cost_overrun_flag BOOLEAN
);

-- 3. Create Building Operations Table
CREATE TABLE building_operations (
    operation_id VARCHAR(50) PRIMARY KEY,
    building_id VARCHAR(50) REFERENCES building_design(building_id),
    reporting_year INTEGER,
    annual_energy_use_kbtu NUMERIC,
    energy_use_intensity_kbtu_sqft NUMERIC,
    annual_electricity_cost NUMERIC,
    annual_water_cost NUMERIC,
    annual_maintenance_cost NUMERIC,
    annual_operating_cost NUMERIC,
    carbon_emissions_metric_tons NUMERIC,
    energy_star_score INTEGER,
    peak_demand_kw NUMERIC,
    water_use_gallons NUMERIC,
    operating_cost_per_sqft NUMERIC,
    emissions_intensity NUMERIC,
    energy_efficiency_rating VARCHAR(50),
    energy_cost_per_sqft NUMERIC,
    emissions_per_sqft NUMERIC,
    high_energy_use_flag BOOLEAN,
    high_emissions_flag BOOLEAN,
    retrofit_needed_flag BOOLEAN
);

-- 4. Create Retrofit Recommendations Table
CREATE TABLE retrofit_recommendations (
    recommendation_id VARCHAR(50) PRIMARY KEY,
    building_id VARCHAR(50) REFERENCES building_design(building_id),
    recommended_action VARCHAR(150),
    estimated_retrofit_cost NUMERIC,
    estimated_annual_savings NUMERIC,
    payback_period_years NUMERIC,
    estimated_emissions_reduction_percent NUMERIC,
    retrofit_priority VARCHAR(50),
    implementation_complexity VARCHAR(50)
);

-- 5. Create Master Dashboard Flat Table
CREATE TABLE building_performance_dashboard (
    building_id VARCHAR(50) PRIMARY KEY,
    building_name VARCHAR(150),
    building_type VARCHAR(100),
    location_city VARCHAR(100),
    climate_zone VARCHAR(100),
    year_built INTEGER,
    building_age INTEGER,
    floor_area_sqft NUMERIC,
    number_of_floors INTEGER,
    occupancy_type VARCHAR(100),
    average_occupancy_rate NUMERIC,
    primary_material VARCHAR(100),
    facade_type VARCHAR(100),
    window_to_wall_ratio NUMERIC,
    insulation_level VARCHAR(50),
    hvac_system_type VARCHAR(100),
    lighting_system_type VARCHAR(100),
    renewable_energy_flag BOOLEAN,
    solar_panel_capacity_kw NUMERIC,
    green_roof_flag BOOLEAN,
    leed_certification_level VARCHAR(50),
    estimated_construction_cost NUMERIC,
    actual_construction_cost NUMERIC,
    cost_overrun_amount NUMERIC,
    cost_overrun_percentage NUMERIC,
    cost_per_sqft NUMERIC,
    contractor_name VARCHAR(150),
    delay_days INTEGER,
    delay_reason VARCHAR(100),
    construction_delay_flag BOOLEAN,
    annual_energy_use_kbtu NUMERIC,
    energy_use_intensity_kbtu_sqft NUMERIC,
    annual_electricity_cost NUMERIC,
    annual_water_cost NUMERIC,
    annual_maintenance_cost NUMERIC,
    annual_operating_cost NUMERIC,
    operating_cost_per_sqft NUMERIC,
    carbon_emissions_metric_tons NUMERIC,
    emissions_intensity NUMERIC,
    energy_star_score INTEGER,
    energy_efficiency_rating VARCHAR(50),
    recommended_action VARCHAR(150),
    estimated_retrofit_cost NUMERIC,
    estimated_annual_savings NUMERIC,
    payback_period_years NUMERIC,
    estimated_emissions_reduction_percent NUMERIC,
    retrofit_priority VARCHAR(50),
    implementation_complexity VARCHAR(50),
    lifecycle_cost_estimate NUMERIC,
    lifecycle_cost_per_sqft NUMERIC,
    building_performance_risk_score INTEGER,
    building_performance_risk_category VARCHAR(50)
);
