import os
import sqlite3
import pandas as pd

def load_data_to_sqlite():
    print("Setting up SQLite Database for portfolio queries...")
    db_path = 'data/processed/building_performance.db'
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read and execute schema definition
    schema_path = 'sql/create_tables.sql'
    if not os.path.exists(schema_path):
        print(f"Error: {schema_path} not found.")
        return
        
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
        
    # Split queries by semicolon to execute one by one
    queries = schema_sql.split(';')
    for q in queries:
        q_strip = q.strip()
        if q_strip:
            cursor.execute(q_strip)
    print("Schema tables successfully created in SQLite.")
    
    # Load and insert data
    data_files = {
        'building_design': 'data/processed/building_design_clean.csv',
        'construction_costs': 'data/processed/construction_costs_clean.csv',
        'building_operations': 'data/processed/building_operations_clean.csv',
        'retrofit_recommendations': 'data/processed/retrofit_recommendations_clean.csv',
        'building_performance_dashboard': 'dashboard/building_performance_dashboard_data.csv'
    }
    
    for table, file_path in data_files.items():
        if not os.path.exists(file_path):
            print(f"Error: Required clean data file {file_path} not found.")
            return
            
        df = pd.read_csv(file_path)
        # Handle datetime conversion for sqlite
        if table == 'construction_costs':
            df['project_start_date'] = pd.to_datetime(df['project_start_date']).dt.strftime('%Y-%m-%d')
            df['planned_completion_date'] = pd.to_datetime(df['planned_completion_date']).dt.strftime('%Y-%m-%d')
            df['actual_completion_date'] = pd.to_datetime(df['actual_completion_date']).dt.strftime('%Y-%m-%d')
            
        df.to_sql(table, conn, if_exists='append', index=False)
        print(f"Loaded {len(df)} rows into SQLite table '{table}' from {file_path}.")
        
    conn.commit()
    conn.close()
    print(f"Database setup complete! SQLite file created at: {db_path}")

if __name__ == '__main__':
    load_data_to_sqlite()
