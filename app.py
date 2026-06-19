import os
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Sustainable Building Performance Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom css for metric card alignment and clean design
st.markdown("""
<style>
    .metric-container {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #e9ecef;
        text-align: center;
    }
    .metric-value {
        font-size: 20px;
        font-weight: bold;
        color: #0f172a;
    }
    .metric-label {
        font-size: 12px;
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)

# 2. Data Loading with Caching & Robust Error Handling
@st.cache_data
def load_dashboard_data():
    file_path = "dashboard/building_performance_dashboard_data.csv"
    if not os.path.exists(file_path):
        return None, f"Error: Final dataset '{file_path}' was not found. Please run the data preparation pipeline first (e.g., run `python src/prepare_dashboard_data.py`)."
    
    try:
        # Load file, keep default NAs false to preserve 'None' strings correctly
        df = pd.read_csv(file_path, keep_default_na=False)
        
        # Verify required columns
        required_cols = [
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
        
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            return None, f"Error: The dataset is missing required columns: {missing}"
            
        # Clean boolean indicators for correct presentation
        bool_cols = ['renewable_energy_flag', 'green_roof_flag', 'construction_delay_flag']
        for col in bool_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower().map({'true': 'Yes', 'false': 'No', 'yes': 'Yes', 'no': 'No'})
                
        # Numeric conversions
        df['cost_overrun_percentage'] = pd.to_numeric(df['cost_overrun_percentage'], errors='coerce')
        
        return df, None
    except Exception as e:
        return None, f"An exception occurred while reading the dataset: {e}"

# Load data
df, error_msg = load_dashboard_data()

# 3. Header Setup
st.title("Sustainable Building Performance Analytics Dashboard")
st.markdown("Analyze the relationship between architectural design, construction cost, building energy performance, carbon emissions, and lifecycle operating costs.")
st.markdown("**Author:** Sharadha Karthikeyan | *Master's Portfolio Case Study*")
st.markdown("---")

if error_msg:
    st.error(error_msg)
    st.stop()

# 4. Sidebar Filters
st.sidebar.header("Filter Building Portfolio")

# Helper function to generate multiselect filters with default select all
def create_sidebar_multiselect(df, column, label):
    options = sorted(df[column].dropna().unique())
    selected = st.sidebar.multiselect(label, options=options, default=options)
    return selected

selected_type = create_sidebar_multiselect(df, 'building_type', "Building Type")
selected_city = create_sidebar_multiselect(df, 'location_city', "Location City")
selected_climate = create_sidebar_multiselect(df, 'climate_zone', "Climate Zone")
selected_material = create_sidebar_multiselect(df, 'primary_material', "Primary Material")
selected_insulation = create_sidebar_multiselect(df, 'insulation_level', "Insulation Level")
selected_hvac = create_sidebar_multiselect(df, 'hvac_system_type', "HVAC System")
selected_leed = create_sidebar_multiselect(df, 'leed_certification_level', "LEED Level")
selected_renewable = create_sidebar_multiselect(df, 'renewable_energy_flag', "Renewable Energy (Solar)")
selected_risk = create_sidebar_multiselect(df, 'building_performance_risk_category', "Performance Risk Tier")
selected_priority = create_sidebar_multiselect(df, 'retrofit_priority', "Retrofit Priority")
selected_action = create_sidebar_multiselect(df, 'recommended_action', "Recommended Action")

# Apply Filters
df_filtered = df[
    df['building_type'].isin(selected_type) &
    df['location_city'].isin(selected_city) &
    df['climate_zone'].isin(selected_climate) &
    df['primary_material'].isin(selected_material) &
    df['insulation_level'].isin(selected_insulation) &
    df['hvac_system_type'].isin(selected_hvac) &
    df['leed_certification_level'].isin(selected_leed) &
    df['renewable_energy_flag'].isin(selected_renewable) &
    df['building_performance_risk_category'].isin(selected_risk) &
    df['retrofit_priority'].isin(selected_priority) &
    df['recommended_action'].isin(selected_action)
]

# Check if filtered data is empty
if df_filtered.empty:
    st.warning("No building records match the selected sidebar filters. Please adjust the filters in the sidebar.")
    st.stop()

# 5. KPI Cards Row
kpi_cols1 = st.columns(5)
kpi_cols2 = st.columns(5)

# Row 1 KPIs
total_bldgs = len(df_filtered)
avg_const_cost = df_filtered['actual_construction_cost'].mean()
avg_overrun_pct = df_filtered['cost_overrun_percentage'].mean() * 100
avg_eui = df_filtered['energy_use_intensity_kbtu_sqft'].mean()
avg_op_cost = df_filtered['annual_operating_cost'].mean()

with kpi_cols1[0]:
    st.metric("Total Buildings", f"{total_bldgs:,}")
with kpi_cols1[1]:
    st.metric("Avg Actual Cost", f"${avg_const_cost:,.0f}")
with kpi_cols1[2]:
    st.metric("Avg Cost Overrun", f"{avg_overrun_pct:.1f}%")
with kpi_cols1[3]:
    st.metric("Avg EUI", f"{avg_eui:.1f} kBtu/sf")
with kpi_cols1[4]:
    st.metric("Avg Operating Cost", f"${avg_op_cost:,.0f}/yr")

# Row 2 KPIs
avg_emissions = df_filtered['carbon_emissions_metric_tons'].mean()
avg_star = df_filtered['energy_star_score'].mean()
high_risk_mask = df_filtered['building_performance_risk_category'].isin(['High Risk', 'Critical Risk'])
high_risk_count = high_risk_mask.sum()
high_risk_pct = (high_risk_count / total_bldgs) * 100 if total_bldgs > 0 else 0
avg_retrofit_cost = df_filtered['estimated_retrofit_cost'].mean()
tot_savings = df_filtered['estimated_annual_savings'].sum()

with kpi_cols2[0]:
    st.metric("Avg Carbon Emissions", f"{avg_emissions:,.1f} MT")
with kpi_cols2[1]:
    st.metric("Avg Energy Star", f"{avg_star:.1f} / 100")
with kpi_cols2[2]:
    st.metric("High/Critical Risks", f"{high_risk_count:,} ({high_risk_pct:.1f}%)")
with kpi_cols2[3]:
    st.metric("Avg Retrofit Cost", f"${avg_retrofit_cost:,.0f}")
with kpi_cols2[4]:
    st.metric("Est. Annual Savings", f"${tot_savings:,.0f}")

st.markdown("---")

# 6. Dashboard Tabs Setup
tabs = st.tabs([
    "Executive Overview", 
    "Architecture & Design Impact", 
    "Construction Cost & Schedule", 
    "Sustainability & Retrofit", 
    "Building Details", 
    "Insights & Recommendations"
])

# ----------------- TAB 1: EXECUTIVE OVERVIEW -----------------
with tabs[0]:
    st.subheader("Portfolio Health and Baseline Distribution")
    st.markdown("Overview of building types, risk profiles, EUI distributions, and operational cost correlations.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Building Count by Type
        fig_count = px.bar(
            df_filtered['building_type'].value_counts().reset_index(),
            x='count', y='building_type',
            orientation='h',
            title='Building Count by Building Type',
            labels={'count': 'Number of Buildings', 'building_type': 'Building Type'},
            color='building_type',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig_count.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_count, use_container_width=True)
        
        # EUI by Type Box Plot
        fig_eui_box = px.box(
            df_filtered,
            x='energy_use_intensity_kbtu_sqft', y='building_type',
            color='building_type',
            title='Energy Use Intensity (EUI) Distribution by Type',
            labels={'energy_use_intensity_kbtu_sqft': 'Site EUI (kBtu/sqft/year)', 'building_type': 'Building Type'}
        )
        fig_eui_box.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_eui_box, use_container_width=True)
        
    with col2:
        # Risk Category Distribution
        fig_risk = px.pie(
            df_filtered,
            names='building_performance_risk_category',
            title='Portfolio Risk Category Distribution',
            hole=0.4,
            color='building_performance_risk_category',
            color_discrete_map={
                'Low Risk': '#2e7d32', 'Medium Risk': '#fbc02d', 
                'High Risk': '#f57c00', 'Critical Risk': '#d32f2f'
            }
        )
        fig_risk.update_layout(height=350)
        st.plotly_chart(fig_risk, use_container_width=True)
        
        # Construction Cost vs Operating Cost Scatter Plot
        fig_scatter = px.scatter(
            df_filtered,
            x='actual_construction_cost', y='annual_operating_cost',
            color='building_performance_risk_category',
            title='Construction Cost vs. Annual Operating Cost',
            labels={'actual_construction_cost': 'Construction Cost ($)', 'annual_operating_cost': 'Operating Cost ($/year)'},
            color_discrete_map={
                'Low Risk': '#2e7d32', 'Medium Risk': '#fbc02d', 
                'High Risk': '#f57c00', 'Critical Risk': '#d32f2f'
            },
            hover_name='building_name'
        )
        fig_scatter.update_layout(height=350)
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Carbon emissions by type
    fig_emissions = px.bar(
        df_filtered.groupby('building_type')['carbon_emissions_metric_tons'].mean().reset_index(),
        x='building_type', y='carbon_emissions_metric_tons',
        title='Average Annual Carbon Emissions by Building Type',
        labels={'carbon_emissions_metric_tons': 'Metric Tons CO2e', 'building_type': 'Building Type'},
        color='building_type'
    )
    fig_emissions.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_emissions, use_container_width=True)

# ----------------- TAB 2: ARCHITECTURE & DESIGN IMPACT -----------------
with tabs[1]:
    st.subheader("Architectural Design and Materials Impact Analysis")
    st.markdown("Investigate how envelope insulation, glazing ratios, structural materials, HVAC systems, and LEED certifications shape operational metrics.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # EUI by Insulation Level
        ins_df = df_filtered.groupby('insulation_level')['energy_use_intensity_kbtu_sqft'].mean().reset_index()
        # Sort Low -> Medium -> High
        ins_df['insulation_level'] = pd.Categorical(ins_df['insulation_level'], categories=['Low', 'Medium', 'High'], ordered=True)
        ins_df = ins_df.sort_values('insulation_level')
        fig_ins = px.bar(
            ins_df, x='insulation_level', y='energy_use_intensity_kbtu_sqft',
            title='Average EUI by Envelope Insulation Level',
            labels={'energy_use_intensity_kbtu_sqft': 'Avg Site EUI (kBtu/sf)', 'insulation_level': 'Insulation Level'},
            color='insulation_level',
            color_discrete_sequence=['#ff9800', '#2196f3', '#4caf50']
        )
        fig_ins.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_ins, use_container_width=True)
        
        # Energy Star by LEED
        leed_df = df_filtered.groupby('leed_certification_level')['energy_star_score'].mean().reset_index()
        leed_df['leed_certification_level'] = pd.Categorical(leed_df['leed_certification_level'], categories=['None', 'Certified', 'Silver', 'Gold', 'Platinum'], ordered=True)
        leed_df = leed_df.sort_values('leed_certification_level')
        fig_leed = px.line(
            leed_df, x='leed_certification_level', y='energy_star_score',
            title='Average Energy Star Score by LEED Level',
            labels={'energy_star_score': 'Avg Energy Star Score', 'leed_certification_level': 'LEED Certification'},
            markers=True
        )
        fig_leed.update_layout(height=350)
        st.plotly_chart(fig_leed, use_container_width=True)

        # Renewable vs Non-Renewable Operating Cost per Sqft
        ren_df = df_filtered.groupby('renewable_energy_flag')['operating_cost_per_sqft'].mean().reset_index()
        fig_ren = px.bar(
            ren_df, x='renewable_energy_flag', y='operating_cost_per_sqft',
            title='Avg Operating Cost per Sqft (Renewable vs Non-Renewable)',
            labels={'operating_cost_per_sqft': 'Operating Cost ($/sqft)', 'renewable_energy_flag': 'Renewable Energy (Solar)'},
            color='renewable_energy_flag',
            color_discrete_sequence=['#d32f2f', '#2e7d32']
        )
        fig_ren.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_ren, use_container_width=True)
        
    with col2:
        # EUI by HVAC Type
        hvac_df = df_filtered.groupby('hvac_system_type')['energy_use_intensity_kbtu_sqft'].mean().reset_index().sort_values('energy_use_intensity_kbtu_sqft')
        fig_hvac = px.bar(
            hvac_df, y='hvac_system_type', x='energy_use_intensity_kbtu_sqft',
            orientation='h',
            title='Average EUI by HVAC System Type',
            labels={'energy_use_intensity_kbtu_sqft': 'Avg Site EUI (kBtu/sf)', 'hvac_system_type': 'HVAC System Type'},
            color='energy_use_intensity_kbtu_sqft',
            color_continuous_scale='Reds'
        )
        fig_hvac.update_layout(height=350)
        st.plotly_chart(fig_hvac, use_container_width=True)

        # Emissions by Primary Material
        mat_df = df_filtered.groupby('primary_material')['carbon_emissions_metric_tons'].mean().reset_index().sort_values('carbon_emissions_metric_tons', ascending=False)
        fig_mat = px.bar(
            mat_df, x='primary_material', y='carbon_emissions_metric_tons',
            title='Average Carbon Emissions by Primary Material',
            labels={'carbon_emissions_metric_tons': 'Avg Carbon (MT CO2e)', 'primary_material': 'Primary Material'},
            color='primary_material'
        )
        fig_mat.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_mat, use_container_width=True)
        
        # WWR vs Operating Cost Scatter Plot
        fig_wwr = px.scatter(
            df_filtered, x='window_to_wall_ratio', y='operating_cost_per_sqft',
            color='building_type',
            trendline='ols',
            title='Window-to-Wall Ratio vs. Operating Cost per Sqft',
            labels={'window_to_wall_ratio': 'Window-to-Wall Ratio', 'operating_cost_per_sqft': 'Operating Cost ($/sqft)'}
        )
        fig_wwr.update_layout(height=350)
        st.plotly_chart(fig_wwr, use_container_width=True)

# ----------------- TAB 3: CONSTRUCTION COST & SCHEDULE -----------------
with tabs[2]:
    st.subheader("Construction Financial Performance & Schedule Analysis")
    st.markdown("Track CapEx variance, contractor schedule efficiency, delay causes, and their associated cost overruns.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget vs Actual Construction Cost
        cost_sum = df_filtered.groupby('building_type')[['estimated_construction_cost', 'actual_construction_cost']].mean().reset_index()
        fig_bud = px.bar(
            cost_sum, x='building_type', y=['estimated_construction_cost', 'actual_construction_cost'],
            title='Average Estimated vs. Actual Construction Cost',
            labels={'value': 'Average Capital Expenditure ($)', 'building_type': 'Building Type'},
            barmode='group',
            color_discrete_sequence=['#4f46e5', '#ef4444']
        )
        fig_bud.update_layout(height=350)
        st.plotly_chart(fig_bud, use_container_width=True)
        
        # Cost Overrun % by Contractor
        cont_df = df_filtered.groupby('contractor_name')['cost_overrun_percentage'].mean().reset_index().sort_values('cost_overrun_percentage', ascending=False)
        cont_df['cost_overrun_percentage'] = cont_df['cost_overrun_percentage'] * 100
        fig_cont = px.bar(
            cont_df, x='contractor_name', y='cost_overrun_percentage',
            title='Average Cost Overrun % by Contractor',
            labels={'cost_overrun_percentage': 'Avg Cost Overrun (%)', 'contractor_name': 'Contractor'},
            color='cost_overrun_percentage',
            color_continuous_scale='Reds'
        )
        fig_cont.update_layout(height=350)
        st.plotly_chart(fig_cont, use_container_width=True)

        # Delay Days vs Cost Overrun scatter
        fig_del_sc = px.scatter(
            df_filtered, x='delay_days', y='cost_overrun_percentage',
            color='delay_reason',
            trendline='ols',
            title='Delay Days vs. Cost Overrun %',
            labels={'delay_days': 'Delay Days', 'cost_overrun_percentage': 'Cost Overrun %'},
            hover_name='building_name'
        )
        fig_del_sc.update_layout(height=350)
        st.plotly_chart(fig_del_sc, use_container_width=True)
        
    with col2:
        # Cost Overrun % by Building Type
        type_overrun = df_filtered.groupby('building_type')['cost_overrun_percentage'].mean().reset_index().sort_values('cost_overrun_percentage')
        type_overrun['cost_overrun_percentage'] = type_overrun['cost_overrun_percentage'] * 100
        fig_over_type = px.bar(
            type_overrun, y='building_type', x='cost_overrun_percentage',
            orientation='h',
            title='Average Cost Overrun % by Building Type',
            labels={'cost_overrun_percentage': 'Avg Overrun (%)', 'building_type': 'Building Type'},
            color='cost_overrun_percentage',
            color_continuous_scale='Reds'
        )
        fig_over_type.update_layout(height=350)
        st.plotly_chart(fig_over_type, use_container_width=True)

        # Delay Days by Reason
        delay_reason_df = df_filtered[df_filtered['delay_reason'] != 'None'].groupby('delay_reason')['delay_days'].mean().reset_index().sort_values('delay_days', ascending=False)
        fig_del_reason = px.bar(
            delay_reason_df, x='delay_reason', y='delay_days',
            title='Average Delay Duration by Delay Cause',
            labels={'delay_days': 'Avg Delay (Days)', 'delay_reason': 'Primary Delay Reason'},
            color='delay_days',
            color_continuous_scale='Oranges'
        )
        fig_del_reason.update_layout(height=350)
        st.plotly_chart(fig_del_reason, use_container_width=True)
        
        # Cost per Sqft by Building Type
        cost_sqft_df = df_filtered.groupby('building_type')['cost_per_sqft'].mean().reset_index().sort_values('cost_per_sqft', ascending=False)
        fig_cost_sqft = px.bar(
            cost_sqft_df, x='building_type', y='cost_per_sqft',
            title='Average Construction Cost per Square Foot',
            labels={'cost_per_sqft': 'Construction Cost ($/sqft)', 'building_type': 'Building Type'},
            color='cost_per_sqft',
            color_continuous_scale='Blues'
        )
        fig_cost_sqft.update_layout(height=350)
        st.plotly_chart(fig_cost_sqft, use_container_width=True)

# ----------------- TAB 4: SUSTAINABILITY & RETROFIT -----------------
with tabs[3]:
    st.subheader("Sustainability Benchmarks & Retrofit Selection")
    st.markdown("Identify cost-effective carbon reduction measures, calculate energy payback timelines, and prioritize target assets.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Retrofit Priority Distribution
        fig_ret_priority = px.pie(
            df_filtered, names='retrofit_priority',
            title='Retrofit Priority Distribution',
            color='retrofit_priority',
            color_discrete_map={
                'Critical': '#f44336', 'High': '#ff9800', 
                'Medium': '#3f51b5', 'Low': '#4caf50'
            }
        )
        fig_ret_priority.update_layout(height=350)
        st.plotly_chart(fig_ret_priority, use_container_width=True)
        
        # Payback period by retrofit action
        payback_df = df_filtered.groupby('recommended_action')['payback_period_years'].mean().reset_index().sort_values('payback_period_years')
        fig_payback = px.bar(
            payback_df, x='recommended_action', y='payback_period_years',
            title='Average Payback Period by Retrofit Action',
            labels={'payback_period_years': 'Avg Payback (Years)', 'recommended_action': 'Retrofit Action'},
            color='payback_period_years',
            color_continuous_scale='Greens'
        )
        fig_payback.update_layout(height=350)
        st.plotly_chart(fig_payback, use_container_width=True)
        
    with col2:
        # Savings by Retrofit Action
        savings_action_df = df_filtered.groupby('recommended_action')['estimated_annual_savings'].sum().reset_index().sort_values('estimated_annual_savings', ascending=False)
        fig_savings_action = px.bar(
            savings_action_df, x='estimated_annual_savings', y='recommended_action',
            orientation='h',
            title='Total Annual Savings by Recommended Action',
            labels={'estimated_annual_savings': 'Total Savings ($/year)', 'recommended_action': 'Retrofit Action'},
            color='estimated_annual_savings',
            color_continuous_scale='Greens'
        )
        fig_savings_action.update_layout(height=350)
        st.plotly_chart(fig_savings_action, use_container_width=True)

        # Emissions reduction by action
        em_red_df = df_filtered.groupby('recommended_action')['estimated_emissions_reduction_percent'].mean().reset_index().sort_values('estimated_emissions_reduction_percent', ascending=False)
        fig_em_red = px.bar(
            em_red_df, x='recommended_action', y='estimated_emissions_reduction_percent',
            title='Average Emissions Reduction % by Retrofit Action',
            labels={'estimated_emissions_reduction_percent': 'Avg Carbon Reduction (%)', 'recommended_action': 'Retrofit Action'},
            color='estimated_emissions_reduction_percent',
            color_continuous_scale='Viridis'
        )
        fig_em_red.update_layout(height=350)
        st.plotly_chart(fig_em_red, use_container_width=True)

    # Lifecycle cost per sqft by type
    life_df = df_filtered.groupby('building_type')['lifecycle_cost_per_sqft'].mean().reset_index().sort_values('lifecycle_cost_per_sqft', ascending=False)
    fig_life = px.bar(
        life_df, y='building_type', x='lifecycle_cost_per_sqft',
        orientation='h',
        title='Average 30-Year Lifecycle Cost per Square Foot',
        labels={'lifecycle_cost_per_sqft': 'Lifecycle Cost ($/sqft)', 'building_type': 'Building Type'},
        color='lifecycle_cost_per_sqft',
        color_continuous_scale='Purples'
    )
    fig_life.update_layout(height=350)
    st.plotly_chart(fig_life, use_container_width=True)

    # Critical/High Risk Building Table
    st.markdown("---")
    st.subheader("High and Critical Risk Assets (For Immediate Attention)")
    st.markdown("These assets combine low efficiency ratings, aging envelopes, and outdated HVAC systems. Immediate retrofit planning is advised.")
    
    # Filter critical risk and high risk buildings from filtered set
    df_risk_table = df_filtered[df_filtered['building_performance_risk_category'].isin(['High Risk', 'Critical Risk'])].copy()
    
    if df_risk_table.empty:
        st.info("No high-risk or critical-risk assets match the selected filters.")
    else:
        # Reorder and rename columns for display
        risk_cols_select = [
            'building_name', 'building_type', 'building_performance_risk_score', 
            'building_performance_risk_category', 'energy_use_intensity_kbtu_sqft', 
            'annual_operating_cost', 'carbon_emissions_metric_tons', 'recommended_action', 
            'estimated_retrofit_cost', 'estimated_annual_savings', 'payback_period_years'
        ]
        
        # Rename dictionary
        col_rename_dict = {
            'building_name': 'Building Name',
            'building_type': 'Building Type',
            'building_performance_risk_score': 'Risk Score',
            'building_performance_risk_category': 'Risk Category',
            'energy_use_intensity_kbtu_sqft': 'Energy Use Intensity (EUI)',
            'annual_operating_cost': 'Annual Operating Cost ($)',
            'carbon_emissions_metric_tons': 'Carbon Emissions (MT)',
            'recommended_action': 'Recommended Upgrade',
            'estimated_retrofit_cost': 'Upgrade Cost ($)',
            'estimated_annual_savings': 'Annual Savings ($)',
            'payback_period_years': 'Payback (Years)'
        }
        
        df_risk_display = df_risk_table[risk_cols_select].rename(columns=col_rename_dict)
        
        # Format currency fields for presentation
        df_risk_display['Annual Operating Cost ($)'] = df_risk_display['Annual Operating Cost ($)'].map(lambda x: f"${x:,.0f}")
        df_risk_display['Upgrade Cost ($)'] = df_risk_display['Upgrade Cost ($)'].map(lambda x: f"${x:,.0f}")
        df_risk_display['Annual Savings ($)'] = df_risk_display['Annual Savings ($)'].map(lambda x: f"${x:,.0f}")
        df_risk_display['Payback (Years)'] = df_risk_display['Payback (Years)'].map(lambda x: f"{x:.2f}")
        
        st.dataframe(df_risk_display, width="stretch")

# ----------------- TAB 5: BUILDING DETAILS -----------------
with tabs[4]:
    st.subheader("Portfolio Detailed Building Query Panel")
    st.markdown("Query, filter, and extract specific asset records. Click column headers to sort.")
    
    detail_cols = [
        'building_id', 'building_name', 'building_type', 'location_city', 'floor_area_sqft', 
        'primary_material', 'hvac_system_type', 'insulation_level', 'annual_operating_cost', 
        'energy_use_intensity_kbtu_sqft', 'carbon_emissions_metric_tons', 'energy_star_score', 
        'recommended_action', 'retrofit_priority', 'building_performance_risk_score', 
        'building_performance_risk_category'
    ]
    
    # Render interactive dataframe
    st.dataframe(df_filtered[detail_cols], width="stretch")
    
    # CSV Download Button
    csv_data = df_filtered[detail_cols].to_csv(index=False)
    st.download_button(
        label="Download Filtered Building Details (CSV)",
        data=csv_data,
        file_name="filtered_building_performance_data.csv",
        mime="text/csv"
    )

# ----------------- TAB 6: INSIGHTS & RECOMMENDATIONS -----------------
with tabs[5]:
    st.subheader("Business Storytelling Reports")
    st.markdown("Read the master portfolio reports detailing the analytical methodology and key management recommendations.")
    
    report_col1, report_col2 = st.columns(2)
    
    with report_col1:
        st.markdown("### Executive Summary")
        summary_path = "reports/executive_summary.md"
        if os.path.exists(summary_path):
            with open(summary_path, 'r') as f:
                st.markdown(f.read())
        else:
            st.info("Executive Summary report ('reports/executive_summary.md') was not found. Complete reports setup first.")
            
    with report_col2:
        st.markdown("### Insights & actionable recommendations")
        insights_path = "reports/insights_and_recommendations.md"
        if os.path.exists(insights_path):
            with open(insights_path, 'r') as f:
                st.markdown(f.read())
        else:
            st.info("Insights report ('reports/insights_and_recommendations.md') was not found. Complete reports setup first.")
