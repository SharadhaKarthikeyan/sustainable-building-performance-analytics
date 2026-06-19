import json
import os

def create_notebooks():
    print("Programmatically creating Jupyter Notebooks...")
    os.makedirs('notebooks', exist_ok=True)
    
    # 1. 01_data_loading_and_cleaning.ipynb
    nb1 = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Notebook 01: Data Loading & Cleaning\n",
                    "**Sustainable Building Performance Analytics Dashboard**\n\n",
                    "## Purpose\n",
                    "This notebook loads the raw benchmarking and synthetic architectural datasets, standardizes column names, converts datetimes, cleans missing value bands (like LEED and cost overruns), and saves the clean tables to the processed directory."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Run clean data script\n",
                    "%run ../src/clean_data.py"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Inspecting Cleaned Datasets"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "design = pd.read_csv('../data/processed/building_design_clean.csv')\n",
                    "costs = pd.read_csv('../data/processed/construction_costs_clean.csv')\n",
                    "ops = pd.read_csv('../data/processed/building_operations_clean.csv')\n",
                    "print(f\"Design columns: {design.columns.tolist()[:5]}\")\n",
                    "print(f\"Costs columns: {costs.columns.tolist()[:5]}\")\n",
                    "print(f\"Operations columns: {ops.columns.tolist()[:5]}\")"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    # 2. 02_exploratory_data_analysis.ipynb
    nb2 = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Notebook 02: Exploratory Data Analysis\n",
                    "**Sustainable Building Performance Analytics Dashboard**\n\n",
                    "## Purpose\n",
                    "This notebook runs exploratory visualizations on our cleaned data, looking at variables like EUI by building type, cost per square foot, delays by contractor, carbon emissions by primary material, and sustainability features like LEED levels and HVAC systems."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Run EDA visual script\n",
                    "%run ../src/eda.py"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Key Descriptive Metrics"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "df = pd.read_csv('../dashboard/building_performance_dashboard_data.csv')\n",
                    "df.groupby('building_type')[['energy_use_intensity_kbtu_sqft', 'cost_per_sqft', 'operating_cost_per_sqft']].mean()"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    # 3. 03_building_performance_risk_analysis.ipynb
    nb3 = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Notebook 03: Building Performance Risk Analysis\n",
                    "**Sustainable Building Performance Analytics Dashboard**\n\n",
                    "## Purpose\n",
                    "This notebook applies the master's-level **12-factor Risk Scoring Model** to rank buildings on a scale of 0 to 12. It covers operational inefficiency, poor insulation, cost overruns, delay risk, and lack of renewable integrations, sorting structures into Risk Categories (Low, Medium, High, Critical)."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "df = pd.read_csv('../data/processed/building_design_clean.csv')\n",
                    "print(\"Risk Category Distribution:\")\n",
                    "print(df['building_performance_risk_category'].value_counts())\n",
                    "print(\"\\nAverage Risk Score by Building Type:\")\n",
                    "print(df.groupby('building_type')['building_performance_risk_score'].mean())"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    # 4. 04_dashboard_data_preparation.ipynb
    nb4 = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Notebook 04: Dashboard Data Preparation\n",
                    "**Sustainable Building Performance Analytics Dashboard**\n\n",
                    "## Purpose\n",
                    "This notebook merges the cleaned and risk-scored tables into a single unified dashboard flat file: `dashboard/building_performance_dashboard_data.csv` for direct import into Power BI and Tableau."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Run dashboard prepare script\n",
                    "%run ../src/prepare_dashboard_data.py"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Verification of Dashboard Columns"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "df_dash = pd.read_csv('../dashboard/building_performance_dashboard_data.csv')\n",
                    "print(f\"Dashboard Shape: {df_dash.shape}\")\n",
                    "print(f\"Number of columns: {len(df_dash.columns)}\")\n",
                    "assert len(df_dash.columns) == 52, \"Warning: Incorrect column count!\""
                ]
            }
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    # Write to files
    with open('notebooks/01_data_loading_and_cleaning.ipynb', 'w') as f:
        json.dump(nb1, f, indent=1)
    with open('notebooks/02_exploratory_data_analysis.ipynb', 'w') as f:
        json.dump(nb2, f, indent=1)
    with open('notebooks/03_building_performance_risk_analysis.ipynb', 'w') as f:
        json.dump(nb3, f, indent=1)
    with open('notebooks/04_dashboard_data_preparation.ipynb', 'w') as f:
        json.dump(nb4, f, indent=1)
        
    print("Jupyter Notebooks created successfully in notebooks/")

if __name__ == '__main__':
    create_notebooks()
