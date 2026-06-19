-- SQL Script: Analysis Queries
-- This file contains 22 analytical queries to extract building design, construction, operational, and retrofit insights.
-- These queries are designed to be run in SQLite or PostgreSQL.

-- 1. Total Buildings
-- Returns the total number of buildings in the portfolio.
SELECT COUNT(DISTINCT building_id) AS total_buildings
FROM building_design;

-- 2. Average Construction Cost
-- Returns the average planned and actual construction costs across the portfolio.
SELECT 
    AVG(estimated_construction_cost) AS avg_estimated_construction_cost,
    AVG(actual_construction_cost) AS avg_actual_construction_cost,
    AVG(cost_overrun_amount) AS avg_cost_overrun_amount
FROM construction_costs;

-- 3. Average Operating Cost
-- Returns the average annual electricity, water, maintenance, and total operating costs.
SELECT 
    AVG(annual_electricity_cost) AS avg_electricity_cost,
    AVG(annual_water_cost) AS avg_water_cost,
    AVG(annual_maintenance_cost) AS avg_maintenance_cost,
    AVG(annual_operating_cost) AS avg_total_operating_cost
FROM building_operations;

-- 4. Average Energy Use Intensity
-- Returns the average Energy Use Intensity (EUI) in kBtu/sqft/year.
SELECT 
    AVG(energy_use_intensity_kbtu_sqft) AS avg_eui_kbtu_sqft
FROM building_operations;

-- 5. Average Carbon Emissions
-- Returns the average annual carbon emissions in metric tons.
SELECT 
    AVG(carbon_emissions_metric_tons) AS avg_carbon_emissions_metric_tons
FROM building_operations;

-- 6. Building Count by Building Type
-- Group and count the buildings in the portfolio by their building type.
SELECT 
    building_type,
    COUNT(*) AS building_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM building_design), 2) AS percentage_of_portfolio
FROM building_design
GROUP BY building_type
ORDER BY building_count DESC;

-- 7. Energy Use Intensity (EUI) by Building Type
-- Calculates EUI metrics (min, avg, max) grouped by building type.
SELECT 
    d.building_type,
    ROUND(MIN(o.energy_use_intensity_kbtu_sqft), 2) AS min_eui,
    ROUND(AVG(o.energy_use_intensity_kbtu_sqft), 2) AS avg_eui,
    ROUND(MAX(o.energy_use_intensity_kbtu_sqft), 2) AS max_eui
FROM building_design d
JOIN building_operations o ON d.building_id = o.building_id
GROUP BY d.building_type
ORDER BY avg_eui DESC;

-- 8. Carbon Emissions by Primary Material
-- Computes average annual carbon emissions and emissions intensity by construction material.
SELECT 
    d.primary_material,
    ROUND(AVG(o.carbon_emissions_metric_tons), 2) AS avg_carbon_emissions,
    ROUND(AVG(o.emissions_intensity), 4) AS avg_emissions_intensity_kg_sf
FROM building_design d
JOIN building_operations o ON d.building_id = o.building_id
GROUP BY d.primary_material
ORDER BY avg_carbon_emissions DESC;

-- 9. Cost per Square Foot by Building Type
-- Calculates planned and actual construction cost per square foot by building type.
SELECT 
    d.building_type,
    ROUND(AVG(c.estimated_construction_cost / d.floor_area_sqft), 2) AS avg_estimated_cost_per_sqft,
    ROUND(AVG(c.actual_construction_cost / d.floor_area_sqft), 2) AS avg_actual_cost_per_sqft
FROM building_design d
JOIN construction_costs c ON d.building_id = c.building_id
GROUP BY d.building_type
ORDER BY avg_actual_cost_per_sqft DESC;

-- 10. Cost Overrun by Contractor
-- Evaluates budget performance (cost overrun percent and delay days) by contractor.
SELECT 
    contractor_name,
    COUNT(*) AS total_projects,
    SUM(CASE WHEN cost_overrun_flag = 1 OR cost_overrun_flag = 'true' THEN 1 ELSE 0 END) AS overrun_projects,
    ROUND(AVG(cost_overrun_percentage) * 100.0, 2) AS avg_cost_overrun_percent,
    ROUND(AVG(delay_days), 1) AS avg_delay_days
FROM construction_costs
GROUP BY contractor_name
ORDER BY avg_cost_overrun_percent DESC;

-- 11. Average Delay Days by Delay Reason
-- Compiles the average delay duration when delays occur, ordered by severity.
SELECT 
    delay_reason,
    COUNT(*) AS project_count,
    ROUND(AVG(delay_days), 1) AS avg_delay_days
FROM construction_costs
WHERE delay_reason <> 'None'
GROUP BY delay_reason
ORDER BY avg_delay_days DESC;

-- 12. Cost Overrun by Delay Reason
-- Analyzes average cost overrun percentage and average overrun amount by delay reason.
SELECT 
    delay_reason,
    COUNT(*) AS project_count,
    ROUND(AVG(cost_overrun_percentage) * 100.0, 2) AS avg_cost_overrun_percent,
    ROUND(AVG(cost_overrun_amount), 2) AS avg_cost_overrun_amount
FROM construction_costs
WHERE delay_reason <> 'None'
GROUP BY delay_reason
ORDER BY avg_cost_overrun_percent DESC;

-- 13. Energy Efficiency Rating by HVAC Type
-- Cross-tabulates energy efficiency ratings with HVAC system types.
SELECT 
    d.hvac_system_type,
    SUM(CASE WHEN o.energy_efficiency_rating = 'Excellent' THEN 1 ELSE 0 END) AS rating_excellent,
    SUM(CASE WHEN o.energy_efficiency_rating = 'Good' THEN 1 ELSE 0 END) AS rating_good,
    SUM(CASE WHEN o.energy_efficiency_rating = 'Fair' THEN 1 ELSE 0 END) AS rating_fair,
    SUM(CASE WHEN o.energy_efficiency_rating = 'Poor' THEN 1 ELSE 0 END) AS rating_poor,
    COUNT(*) AS total_buildings
