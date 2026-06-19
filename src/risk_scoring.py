import pandas as pd
import numpy as np

def calculate_risk_scores(df_design, df_cost, df_operations):
    """
    Calculates the building performance risk score (0-12) for each building.
    Inputs: Cleaned DataFrames for design, costs, and operations.
    Output: DataFrame with building_id, risk_score, and risk_category.
    """
    # Merge datasets temporarily to calculate features
    df = df_design.merge(df_cost, on='building_id').merge(df_operations, on='building_id')
    
    # Calculate derived columns needed for risk factors if not already present
    df['building_age'] = 2024 - df['year_built']
    df['operating_cost_per_sqft'] = df['annual_operating_cost'] / df['floor_area_sqft']
    df['water_per_sqft'] = df['water_use_gallons'] / df['floor_area_sqft']
    
    # Calculate type-specific 80th percentiles
    eui_80th = df.groupby('building_type')['energy_use_intensity_kbtu_sqft'].transform(lambda x: x.quantile(0.80))
    emissions_80th = df.groupby('building_type')['emissions_intensity'].transform(lambda x: x.quantile(0.80))
    op_cost_80th = df.groupby('building_type')['operating_cost_per_sqft'].transform(lambda x: x.quantile(0.80))
    water_80th = df.groupby('building_type')['water_per_sqft'].transform(lambda x: x.quantile(0.80))
    
    # Risk points initialization
    risk_score = pd.Series(0, index=df.index)
    
    # 1. High Energy Use Intensity
    risk_score += (df['energy_use_intensity_kbtu_sqft'] > eui_80th).astype(int)
    
    # 2. High Carbon Emissions Intensity
    risk_score += (df['emissions_intensity'] > emissions_80th).astype(int)
    
    # 3. High Annual Operating Cost per Sqft
    risk_score += (df['operating_cost_per_sqft'] > op_cost_80th).astype(int)
    
    # 4. High Construction Cost Overrun
    risk_score += (df['cost_overrun_percentage'] > 0.15).astype(int)
    
    # 5. Construction Delay
    risk_score += (df['delay_days'] > 60).astype(int)
    
    # 6. Low Energy Star Score
    risk_score += (df['energy_star_score'] < 50).astype(int)
    
    # 7. Poor Insulation
    risk_score += (df['insulation_level'].str.lower() == 'low').astype(int)
    
    # 8. Inefficient HVAC system
    inefficient_hvacs = ['standard hvac', 'electric resistance']
    risk_score += df['hvac_system_type'].str.lower().isin(inefficient_hvacs).astype(int)
    
    # 9. No Renewable Energy
    # Check if renewable energy flag is False (or 0)
    risk_score += (~df['renewable_energy_flag'].astype(bool)).astype(int)
    
    # 10. Low or no sustainability certification
    low_leeds = ['none', 'certified']
    risk_score += df['leed_certification_level'].str.lower().isin(low_leeds).astype(int)
    
    # 11. High Water Use per Sqft
    risk_score += (df['water_per_sqft'] > water_80th).astype(int)
    
    # 12. Old Building Age
    risk_score += (df['building_age'] > 40).astype(int)
    
    df['building_performance_risk_score'] = risk_score
    
    # Categorize Risk
    # Low Risk: 0–3, Medium Risk: 4–6, High Risk: 7–9, Critical Risk: 10–12
    conditions = [
        (df['building_performance_risk_score'] <= 3),
        (df['building_performance_risk_score'] >= 4) & (df['building_performance_risk_score'] <= 6),
        (df['building_performance_risk_score'] >= 7) & (df['building_performance_risk_score'] <= 9),
        (df['building_performance_risk_score'] >= 10)
    ]
    categories = ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk']
    df['building_performance_risk_category'] = np.select(conditions, categories, default='Medium Risk')
    
    return df[['building_id', 'building_performance_risk_score', 'building_performance_risk_category']]

if __name__ == '__main__':
    # Test execution
    try:
        design = pd.read_csv('data/synthetic/building_design.csv')
        cost = pd.read_csv('data/synthetic/construction_costs.csv')
        ops = pd.read_csv('data/synthetic/building_operations.csv')
        risk_df = calculate_risk_scores(design, cost, ops)
        print("Test Risk Scoring run successful!")
        print(risk_df['building_performance_risk_category'].value_counts())
    except Exception as e:
        print(f"Error during test: {e}")
