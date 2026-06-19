import os
import numpy as np
import pandas as pd
import datetime

# Ensure reproducibility
np.random.seed(42)

def map_building_type(row):
    bt = str(row.get('BuildingType', '')).lower()
    lput = str(row.get('LargestPropertyUseType', '')).lower()
    
    if 'cos' in bt or 'government' in lput or 'public' in lput:
        return 'Government'
    if 'school' in lput or 'k-12' in lput or 'educational' in lput or 'college' in lput or 'university' in lput:
        return 'Educational'
    if 'medical' in lput or 'hospital' in lput or 'care' in lput or 'healthcare' in lput:
        return 'Healthcare'
    if 'hotel' in lput or 'motel' in lput or 'hospitality' in lput or 'lodging' in lput:
        return 'Hospitality'
    if 'multifamily' in bt or 'housing' in lput or 'residential' in lput or 'apartment' in lput:
        return 'Residential'
    if 'office' in lput or 'commercial' in lput:
        return 'Office'
    if 'retail' in lput or 'store' in lput or 'restaurant' in lput or 'strip mall' in lput or 'supermarket' in lput:
        return 'Retail'
    if 'mixed' in lput or 'multi-use' in lput or 'campus' in bt:
        return 'Mixed Use'
    
    return 'Mixed Use' # fallback