FROM building_design d
JOIN building_operations o ON d.building_id = o.building_id
GROUP BY d.hvac_system_type
ORDER BY rating_excellent DESC;

-- 14. Average Energy Star Score by LEED Level
-- Evaluates the operational performance (Energy Star score) across different LEED certification bands.
SELECT 
    d.leed_certification_level,
    COUNT(*) AS building_count,
    ROUND(AVG(o.energy_star_score), 2) AS avg_energy_star_score
FROM building_design d
JOIN building_operations o ON d.building_id = o.building_id
GROUP BY d.leed_certification_level
ORDER BY avg_energy_star_score DESC;

-- 15. Renewable vs Non-Renewable Operating Cost Comparison
-- Explores the operational cost benefits of renewable energy installations.
SELECT 
    d.renewable_energy_flag,
    COUNT(*) AS building_count,
    ROUND(AVG(o.annual_electricity_cost), 2) AS avg_electricity_cost,
    ROUND(AVG(o.carbon_emissions_metric_tons), 2) AS avg_carbon_emissions,
    ROUND(AVG(o.annual_operating_cost / d.floor_area_sqft), 2) AS avg_operating_cost_per_sqft
FROM building_design d
JOIN building_operations o ON d.building_id = o.building_id
GROUP BY d.renewable_energy_flag;

-- 16. High-Risk Buildings by Building Type
-- Counts high-risk and critical-risk buildings grouped by building type.
SELECT 
    building_type,
    COUNT(*) AS total_buildings,
    SUM(CASE WHEN building_performance_risk_category IN ('High Risk', 'Critical Risk') THEN 1 ELSE 0 END) AS high_or_critical_risk_count,
    ROUND(SUM(CASE WHEN building_performance_risk_category IN ('High Risk', 'Critical Risk') THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS risk_rate_percent
FROM building_design
GROUP BY building_type
ORDER BY risk_rate_percent DESC;

-- 17. Critical-Risk Buildings List
-- Lists the highest risk buildings (score >= 10) in the portfolio, including key stats.
SELECT 
    d.building_id,
    d.building_name,
    d.building_type,
    d.year_built,
    d.building_performance_risk_score,
    o.energy_star_score,
    ROUND(o.energy_use_intensity_kbtu_sqft, 2) AS eui,
    ROUND(o.annual_operating_cost, 2) AS annual_op_cost
FROM building_design d
JOIN building_operations o ON d.building_id = o.building_id
WHERE d.building_performance_risk_category = 'Critical Risk'
ORDER BY d.building_performance_risk_score DESC, o.energy_star_score ASC
LIMIT 15;

-- 18. Retrofit Priority Count
-- Aggregates retrofit recommendations by priority tier.
SELECT 
    retrofit_priority,
    COUNT(*) AS recommendation_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM retrofit_recommendations), 2) AS percentage
FROM retrofit_recommendations
GROUP BY retrofit_priority
ORDER BY 
    CASE retrofit_priority
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
        ELSE 5
    END;

-- 19. Estimated Annual Savings by Retrofit Action
-- Summarizes financial and emission savings across recommended actions.
SELECT 
    recommended_action,
    COUNT(*) AS count_recommended,
    ROUND(AVG(estimated_retrofit_cost), 2) AS avg_retrofit_cost,
    ROUND(AVG(estimated_annual_savings), 2) AS avg_annual_savings,
    ROUND(AVG(estimated_emissions_reduction_percent), 2) AS avg_emissions_reduction_percent
FROM retrofit_recommendations
GROUP BY recommended_action
ORDER BY avg_annual_savings DESC;

-- 20. Payback Period by Retrofit Action
-- Ranks recommended actions by average payback period length.
SELECT 
    recommended_action,
    ROUND(MIN(payback_period_years), 2) AS min_payback_years,
    ROUND(AVG(payback_period_years), 2) AS avg_payback_years,
    ROUND(MAX(payback_period_years), 2) AS max_payback_years
FROM retrofit_recommendations
GROUP BY recommended_action
ORDER BY avg_payback_years ASC;

-- 21. Lifecycle Cost per Square Foot by Building Type
-- Computes the 30-year lifecycle cost per square foot for each building type.
SELECT 
    building_type,
    ROUND(AVG(floor_area_sqft), 0) AS avg_floor_area,
    ROUND(AVG(lifecycle_cost_estimate), 2) AS avg_lifecycle_cost,
    ROUND(AVG(lifecycle_cost_per_sqft), 2) AS avg_lifecycle_cost_per_sqft
FROM building_design
GROUP BY building_type
ORDER BY avg_lifecycle_cost_per_sqft DESC;

-- 22. Buildings Recommended for Urgent Retrofit
-- Identifies buildings that combine high risk (High/Critical) and short payback retrofit actions (payback < 5 years).
SELECT 
    d.building_id,
    d.building_name,
    d.building_type,
    d.building_performance_risk_category,
    r.recommended_action,
    ROUND(r.estimated_retrofit_cost, 0) AS cost,
    ROUND(r.estimated_annual_savings, 0) AS annual_savings,
    ROUND(r.payback_period_years, 2) AS payback_years
FROM building_design d
JOIN retrofit_recommendations r ON d.building_id = r.building_id
WHERE d.building_performance_risk_category IN ('High Risk', 'Critical Risk')
  AND r.payback_period_years < 5.0
ORDER BY r.payback_period_years ASC;
