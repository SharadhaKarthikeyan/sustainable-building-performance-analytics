import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for professional charts
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'axes.edgecolor': '#cccccc',
    'axes.linewidth': 0.8,
    'xtick.color': '#333333',
    'ytick.color': '#333333',
    'text.color': '#111111',
    'figure.titlesize': 14,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9
})

# Color palette definition
COLORS_BUILDING_TYPES = sns.color_palette("muted", 8)
COLOR_EMISSIONS = '#2e7d32' # Green
COLOR_COST = '#c62828'      # Red/Crimson
COLOR_RISK = ['#2e7d32', '#fbc02d', '#f57c00', '#d32f2f'] # Low, Med, High, Critical

def generate_visuals():
    print("Generating exploratory data analysis visualizations...")
    
    # Load dashboard-ready data
    data_path = 'dashboard/building_performance_dashboard_data.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Running prepare_dashboard_data.py first.")
        return
        
    df = pd.read_csv(data_path)
    os.makedirs('visuals', exist_ok=True)
    
    # 1. energy_use_by_building_type.png (Box plot of EUI)
    plt.figure(figsize=(10, 6))
    order = df.groupby('building_type')['energy_use_intensity_kbtu_sqft'].median().sort_values(ascending=False).index
    sns.boxplot(
        x='energy_use_intensity_kbtu_sqft', 
        y='building_type', 
        data=df, 
        order=order, 
        palette="viridis",
        hue='building_type',
        legend=False,
        width=0.6,
        linewidth=1.2,
        flierprops={"marker": "o", "markersize": 3, "markerfacecolor": "gray", "alpha": 0.5}
    )
    plt.title('Energy Use Intensity (EUI) Distribution by Building Type\n(Real Benchmarking & Calibrated Baselines)', fontsize=14, pad=15, fontweight='bold')
    plt.xlabel('Site EUI (kBtu/sqft/year)', fontsize=11)
    plt.ylabel('Building Type', fontsize=11)
    plt.tight_layout()
    plt.savefig('visuals/energy_use_by_building_type.png', dpi=300)
    plt.close()
    print("1. Saved energy_use_by_building_type.png")

    # 2. cost_vs_energy_performance.png (Scatter plot: Cost/sqft vs EUI)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x='energy_use_intensity_kbtu_sqft', 
        y='cost_per_sqft', 
        hue='building_performance_risk_category', 
        hue_order=['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk'],
        palette={'Low Risk': '#2e7d32', 'Medium Risk': '#fbc02d', 'High Risk': '#f57c00', 'Critical Risk': '#d32f2f'},
        alpha=0.7, 
        edgecolor='w',
        linewidth=0.5,
        s=35,
        data=df
    )
    plt.title('Construction Cost per Sqft vs Energy Use Intensity (EUI)\nColored by Portfolio Risk Category', fontsize=14, pad=15, fontweight='bold')
    plt.xlabel('Site EUI (kBtu/sqft/year)', fontsize=11)
    plt.ylabel('Actual Construction Cost per Sqft ($/sqft)', fontsize=11)
    plt.legend(title='Building Performance Risk', frameon=True, facecolor='w', edgecolor='gray')
    plt.tight_layout()
    plt.savefig('visuals/cost_vs_energy_performance.png', dpi=300)
    plt.close()
    print("2. Saved cost_vs_energy_performance.png")

    # 3. carbon_emissions_by_material.png (Bar chart of average emissions)
    plt.figure(figsize=(10, 6))
    mat_order = df.groupby('primary_material')['carbon_emissions_metric_tons'].mean().sort_values(ascending=False).index
    sns.barplot(
        x='carbon_emissions_metric_tons',
        y='primary_material',
        data=df,
        order=mat_order,
        palette="crest",
        hue='primary_material',
        legend=False,
        errorbar=None,
        width=0.6
    )
    plt.title('Average Carbon Emissions by Primary Construction Material\n(Enriched Architecture & Structural Analysis)', fontsize=14, pad=15, fontweight='bold')
    plt.xlabel('Average Annual Carbon Emissions (Metric Tons CO2e)', fontsize=11)
    plt.ylabel('Primary Material', fontsize=11)
    plt.tight_layout()
    plt.savefig('visuals/carbon_emissions_by_material.png', dpi=300)
    plt.close()
    print("3. Saved carbon_emissions_by_material.png")

    # 4. risk_category_distribution.png (Donut Chart)
    plt.figure(figsize=(8, 8))
    risk_counts = df['building_performance_risk_category'].value_counts()
    risk_order = ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk']
    risk_counts = risk_counts.reindex(risk_order).fillna(0)
    
    # Custom elegant donut chart
    colors = ['#2e7d32', '#fbc02d', '#f57c00', '#d32f2f']
    plt.pie(
        risk_counts.values, 
        labels=risk_counts.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colors, 
        wedgeprops=dict(width=0.4, edgecolor='w', linewidth=1.5),
        textprops={'fontsize': 10, 'weight': 'bold'}
    )
    plt.title('Distribution of Building Performance Risk Category\nAcross Portfolio (n=2,200)', fontsize=14, pad=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig('visuals/risk_category_distribution.png', dpi=300)
    plt.close()
    print("4. Saved risk_category_distribution.png")

    # 5. retrofit_priority_analysis.png (Scatter/Bubble: Payback vs Emissions Reduction)
    plt.figure(figsize=(10, 6))
    # Group retrofit recommendations
    sns.scatterplot(
        x='payback_period_years', 
        y='estimated_emissions_reduction_percent',
        hue='retrofit_priority',
        hue_order=['Low', 'Medium', 'High', 'Critical'],
        palette={'Low': '#2e7d32', 'Medium': '#3f51b5', 'High': '#ff9800', 'Critical': '#f44336'},
        size='estimated_retrofit_cost',
        sizes=(20, 200),
        alpha=0.7, 
        edgecolor='w',
        data=df
    )
    plt.title('Retrofit Action Analysis: Payback Period vs Emissions Reduction\nBubble Size Proportional to Capital Expenditure Cost', fontsize=14, pad=15, fontweight='bold')
    plt.xlabel('Retrofit Payback Period (Years)', fontsize=11)
    plt.ylabel('Estimated Carbon Emissions Reduction (%)', fontsize=11)
    plt.legend(title='Retrofit Priority & Size', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('visuals/retrofit_priority_analysis.png', dpi=300)
    plt.close()
    print("5. Saved retrofit_priority_analysis.png")
    print("All visuals generated successfully.")

if __name__ == '__main__':
    generate_visuals()