def generate_data(num_records=2200):
    print("Starting generation...")
    
    raw_path = 'data/raw/building_energy_benchmarking.csv'
    use_hybrid = os.path.exists(raw_path)
    
    if use_hybrid:
        try:
            df_raw = pd.read_csv(raw_path)
            for col in ['SiteEUI(kBtu/sf)', 'PropertyGFATotal', 'TotalGHGEmissions', 'SiteEnergyUse(kBtu)', 'ENERGYSTARScore', 'YearBuilt', 'GHGEmissionsIntensity']:
                if col in df_raw.columns:
                    df_raw[col] = df_raw[col].astype(str).str.replace(',', '').str.strip()
                    df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')
            
            if 'GHGEmissionsIntensity' not in df_raw.columns or df_raw['GHGEmissionsIntensity'].isnull().all():
                df_raw['GHGEmissionsIntensity'] = (df_raw['TotalGHGEmissions'] / df_raw['PropertyGFATotal']) * 1000
                
            # Filter for valid buildings
            valid_mask = (
                df_raw['SiteEUI(kBtu/sf)'].notnull() & (df_raw['SiteEUI(kBtu/sf)'] > 0) &
                df_raw['PropertyGFATotal'].notnull() & (df_raw['PropertyGFATotal'] > 0) &
                df_raw['YearBuilt'].notnull() & (df_raw['YearBuilt'] > 0) &
                df_raw['ENERGYSTARScore'].notnull() &
                df_raw['TotalGHGEmissions'].notnull()
            )
            df_valid = df_raw[valid_mask].copy()
            df_valid = df_valid.drop_duplicates(subset=['OSEBuildingID'])
            
            if len(df_valid) >= num_records:
                df_sampled = df_valid.sample(n=num_records, random_state=42).reset_index(drop=True)
            else:
                print(f"Warning: only {len(df_valid)} valid records in public dataset. Taking all and padding.")
                df_sampled = df_valid.reset_index(drop=True)
                # If padding is needed, sample with replacement
                pad_size = num_records - len(df_sampled)
                df_pad = df_valid.sample(n=pad_size, replace=True, random_state=42).reset_index(drop=True)
                df_sampled = pd.concat([df_sampled, df_pad], ignore_index=True)
            
            # Map basic variables
            building_ids = [f"BLDG_{id_num}" for id_num in df_sampled['OSEBuildingID']]
            building_names = df_sampled['BuildingName'].fillna("Building").astype(str).tolist()
            b_types = [map_building_type(row) for _, row in df_sampled.iterrows()]
            b_cities = ['Seattle'] * num_records
            b_climates = ['4C (Marine)'] * num_records
            years_built = df_sampled['YearBuilt'].astype(int).tolist()
            floor_areas = df_sampled['PropertyGFATotal'].astype(float).tolist()
            
            # Number of floors handling
            num_floors = []
            for _, row in df_sampled.iterrows():
                floors = row.get('NumberofFloors')
                if pd.isnull(floors) or floors <= 0:
                    area = row['PropertyGFATotal']
                    floors = max(1, int(area / 20000))
                num_floors.append(int(floors))
            
            occupancy_rates = np.round(np.random.beta(8, 2, size=num_records) * 0.4 + 0.58, 2).tolist()
            
            # Extract real operations variables
            real_euis = df_sampled['SiteEUI(kBtu/sf)'].astype(float).tolist()
            real_aeu = df_sampled['SiteEnergyUse(kBtu)'].astype(float).tolist()
            real_emissions = df_sampled['TotalGHGEmissions'].astype(float).tolist()
            real_energy_star = df_sampled['ENERGYSTARScore'].astype(int).tolist()
            real_emissions_intensity = df_sampled['GHGEmissionsIntensity'].astype(float).tolist()
            
            # Set data flag
            data_source_flag = "Seattle Open Data (2020)"
            
        except Exception as e:
            print(f"Failed to process raw data: {e}. Falling back to pure synthetic data generation.")
            use_hybrid = False

    if not use_hybrid:
        print("Pure Synthetic mode: generating building design from distributions.")
        # Fallback pure synthetic generation
        building_ids = [f"BLDG_{i:04d}" for i in range(1, num_records + 1)]
        building_types = ['Office', 'Residential', 'Educational', 'Healthcare', 'Retail', 'Hospitality', 'Mixed Use', 'Government']
        building_type_weights = [0.25, 0.20, 0.15, 0.08, 0.12, 0.08, 0.07, 0.05]
        cities = ['Seattle', 'Portland', 'San Francisco', 'Bellevue', 'Tacoma', 'Spokane']
        city_weights = [0.35, 0.20, 0.15, 0.15, 0.10, 0.05]
        
        b_types = np.random.choice(building_types, size=num_records, p=building_type_weights).tolist()
        b_cities = np.random.choice(cities, size=num_records, p=city_weights).tolist()
        
        city_climate_map = {
            'Seattle': '4C (Marine)', 'Portland': '4C (Marine)', 'San Francisco': '3C (Marine)',
            'Bellevue': '4C (Marine)', 'Tacoma': '4C (Marine)', 'Spokane': '5B (Cold Dry)'
        }
        b_climates = [city_climate_map[c] for c in b_cities]
        
        name_prefixes = {
            'Office': ['Summit', 'One Union', 'Metropolitan', 'Cascade', 'Skyline', 'Pioneer', 'Horizon', 'EcoWorks'],
            'Residential': ['Greenwood', 'Parkside', 'Pine Heights', 'Lakeside', 'Urban Hearth', 'Bellevue Lofts', 'Ridgeview'],
            'Educational': ['University Hall', 'Centennial Academy', 'Lincoln Prep', 'Science Center', 'Discovery School'],
            'Healthcare': ['Mercy Hospital', 'Swedish Medical Center', 'St. Jude Pavilion', 'Providence Health', 'Swedish East'],
            'Retail': ['Town Center', 'Gateway Mall', 'Plaza 500', 'Cascade Retail', 'Market Street', 'Pioneer Square Retail'],
            'Hospitality': ['Grand Vista Hotel', 'Sovereign Lodge', 'Cascade Inn', 'Pacific Resort', 'The Canopy'],
            'Mixed Use': ['The Exchange', 'Canal Crossing', 'South Lake Hub', 'Westlake Commons', 'Harbor Steps'],
            'Government': ['City Hall', 'Municipal Center', 'Federal Building', 'County Courthouse', 'Public Safety Building']
        }
        building_names = []
        for i, t in enumerate(b_types):
            pref = np.random.choice(name_prefixes[t])
            building_names.append(f"{pref} {np.random.randint(10, 99)} ({building_ids[i]})")
            
        years_built = np.random.randint(1920, 2024, size=num_records).tolist()
        
        floor_areas = []
        for t in b_types:
            if t in ['Office', 'Mixed Use', 'Healthcare']:
                area = np.random.randint(50000, 750000)
            elif t in ['Hospitality', 'Government', 'Educational']:
                area = np.random.randint(30000, 350000)
            else:
                area = np.random.randint(15000, 200000)
            floor_areas.append(area)
            
        num_floors = []
        for i, t in enumerate(b_types):
            area = floor_areas[i]
            if t in ['Office', 'Mixed Use'] and area > 300000:
                floors = np.random.randint(15, 60)
            elif t in ['Residential', 'Hospitality'] and area > 100000:
                floors = np.random.randint(5, 25)
            else:
                floors = np.random.randint(1, 10)
            num_floors.append(floors)
            
        occupancy_rates = np.round(np.random.beta(8, 2, size=num_records) * 0.4 + 0.58, 2).tolist()
        data_source_flag = "Synthetic Baseline"

    # Now synthesize design characteristics to correlate with Energy Star Score / EUI
    materials = ['Concrete', 'Steel', 'Timber', 'Brick', 'Composite', 'Glass-heavy facade']
    facade_types = ['Curtain Wall', 'Window Wall', 'Masonry', 'Rain Screen', 'Insulated Panels']
    
    b_materials = []
    b_facades = []
    window_to_wall_ratios = []
    insulation_levels = []
    b_hvac = []
    b_lighting = []
    renewable_energy_flags = []
    solar_capacities = []
    green_roof_flags = []
    leed_levels = []
    
    for i in range(num_records):
        floors = num_floors[i]
        year = years_built[i]
        t = b_types[i]
        
        # If in hybrid mode, use Energy Star score as proxy for efficiency level. Otherwise, random.
        if use_hybrid:
            score = real_energy_star[i]
        else:
            score = np.random.randint(10, 99)
            
        # Determine materials & facades
        if floors > 15:
            mat = np.random.choice(['Steel', 'Concrete', 'Glass-heavy facade'], p=[0.4, 0.4, 0.2])
        elif year > 2010 and floors <= 4:
            mat = np.random.choice(['Timber', 'Composite', 'Concrete'], p=[0.5, 0.3, 0.2])
        else:
            mat = np.random.choice(materials)
        b_materials.append(mat)
        
        if mat == 'Glass-heavy facade':
            fac = 'Curtain Wall'
            wwr = np.round(np.random.uniform(0.65, 0.85), 2)
        elif mat == 'Brick':
            fac = 'Masonry'
            wwr = np.round(np.random.uniform(0.15, 0.35), 2)
        else:
            fac = np.random.choice(facade_types)
            wwr = np.round(np.random.uniform(0.25, 0.55), 2)
            
        b_facades.append(fac)
        window_to_wall_ratios.append(wwr)
        
        # Insulation Level (correlated with score and age)
        if score >= 75:
            ins = np.random.choice(['Medium', 'High'], p=[0.2, 0.8])
        elif score <= 40 or year < 1980:
            ins = np.random.choice(['Low', 'Medium'], p=[0.8, 0.2])
        else:
            ins = np.random.choice(['Low', 'Medium', 'High'], p=[0.2, 0.6, 0.2])
        insulation_levels.append(ins)
        
        # HVAC system type
        if score >= 80:
            hvac = np.random.choice(['High Efficiency HVAC', 'Heat Pump', 'District Heating'], p=[0.3, 0.5, 0.2])
        elif score <= 35:
            hvac = np.random.choice(['Standard HVAC', 'Electric Resistance'], p=[0.7, 0.3])
        else:
            hvac = np.random.choice(['Standard HVAC', 'High Efficiency HVAC', 'Heat Pump', 'District Heating', 'Electric Resistance', 'Mixed System'])
        b_hvac.append(hvac)
        
        # Lighting
        if score >= 70:
            lighting = np.random.choice(['LED', 'Smart LED'], p=[0.4, 0.6])
        elif score <= 30:
            lighting = np.random.choice(['Fluorescent', 'Incandescent'], p=[0.7, 0.3])
        else:
            lighting = np.random.choice(['LED', 'Fluorescent'], p=[0.7, 0.3])
        b_lighting.append(lighting)
        
        # Renewables & Green Roofs
        prob_renew = 0.05
        if score >= 80 or year > 2012:
            prob_renew = 0.35
        has_renew = np.random.choice([True, False], p=[prob_renew, 1 - prob_renew])
        renewable_energy_flags.append(has_renew)
        
        if has_renew:
            solar_capacities.append(np.round(np.random.uniform(10.0, 450.0), 1))
        else:
            solar_capacities.append(0.0)
            
        prob_green = 0.02
        if score >= 85 and t in ['Office', 'Mixed Use', 'Educational']:
            prob_green = 0.20
        green_roof_flags.append(np.random.choice([True, False], p=[prob_green, 1 - prob_green]))
        
        # LEED Certification
        if score >= 85:
            leed = np.random.choice(['Silver', 'Gold', 'Platinum'], p=[0.25, 0.50, 0.25])
        elif score >= 60:
            leed = np.random.choice(['None', 'Certified', 'Silver', 'Gold'], p=[0.40, 0.30, 0.20, 0.10])
        else:
            leed = 'None'
        leed_levels.append(leed)

    df_design = pd.DataFrame({
        'building_id': building_ids,
        'building_name': building_names,
        'building_type': b_types,
        'location_city': b_cities,
        'climate_zone': b_climates,
        'year_built': years_built,
        'floor_area_sqft': floor_areas,
        'number_of_floors': num_floors,
        'occupancy_type': b_types,
        'average_occupancy_rate': occupancy_rates,
        'primary_material': b_materials,
        'facade_type': b_facades,
        'window_to_wall_ratio': window_to_wall_ratios,
        'insulation_level': insulation_levels,
        'hvac_system_type': b_hvac,
        'lighting_system_type': b_lighting,
        'renewable_energy_flag': renewable_energy_flags,
        'solar_panel_capacity_kw': solar_capacities,
        'green_roof_flag': green_roof_flags,
        'leed_certification_level': leed_levels,
        'data_source': [data_source_flag] * num_records
    })

    # 2. Construction Costs Dataset
    cost_ids = [f"COST_{i:04d}" for i in range(1, num_records + 1)]
    base_cost_map = {
        'Healthcare': 450, 'Office': 280, 'Hospitality': 340, 'Government': 320,
        'Mixed Use': 290, 'Educational': 260, 'Residential': 220, 'Retail': 180
    }
    
    estimated_costs = []
    actual_costs = []
    overruns = []
    overrun_pcts = []
    delay_days_list = []
    delay_reasons = []
    
    contractors = ["Apex Builders", "Emerald City Construction", "Summit Contractors", "Cascade Building Group", "Pacific Structures"]
    b_contractors = np.random.choice(contractors, size=num_records)
    
    contractor_profiles = {
        "Apex Builders": (0.35, 1.0), "Emerald City Construction": (0.45, 1.2),
        "Summit Contractors": (0.50, 1.3), "Cascade Building Group": (0.30, 0.9),
        "Pacific Structures": (0.40, 1.1)
    }
    
    start_dates = []
    for y in years_built:
        start_year = max(2013, y - 2)
        start_month = np.random.randint(1, 13)
        start_day = np.random.randint(1, 28)
        start_dates.append(datetime.date(start_year, start_month, start_day))
        
    planned_durations = []
    for area in floor_areas:
        dur = int(180 + (area / 1000) * 0.8 + np.random.randint(-30, 30))
        planned_durations.append(max(180, dur))
        
    for i in range(num_records):
        t = b_types[i]
        area = floor_areas[i]
        material = b_materials[i]
        leed = leed_levels[i]
        hvac = b_hvac[i]
        solar_cap = solar_capacities[i]
        has_green = green_roof_flags[i]
        contractor = b_contractors[i]
        
        # Calculate base estimated cost
        cost_sqft = base_cost_map[t]
        
        # Adjustments
        if material == 'Glass-heavy facade':
            cost_sqft *= 1.12
        elif material == 'Timber':
            cost_sqft *= 1.05
            
        if leed == 'Platinum':
            cost_sqft *= 1.08
        elif leed == 'Gold':
            cost_sqft *= 1.05
        elif leed == 'Silver':
            cost_sqft *= 1.03
            
        if hvac in ['Heat Pump', 'High Efficiency HVAC']:
            cost_sqft *= 1.02
            
        est_cost = area * cost_sqft
        
        if solar_cap > 0:
            est_cost += solar_cap * 2200
            
        if has_green:
            roof_area = area / num_floors[i]
            est_cost += roof_area * 25
            
        est_cost = np.round(est_cost * np.random.uniform(0.95, 1.05), -2)
        estimated_costs.append(est_cost)
        
        # Overruns & Delays
        prob_delay, severity = contractor_profiles[contractor]
        is_delayed = np.random.choice([True, False], p=[prob_delay, 1 - prob_delay])
        
        if is_delayed:
            reason = np.random.choice(
                ['Weather', 'Material Shortage', 'Labor Shortage', 'Permit Delay', 'Design Change', 'Contractor Delay', 'Supply Chain Issue'],
                p=[0.15, 0.20, 0.20, 0.10, 0.15, 0.10, 0.10]
            )
            reason_severity = {
                'Weather': np.random.randint(5, 45),
                'Material Shortage': np.random.randint(30, 150),
                'Labor Shortage': np.random.randint(20, 120),
                'Permit Delay': np.random.randint(15, 90),
                'Design Change': np.random.randint(30, 180),
                'Contractor Delay': np.random.randint(15, 60),
                'Supply Chain Issue': np.random.randint(30, 140)
            }
            days = int(reason_severity[reason] * severity)
            delay_days_list.append(days)
            delay_reasons.append(reason)
            
            reason_cost_factor = {
                'Weather': 0.0008, 'Material Shortage': 0.0015, 'Labor Shortage': 0.0012,
                'Permit Delay': 0.0006, 'Design Change': 0.0022, 'Contractor Delay': 0.0010,
                'Supply Chain Issue': 0.0014
            }
            overrun_pct = (days * reason_cost_factor[reason]) + np.random.uniform(-0.02, 0.04)
            overrun_pct = max(0.01, np.round(overrun_pct, 4))
        else:
            delay_days_list.append(0)
            delay_reasons.append('None')
            overrun_pct = np.round(np.random.uniform(-0.01, 0.015), 4)
            overrun_pct = max(0.0, overrun_pct)
            
        overrun_pcts.append(overrun_pct)
        overrun_amt = np.round(est_cost * overrun_pct, -2)
        overruns.append(overrun_amt)
        actual_costs.append(est_cost + overrun_amt)

    df_cost = pd.DataFrame({
        'cost_id': cost_ids,
        'building_id': building_ids,
        'estimated_construction_cost': estimated_costs,
        'actual_construction_cost': actual_costs,
        'cost_overrun_amount': overruns,
        'cost_overrun_percentage': overrun_pcts,
        'contractor_name': b_contractors,
        'project_start_date': start_dates,
        'planned_duration_days': planned_durations,
        'delay_days': delay_days_list,
        'delay_reason': delay_reasons
    })
    
    df_cost['project_start_date'] = pd.to_datetime(df_cost['project_start_date'])
    df_cost['planned_completion_date'] = df_cost['project_start_date'] + pd.to_timedelta(df_cost['planned_duration_days'], unit='D')
    df_cost['actual_duration_days'] = df_cost['planned_duration_days'] + df_cost['delay_days']
    df_cost['actual_completion_date'] = df_cost['project_start_date'] + pd.to_timedelta(df_cost['actual_duration_days'], unit='D')
    
    df_cost['material_cost'] = np.round(df_cost['actual_construction_cost'] * np.random.uniform(0.42, 0.48, size=num_records), -2)
    df_cost['labor_cost'] = np.round(df_cost['actual_construction_cost'] * np.random.uniform(0.32, 0.38, size=num_records), -2)
    df_cost['equipment_cost'] = np.round(df_cost['actual_construction_cost'] * np.random.uniform(0.08, 0.12, size=num_records), -2)
    df_cost['design_consulting_cost'] = np.round(df_cost['actual_construction_cost'] * np.random.uniform(0.05, 0.07, size=num_records), -2)
    df_cost['permit_cost'] = df_cost['actual_construction_cost'] - (df_cost['material_cost'] + df_cost['labor_cost'] + df_cost['equipment_cost'] + df_cost['design_consulting_cost'])

    # 3. Building Operations Dataset
    op_ids = [f"OP_{i:04d}" for i in range(1, num_records + 1)]
    
    if use_hybrid:
        # Map operations metrics directly from sampled benchmarking data
        euis = real_euis
        annual_energy_use = real_aeu
        carbon_emissions = real_emissions
        energy_star_scores = real_energy_star
        emissions_intensities = real_emissions_intensity
    else:
        # Pure synthetic calculations
        base_eui_map = {
            'Healthcare': 210, 'Hospitality': 110, 'Government': 90, 'Office': 75,
            'Mixed Use': 80, 'Educational': 65, 'Retail': 70, 'Residential': 60
        }
        euis = []
        for i in range(num_records):
            t = b_types[i]
            year = years_built[i]
            insul = insulation_levels[i]
            hvac = b_hvac[i]
            lighting = b_lighting[i]
            wwr = window_to_wall_ratios[i]
            occ = occupancy_rates[i]
            
            eui = base_eui_map[t]
            if insul == 'Low': eui *= 1.25
            elif insul == 'High': eui *= 0.80
            
            if hvac == 'Heat Pump': eui *= 0.70
            elif hvac == 'High Efficiency HVAC': eui *= 0.82
            elif hvac == 'Electric Resistance': eui *= 1.25
            elif hvac == 'District Heating': eui *= 0.88
            
            if lighting == 'Smart LED': eui *= 0.90
            elif lighting == 'Incandescent': eui *= 1.15
            elif lighting == 'Fluorescent': eui *= 1.05
            
            if wwr > 0.50: eui *= (1.0 + (wwr - 0.50) * 0.4)
            elif wwr < 0.25: eui *= 0.95
            
            if year < 1980: eui *= (1.0 + (1980 - year) * 0.004)
            elif year > 2015: eui *= 0.88
            
            eui *= (0.75 + 0.25 * occ)
            eui = max(15.0, np.round(eui * np.random.uniform(0.92, 1.08), 2))
            euis.append(eui)
            
        euis = np.array(euis)
        annual_energy_use = np.round(euis * np.array(floor_areas), -1).tolist()
        
        # Calculate Energy Star Score
        energy_star_scores = []
        df_temp = pd.DataFrame({'building_type': b_types, 'eui': euis})
        for i in range(num_records):
            t = b_types[i]
            eui = euis[i]
            type_euis = df_temp[df_temp['building_type'] == t]['eui']
            pct = (type_euis > eui).sum() / len(type_euis)
            score = int(pct * 100)
            leed = leed_levels[i]
            if leed == 'Platinum': score += 15
            elif leed == 'Gold': score += 10
            elif leed == 'Silver': score += 5
            score = max(1, min(100, score))
            energy_star_scores.append(score)
            
        # Carbon emissions synthetic
        carbon_emissions = []
        for i in range(num_records):
            aeu = annual_energy_use[i]
            hvac = b_hvac[i]
            solar_cap = solar_capacities[i]
            
            factor = 0.000062
            if hvac == 'Heat Pump': factor = 0.000038
            elif hvac == 'District Heating': factor = 0.000048
            elif hvac == 'Electric Resistance': factor = 0.000072
            
            emissions = aeu * factor
            if renewable_energy_flags[i]:
                emissions *= max(0.50, 1 - (solar_cap / 500))
            carbon_emissions.append(np.round(emissions, 2))
        carbon_emissions = np.array(carbon_emissions)
        emissions_intensities = np.round(carbon_emissions / np.array(floor_areas) * 1000, 4).tolist()

    # Calculate operational utility costs based on energy use & sizes
    electricity_costs = []
    water_costs = []
    maintenance_costs = []
    
    for i in range(num_records):
        aeu = annual_energy_use[i]
        solar_cap = solar_capacities[i]
        t = b_types[i]
        area = floor_areas[i]
        year = years_built[i]
        hvac = b_hvac[i]
        occ = occupancy_rates[i]
        
        base_elec = aeu * 0.035
        solar_savings = solar_cap * 150
        elec_cost = max(base_elec * 0.4, base_elec - solar_savings)
        electricity_costs.append(np.round(elec_cost, -2))
        
        water_use_sqft_map = {
            'Healthcare': 50, 'Hospitality': 42, 'Residential': 36, 'Office': 16,
            'Mixed Use': 22, 'Educational': 14, 'Government': 18, 'Retail': 12
        }
        water_gal = area * water_use_sqft_map[t] * occ * np.random.uniform(0.90, 1.10)
        water_cost = water_gal * 0.015
        water_costs.append(np.round(water_cost, -2))
        
        base_maint = area * 1.20
        if year < 1980: base_maint *= 1.35
        elif year < 2000: base_maint *= 1.15
        if hvac == 'Standard HVAC' and year < 1995: base_maint *= 1.10
        maintenance_costs.append(np.round(base_maint * np.random.uniform(0.92, 1.08), -2))

    electricity_costs = np.array(electricity_costs)
    water_costs = np.array(water_costs)
    maintenance_costs = np.array(maintenance_costs)
    
    annual_operating_costs = electricity_costs + water_costs + maintenance_costs
    operating_costs_per_sqft = np.round(annual_operating_costs / np.array(floor_areas), 2)
    peak_demands = np.round((np.array(floor_areas) / 1000) * np.random.uniform(1.2, 3.8) * (1.1 - 0.2 * (np.array(energy_star_scores) / 100.0)), 1)
    water_gallons = np.round(water_costs / 0.015, -1)
    
    rating_list = []
    for score in energy_star_scores:
        if score >= 80: rating_list.append('Excellent')
        elif score >= 60: rating_list.append('Good')
        elif score >= 40: rating_list.append('Fair')
        else: rating_list.append('Poor')

    df_operations = pd.DataFrame({
        'operation_id': op_ids,
        'building_id': building_ids,
        'reporting_year': [2024] * num_records,
        'annual_energy_use_kbtu': annual_energy_use,
        'energy_use_intensity_kbtu_sqft': euis,
        'annual_electricity_cost': electricity_costs,
        'annual_water_cost': water_costs,
        'annual_maintenance_cost': maintenance_costs,
        'annual_operating_cost': annual_operating_costs,
        'carbon_emissions_metric_tons': carbon_emissions,
        'energy_star_score': energy_star_scores,
        'peak_demand_kw': peak_demands,
        'water_use_gallons': water_gallons,
        'operating_cost_per_sqft': operating_costs_per_sqft,
        'emissions_intensity': emissions_intensities,
        'energy_efficiency_rating': rating_list
    })

    # 4. Retrofit Recommendations Dataset
    rec_ids = [f"REC_{i:04d}" for i in range(1, num_records + 1)]
    recommended_actions = []
    estimated_retrofit_costs = []
    estimated_annual_savings = []
    estimated_emissions_reduction_pcts = []
    complexities = []
    
    for i in range(num_records):
        hvac = b_hvac[i]
        insul = insulation_levels[i]
        lighting = b_lighting[i]
        solar_cap = solar_capacities[i]
        score = energy_star_scores[i]
        area = floor_areas[i]
        elec_cost = electricity_costs[i]
        maint_cost = maintenance_costs[i]
        water_cost = water_costs[i]
        water_gal = water_gallons[i]
        year = years_built[i]
        
        # Decide action logically
        if hvac in ['Standard HVAC', 'Electric Resistance'] and score < 50:
            action = np.random.choice(['HVAC Upgrade', 'Deep Energy Retrofit'], p=[0.70, 0.30])
        elif insul == 'Low' and score < 60:
            action = np.random.choice(['Insulation Improvement', 'Window Replacement'], p=[0.60, 0.40])
        elif lighting in ['Incandescent', 'Fluorescent']:
            action = 'LED Lighting Retrofit'
        elif solar_cap == 0 and area > 120000:
            action = 'Solar Panel Installation'
        elif water_gal > 5000000 and score < 60:
            action = 'Water Efficiency Upgrade'
        elif score < 40 and (2024 - year) > 40:
            action = 'Deep Energy Retrofit'
        else:
            action = np.random.choice(['Building Automation System', 'LED Lighting Retrofit', 'Solar Panel Installation', 'Water Efficiency Upgrade'])
            
        recommended_actions.append(action)
        
        # Cost and savings estimates
        if action == 'HVAC Upgrade':
            cost = 15000 + area * 1.45
            savings = 0.22 * elec_cost
            reduction = np.random.uniform(18, 26)
            complexity = 'Medium'
        elif action == 'Insulation Improvement':
            cost = 8000 + area * 0.70
            savings = 0.16 * (elec_cost * 0.7)
            reduction = np.random.uniform(12, 18)
            complexity = 'Medium'
        elif action == 'Window Replacement':
            cost = 12000 + area * 1.85
            savings = 0.12 * elec_cost
            reduction = np.random.uniform(9, 14)
            complexity = 'Medium'
        elif action == 'Solar Panel Installation':
            kw = min(250.0, np.round(area / 1500, 1))
            kw = max(20.0, kw)
            cost = 25000 + kw * 2000
            savings = kw * 145
            reduction = np.random.uniform(15, 28)
            complexity = 'Medium'
        elif action == 'LED Lighting Retrofit':
            cost = 3000 + area * 0.28
            savings = 0.18 * elec_cost
            reduction = np.random.uniform(8, 12)
            complexity = 'Low'
        elif action == 'Building Automation System':
            cost = 9000 + area * 0.35
            savings = 0.15 * elec_cost + 0.05 * maint_cost
            reduction = np.random.uniform(10, 16)
            complexity = 'Medium'
        elif action == 'Water Efficiency Upgrade':
            cost = 4000 + area * 0.18
            savings = 0.28 * water_cost
            reduction = np.random.uniform(2, 5)
            complexity = 'Low'
        else: # Deep Energy Retrofit
            cost = 60000 + area * 4.20
            savings = 0.42 * elec_cost + 0.15 * maint_cost
            reduction = np.random.uniform(32, 48)
            complexity = 'High'
            
        cost = np.round(cost, -2)
        savings = np.round(savings, -2)
        if savings <= 0:
            savings = np.round(cost * 0.08, -2)
            
        estimated_retrofit_costs.append(cost)
        estimated_annual_savings.append(savings)
        estimated_emissions_reduction_pcts.append(np.round(reduction, 2))
        complexities.append(complexity)
        
    estimated_retrofit_costs = np.array(estimated_retrofit_costs)
    estimated_annual_savings = np.array(estimated_annual_savings)
    paybacks = np.round(estimated_retrofit_costs / estimated_annual_savings, 2)
    
    priorities = []
    for i in range(num_records):
        pb = paybacks[i]
        score = energy_star_scores[i]
        
        if pb < 4.0 or (pb < 6.0 and score < 40):
            priorities.append('Critical')
        elif pb < 7.0 or (pb < 9.0 and score < 60):
            priorities.append('High')
        elif pb < 12.0:
            priorities.append('Medium')
        else:
            priorities.append('Low')

    df_retrofit = pd.DataFrame({
        'recommendation_id': rec_ids,
        'building_id': building_ids,
        'recommended_action': recommended_actions,
        'estimated_retrofit_cost': estimated_retrofit_costs,
        'estimated_annual_savings': estimated_annual_savings,
        'payback_period_years': paybacks,
        'estimated_emissions_reduction_percent': estimated_emissions_reduction_pcts,
        'retrofit_priority': priorities,
        'implementation_complexity': complexities
    })

    # Save directories check
    os.makedirs('data/synthetic', exist_ok=True)
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    df_design.to_csv('data/synthetic/building_design.csv', index=False)
    df_cost.to_csv('data/synthetic/construction_costs.csv', index=False)
    df_operations.to_csv('data/synthetic/building_operations.csv', index=False)
    df_retrofit.to_csv('data/synthetic/retrofit_recommendations.csv', index=False)
    
    print("Synthetic datasets successfully created in data/synthetic/")
    print(f"Design shape: {df_design.shape}, Cost shape: {df_cost.shape}, Operations shape: {df_operations.shape}, Retrofit shape: {df_retrofit.shape}")

if __name__ == '__main__':
    generate_data(2200)
