-- SQL Script: KPI Queries
-- This script contains queries to calculate the 20 Key Performance Indicators (KPIs) defined in the portfolio.
-- Compatible with SQLite and PostgreSQL.

-- 1. Total Buildings
SELECT COUNT(DISTINCT building_id) AS kpi_total_buildings
FROM building_design;

-- 2. Average Construction Cost (Planned/Budgeted)
SELECT ROUND(AVG(estimated_construction_cost), 2) AS kpi_avg_planned_cost
FROM construction_costs;

-- 3. Average Actual Construction Cost
SELECT ROUND(AVG(actual_construction_cost), 2) AS kpi_avg_actual_cost
FROM construction_costs;

-- 4. Average Cost Overrun %
SELECT ROUND(AVG(cost_overrun_percentage) * 100.0, 2) AS kpi_avg_cost_overrun_percent
FROM construction_costs;

-- 5. Total Cost Overrun Amount
SELECT ROUND(SUM(cost_overrun_amount), 2) AS kpi_total_cost_overrun_amount
FROM construction_costs;

-- 6. Average Delay Days
SELECT ROUND(AVG(delay_days), 1) AS kpi_avg_delay_days
FROM construction_costs;

-- 7. Delayed Project Percentage
SELECT 
    ROUND(SUM(CASE WHEN delay_days > 0 THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS kpi_delayed_project_percent
FROM construction_costs;

-- 8. Average Energy Use Intensity (EUI)
SELECT ROUND(AVG(energy_use_intensity_kbtu_sqft), 2) AS kpi_avg_eui
FROM building_operations;

-- 9. Average Operating Cost
SELECT ROUND(AVG(annual_operating_cost), 2) AS kpi_avg_operating_cost
FROM building_operations;

-- 10. Operating Cost per Sqft
-- Total Operating Cost divided by Total Floor Area
SELECT 
    ROUND(SUM(o.annual_operating_cost) / SUM(d.floor_area_sqft), 2) AS kpi_portfolio_operating_cost_per_sqft
FROM building_operations o
JOIN building_design d ON o.building_id = d.building_id;

-- 11. Average Carbon Emissions
SELECT ROUND(AVG(carbon_emissions_metric_tons), 2) AS kpi_avg_carbon_emissions
FROM building_operations;

-- 12. Emissions Intensity (Average kg CO2 per Sqft)
SELECT ROUND(AVG(emissions_intensity), 4) AS kpi_avg_emissions_intensity
FROM building_operations;

-- 13. Average Energy Star Score
SELECT ROUND(AVG(energy_star_score), 1) AS kpi_avg_energy_star_score
FROM building_operations;

-- 14. Renewable Energy Adoption Rate
SELECT 
    ROUND(SUM(CASE WHEN renewable_energy_flag = 1 OR renewable_energy_flag = 'true' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS kpi_renewable_adoption_rate
FROM building_design;

-- 15. High/Critical Risk Building Count
SELECT COUNT(*) AS kpi_high_critical_risk_count
FROM building_design
WHERE building_performance_risk_category IN ('High Risk', 'Critical Risk');

-- 16. High/Critical Risk Building Percentage
SELECT 
    ROUND(SUM(CASE WHEN building_performance_risk_category IN ('High Risk', 'Critical Risk') THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS kpi_high_critical_risk_percent
FROM building_design;

-- 17. Average Retrofit Cost
SELECT ROUND(AVG(estimated_retrofit_cost), 2) AS kpi_avg_retrofit_cost
FROM retrofit_recommendations;

-- 18. Estimated Annual Savings (Total Portfolio Savings)
SELECT ROUND(SUM(estimated_annual_savings), 2) AS kpi_total_retrofit_annual_savings
FROM retrofit_recommendations;

-- 19. Average Payback Period (Weighted by Cost)
-- Weighted Payback = Sum(Cost) / Sum(Savings)
SELECT 
    ROUND(SUM(estimated_retrofit_cost) / SUM(estimated_annual_savings), 2) AS kpi_portfolio_weighted_payback_years
FROM retrofit_recommendations;

-- 20. Estimated Emissions Reduction % (Average)
SELECT ROUND(AVG(estimated_emissions_reduction_percent), 2) AS kpi_avg_emissions_reduction_percent
FROM retrofit_recommendations;
