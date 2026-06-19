import os
import pandas as pd

def build_dashboard_flat_file():
    print("Preparing final dashboard dataset...")
    
    # Load clean files
    try:
        df_design = pd.read_csv('data/processed/building_design_clean.csv')
        df_cost = pd.read_csv('data/processed/construction_costs_clean.csv')
        df_ops = pd.read_csv('data/processed/building_operations_clean.csv')
        df_retrofit = pd.read_csv('data/processed/retrofit_recommendations_clean.csv')
        print("Cleaned datasets loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error: {e}. Please run clean_data.py first.")
        return

    # Merge design, cost, operations, and retrofits on building_id
    # We use a sequence of inner joins because there is a 1:1 relationship between building records
    df_merged = df_design.merge(df_cost, on='building_id')
    df_merged = df_merged.merge(df_ops, on='building_id')
    df_merged = df_merged.merge(df_retrofit, on='building_id')
    
    print(f"Merged flat dataset shape: {df_merged.shape}")
    
    # Select and order the exact columns requested by the user
    columns_to_keep = [
        'building_id', 'building_name', 'building_type', 'location_city', 'climate_zone', 
        'year_built', 'building_age', 'floor_area_sqft', 'number_of_floors', 'occupancy_type', 
        'average_occupancy_rate', 'primary_material', 'facade_type', 'window_to_wall_ratio', 
        'insulation_level', 'hvac_system_type', 'lighting_system_type', 'renewable_energy_flag', 
        'solar_panel_capacity_kw', 'green_roof_flag', 'leed_certification_level', 
        'estimated_construction_cost', 'actual_construction_cost', 'cost_overrun_amount', 
        'cost_overrun_percentage', 'cost_per_sqft', 'contractor_name', 'delay_days', 
        'delay_reason', 'construction_delay_flag', 'annual_energy_use_kbtu', 
        'energy_use_intensity_kbtu_sqft', 'annual_electricity_cost', 'annual_water_cost', 
        'annual_maintenance_cost', 'annual_operating_cost', 'operating_cost_per_sqft', 
        'carbon_emissions_metric_tons', 'emissions_intensity', 'energy_star_score', 
        'energy_efficiency_rating', 'recommended_action', 'estimated_retrofit_cost', 
        'estimated_annual_savings', 'payback_period_years', 'estimated_emissions_reduction_percent', 
        'retrofit_priority', 'implementation_complexity', 'lifecycle_cost_estimate', 
        'lifecycle_cost_per_sqft', 'building_performance_risk_score', 'building_performance_risk_category'
    ]
    
    # Verify that all requested columns exist
    missing_cols = [col for col in columns_to_keep if col not in df_merged.columns]
    if missing_cols:
        print(f"Warning: The following columns are missing from the merged dataset: {missing_cols}")
        # Just keep the ones that do exist
        columns_to_keep = [col for col in columns_to_keep if col in df_merged.columns]
        
    df_dashboard = df_merged[columns_to_keep].copy()
    
    # Fill None values for string fields that got re-loaded as NaN
    if 'leed_certification_level' in df_dashboard.columns:
        df_dashboard['leed_certification_level'] = df_dashboard['leed_certification_level'].fillna('None')
    if 'delay_reason' in df_dashboard.columns:
        df_dashboard['delay_reason'] = df_dashboard['delay_reason'].fillna('None')
    
    # Ensure target directory exists
    os.makedirs('dashboard', exist_ok=True)
    
    # Save to dashboard directory
    output_path = 'dashboard/building_performance_dashboard_data.csv'
    df_dashboard.to_csv(output_path, index=False)
    
    print(f"Dashboard flat file successfully built and saved to: {output_path}")
    print(f"Final dataset dimensions: {df_dashboard.shape}")
    print(f"Columns in final file: {len(df_dashboard.columns)}")

if __name__ == '__main__':
    build_dashboard_flat_file()
