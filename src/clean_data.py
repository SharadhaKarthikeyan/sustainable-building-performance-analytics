import os
import pandas as pd
import numpy as np
from risk_scoring import calculate_risk_scores

def clean_and_process_data():
    print("Initializing Data Cleaning and Feature Engineering Pipeline...")
    
    # Check if raw benchmarking dataset exists
    raw_benchmarking_path = 'data/raw/building_energy_benchmarking.csv'
    use_public_data = os.path.exists(raw_benchmarking_path)
    
    # Load raw data
    try:
        if use_public_data:
            print(f"Detected public benchmarking dataset at: {raw_benchmarking_path}")
            df_raw_bench = pd.read_csv(raw_benchmarking_path)
            print(f"Successfully loaded public benchmarking dataset. Shape: {df_raw_bench.shape}")
        else:
            print("No public benchmarking dataset found in data/raw/. Using synthetic operations and design data.")
    except Exception as e:
        print(f"Error loading public dataset: {e}. Falling back to synthetic datasets.")
        use_public_data = False

    # Load synthetic datasets
    try:
        df_design = pd.read_csv('data/synthetic/building_design.csv')
        df_cost = pd.read_csv('data/synthetic/construction_costs.csv')
        df_ops = pd.read_csv('data/synthetic/building_operations.csv')
        df_retrofit = pd.read_csv('data/synthetic/retrofit_recommendations.csv')
        print("Successfully loaded synthetic datasets.")
    except FileNotFoundError:
        print("Synthetic datasets not found. Please run generate_synthetic_data.py first.")
        return

    # Standardize column names to lowercase snake_case
    def standardize_cols(df):
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('[^a-z0-9_]', '', regex=True)
        return df

    df_design = standardize_cols(df_design)
    df_cost = standardize_cols(df_cost)
    df_ops = standardize_cols(df_ops)
    df_retrofit = standardize_cols(df_retrofit)

    # Convert date fields to datetime in construction costs
    df_cost['project_start_date'] = pd.to_datetime(df_cost['project_start_date'])
    df_cost['planned_completion_date'] = pd.to_datetime(df_cost['planned_completion_date'])
    df_cost['actual_completion_date'] = pd.to_datetime(df_cost['actual_completion_date'])

    # Handle missing values
    df_design['leed_certification_level'] = df_design['leed_certification_level'].fillna('None')
    df_cost['delay_reason'] = df_cost['delay_reason'].fillna('None')
    
    # Calculate emissions_intensity if null
    df_ops['emissions_intensity'] = df_ops['emissions_intensity'].fillna(
        df_ops['carbon_emissions_metric_tons'] / df_ops['building_id'].map(df_design.set_index('building_id')['floor_area_sqft']) * 1000
    )

    # Standardize types and missing values
    print("Checking shape and missing values...")
    for name, df in zip(['Design', 'Cost', 'Operations', 'Retrofit'], [df_design, df_cost, df_ops, df_retrofit]):
        print(f"{name} dataset shape: {df.shape}, Nulls: {df.isnull().sum().sum()}, Duplicates: {df.duplicated().sum()}")

    # 1. Feature Engineering: Derived Columns in Design
    df_design['building_age'] = 2024 - df_design['year_built']

    # Map floor area to avoid index alignment issues
    area_map = df_design.set_index('building_id')['floor_area_sqft'].to_dict()
    cost_area = df_cost['building_id'].map(area_map)
    ops_area = df_ops['building_id'].map(area_map)

    # 2. Feature Engineering: Derived Columns in Costs
    df_cost['cost_per_sqft'] = np.round(df_cost['actual_construction_cost'] / cost_area, 2)
    df_cost['construction_delay_flag'] = df_cost['delay_days'] > 0
    df_cost['cost_overrun_flag'] = df_cost['cost_overrun_amount'] > 0

    # 3. Feature Engineering: Derived Columns in Operations
    df_ops['operating_cost_per_sqft'] = np.round(df_ops['annual_operating_cost'] / ops_area, 2)
    df_ops['energy_cost_per_sqft'] = np.round(df_ops['annual_electricity_cost'] / ops_area, 2)
    df_ops['emissions_per_sqft'] = np.round(df_ops['carbon_emissions_metric_tons'] / ops_area, 4)
    
    # Calculate 80th percentile flags for energy and emissions within each building type
    df_merged_temp = df_design[['building_id', 'building_type']].merge(df_ops, on='building_id')
    eui_80th_map = df_merged_temp.groupby('building_type')['energy_use_intensity_kbtu_sqft'].quantile(0.80).to_dict()
    emissions_80th_map = df_merged_temp.groupby('building_type')['emissions_intensity'].quantile(0.80).to_dict()
    
    # Map these to df_ops using df_design's building_type
    b_type_series = df_ops['building_id'].map(df_design.set_index('building_id')['building_type'])
    ops_eui_80th = b_type_series.map(eui_80th_map)
    ops_emissions_80th = b_type_series.map(emissions_80th_map)
    
    df_ops['high_energy_use_flag'] = df_ops['energy_use_intensity_kbtu_sqft'] > ops_eui_80th
    df_ops['high_emissions_flag'] = df_ops['emissions_intensity'] > ops_emissions_80th
    df_ops['retrofit_needed_flag'] = df_ops['energy_star_score'] < 60

    # Calculate Sustainability Score Band
    # High: LEED in ['Platinum', 'Gold'] AND Energy Star >= 75
    # Moderate: LEED in ['Silver', 'Certified'] OR Energy Star >= 55
    # Low: otherwise
    sustainability_bands = []
    for i in range(len(df_design)):
        leed = str(df_design.loc[i, 'leed_certification_level']).lower()
        score = df_ops.loc[i, 'energy_star_score']
        
        if leed in ['platinum', 'gold'] and score >= 75:
            sustainability_bands.append('High')
        elif leed in ['silver', 'certified'] or score >= 55:
            sustainability_bands.append('Moderate')
        else:
            sustainability_bands.append('Low')
            
    df_design['sustainability_score_band'] = sustainability_bands

    # 4. Integrate Building Performance Risk Score
    print("Calculating Building Performance Risk Scores...")
    risk_df = calculate_risk_scores(df_design, df_cost, df_ops)
    
    # Merge risk score back to design and operations
    df_design = df_design.merge(risk_df, on='building_id')

    # 5. Lifecycle Cost Estimations (30-year operational horizon)
    # Lifecycle Cost = Actual Construction Cost + 30 * Annual Operating Cost
    df_merged_all = df_design.merge(df_cost, on='building_id').merge(df_ops, on='building_id')
    
    lifecycle_map = (df_merged_all.set_index('building_id')['actual_construction_cost'] + 
                     30 * df_merged_all.set_index('building_id')['annual_operating_cost']).to_dict()
    df_design['lifecycle_cost_estimate'] = df_design['building_id'].map(lifecycle_map)
    df_design['lifecycle_cost_per_sqft'] = np.round(df_design['lifecycle_cost_estimate'] / df_design['floor_area_sqft'], 2)

    # Save cleaned files to data/processed
    os.makedirs('data/processed', exist_ok=True)
    df_design.to_csv('data/processed/building_design_clean.csv', index=False)
    df_cost.to_csv('data/processed/construction_costs_clean.csv', index=False)
    df_ops.to_csv('data/processed/building_operations_clean.csv', index=False)
    df_retrofit.to_csv('data/processed/retrofit_recommendations_clean.csv', index=False)

    print("Data cleaning and feature engineering complete.")
    print("Cleaned files successfully saved in data/processed/")

if __name__ == '__main__':
    clean_and_process_data()
