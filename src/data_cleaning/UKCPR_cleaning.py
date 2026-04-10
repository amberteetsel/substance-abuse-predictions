import pandas as pd

df = pd.read_excel("../../data/Nat_Welfare_Data_1980_2024.xlsx", sheet_name="Data")

df.to_csv("../../data/ukcpr_raw.csv", index=False)

# filter for 1999-2016
df = df[df["year"].between(1999, 2016)].reset_index(drop=True)

# Reduce to key features
cols_to_keep = [
    'state_name', 'year',                          # Keys
    'Population',                                  # Calculate Rates
    'Unemployment rate', 'Poverty Rate',                # Core Economics
    'Food Stamp/SNAP Recipients', 'Gross State Product',        # Financial Stress
    'Medicaid beneficiaries',                      # Healthcare Access
    'Governor is Democrat (1=Yes)',                # Political Context
    'State Minimum Wage'                           # Economic Policy
]

df = df[cols_to_keep].copy()

col_names = ["state_abbr", "year", 
             "population",
             "unempl_rate", "poverty_rate",
             "snap_recipients", "gsp",
            "medicaid_beneficiaries",
            "gov_dem",
            "min_wage"]

df.columns = col_names

# Calculate rates and drop raw counts
df['snap_rate'] = df['snap_recipients'] / df['population']
df['medicaid_rate'] = df['medicaid_beneficiaries'] / df['population']

df = df.drop(columns=['snap_recipients', 'medicaid_beneficiaries', 'population'])

# Add full state names
state_mapping = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 
    'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
}

df['state_name'] = df['state_abbr'].map(state_mapping)

# Define the logical order
ordered_cols = [
    # 1. Identifiers
    'state_name', 'state_abbr', 'year', 
    
    # 2. Economic Features (Macro-level stress)
    'poverty_rate', 'unempl_rate', 'gsp', 'min_wage',
    
    # 3. Social Safety Net & Healthcare (Policy indicators)
    'snap_rate', 'medicaid_rate',
    
    # 4. Political Context
    'gov_dem'
]

# Apply the reordering
df = df[ordered_cols]

# Save cleaned data
df.to_csv("../../data/UKCPR_cleaned.csv", index=False)
