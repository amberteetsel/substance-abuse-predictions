import pandas as pd

# define important cols
keep_cols = ['buyer_state', 'drug_name', 'transaction_date', 'calc_base_wt_in_gm']

chunks = pd.read_csv(
    "../../data/DEA_2.csv.gz", 
    usecols=keep_cols, 
    chunksize=1000000, 
    compression='gzip',
    low_memory=False
)

aggregated_results = []

print("Starting extraction...")
for i, chunk in enumerate(chunks):
    # 1. CLEAN DRUG NAMES FIRST (Strip spaces and uppercase)
    chunk['drug_name'] = chunk['drug_name'].astype(str).str.strip().str.upper()
    
    # 2. UPDATED MASK
    targets = ['OXYCODONE', 'HYDROCODONE', 'FENTANYL', 'FENTANYL BASE']
    mask = chunk['drug_name'].isin(targets)
    small_chunk = chunk[mask].copy()
    
    if not small_chunk.empty:
        # Normalize name to remove "Base"
        small_chunk['drug_name'] = small_chunk['drug_name'].replace({'FENTANYL BASE': 'FENTANYL'})
        
        # Extract year safely (if date is MMDDYYYY)
        # Using string slicing is MUCH faster and less crash-prone than pd.to_datetime
        small_chunk['year'] = small_chunk['transaction_date'].astype(str).str[-4:].astype(int)
        
        # Aggregate
        chunk_summed = small_chunk.groupby(['buyer_state', 'year', 'drug_name'])['calc_base_wt_in_gm'].sum().reset_index()
        aggregated_results.append(chunk_summed)
    
    if i % 10 == 0:
        print(f"Chunk {i}: Found {len(small_chunk)} relevant rows.")

# Check before concat
if not aggregated_results:
    print("❌ ERROR: No data found! Check drug names in raw file.")
else:
    df_mini = pd.concat(aggregated_results)
    df_final_sum = df_mini.groupby(['buyer_state', 'year', 'drug_name'])['calc_base_wt_in_gm'].sum().reset_index()
    print(f"✅ SUCCESS: Found {len(df_final_sum)} state/year/drug combinations.")
    df_final_sum.to_csv('../../data/dea_summary_pre_aggregated.csv', index=False)

df = pd.read_csv('../../data/dea_summary_pre_aggregated.csv')

# Clean, get to format that can merge with NCHS

print("Pivoting drug columns...")
df_pivot = df.pivot_table(
    index=['buyer_state', 'year'], 
    columns='drug_name', 
    values='calc_base_wt_in_gm'
).reset_index()

# Clean col names
df_pivot.columns.name = None 
df_pivot = df_pivot.rename(columns={
    'buyer_state': 'state',
    'HYDROCODONE': 'hydro_gms',
    'OXYCODONE': 'oxy_gms',
    'FENTANYL': 'fent_gms'
})

# Fill NAs and save
df_pivot = df_pivot.fillna(0)
df_pivot.to_csv('../../data/dea_final.csv', index=False)
print("Transformation complete! No more crashes.")

import numpy as np
# Data from 2000, 2005
# state mapping dict
state_map = {
    'ALABAMA': 'AL', 'ALASKA': 'AK', 'ARIZONA': 'AZ', 'ARKANSAS': 'AR', 'CALIFORNIA': 'CA',
    'COLORADO': 'CO', 'CONNECTICUT': 'CT', 'DELAWARE': 'DE', 'FLORIDA': 'FL', 'GEORGIA': 'GA',
    'HAWAII': 'HI', 'IDAHO': 'ID', 'ILLINOIS': 'IL', 'INDIANA': 'IN', 'IOWA': 'IA',
    'KANSAS': 'KS', 'KENTUCKY': 'KY', 'LOUISIANA': 'LA', 'MAINE': 'ME', 'MARYLAND': 'MD',
    'MASSACHUSETTS': 'MA', 'MICHIGAN': 'MI', 'MINNESOTA': 'MN', 'MISSISSIPPI': 'MS', 'MISSOURI': 'MO',
    'MONTANA': 'MT', 'NEBRASKA': 'NE', 'NEVADA': 'NV', 'NEW HAMPSHIRE': 'NH', 'NEW JERSEY': 'NJ',
    'NEW MEXICO': 'NM', 'NEW YORK': 'NY', 'NORTH CAROLINA': 'NC', 'NORTH DAKOTA': 'ND', 'OHIO': 'OH',
    'OKLAHOMA': 'OK', 'OREGON': 'OR', 'PENNSYLVANIA': 'PA', 'RHODE ISLAND': 'RI', 'SOUTH CAROLINA': 'SC',
    'SOUTH DAKOTA': 'SD', 'TENNESSEE': 'TN', 'TEXAS': 'TX', 'UTAH': 'UT', 'VERMONT': 'VT',
    'VIRGINIA': 'VA', 'WASHINGTON': 'WA', 'WEST VIRGINIA': 'WV', 'WISCONSIN': 'WI', 'WYOMING': 'WY',
    'DISTRICT OF COLUMBIA': 'DC'
}

# load and clean 2000, 2005 data
df_manual = pd.read_excel("../../data/DEA_2000_2005.xlsx")
# df_manual = df_manual.rename(columns={"Year":'year', "State":'state'})
df_manual['state'] = df_manual['state'].str.upper().str.strip().map(state_map)
df_manual = df_manual[['state', 'year', 'hydro_gms', 'oxy_gms', 'fent_gms']]

# 2006-16
df_2006_16 = pd.read_csv('../../data/dea_final.csv')
df_2006_16 = df_2006_16.loc[df_2006_16.state!="DC"].reset_index(drop=True)

# Combine
dea_master = pd.concat([df_manual, df_2006_16], ignore_index=True)

# initialize grid with all state-year combinations
states = dea_master['state'].unique()
years = range(2000, 2017)
full_grid = pd.MultiIndex.from_product([states, years], names=['state', 'year']).to_frame(index=False)

# add data
dea_full = pd.merge(full_grid, dea_master, on=['state', 'year'], how='left')

# sort and fill drug gms, interpolate missing years
drug_cols = ['hydro_gms', 'oxy_gms', 'fent_gms']
dea_full[drug_cols] = dea_full.groupby('state')[drug_cols].transform(lambda x: x.interpolate(method='linear'))

# Backfill Fentanyl for 2000 (since your data starts in 2001)
dea_full['fent_gms'] = dea_full.groupby('state')['fent_gms'].transform(lambda x: x.bfill())

# Export the final file
dea_full.to_csv('../../data/dea_full_interpolated.csv', index=False)