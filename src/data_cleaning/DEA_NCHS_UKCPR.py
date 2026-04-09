import pandas as pd
import numpy as np

# Load datasets
nchs = pd.read_csv('../../data/NCHS_Mortality_Clean.csv')
dea = pd.read_csv('../../data/dea_full_interpolated.csv')
ukcpr = pd.read_csv('../../data/UKCPR_cleaned.csv')

################# NCHS CLEANING #################

# Add state abbrev to NCHS
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

# Remove national data and DC from NCHS since DEA data is state-level
nchs = nchs[(nchs['state'] != 'United States')].reset_index(drop=True)
nchs = nchs[nchs['state'].str.strip().str.upper() != 'DC'].reset_index(drop=True)
# Remove 1999 from NCHS since DEA data starts in 2000
nchs = nchs[nchs['year'] >= 2000].reset_index(drop=True)
# Get rid of DC
nchs = nchs.loc[nchs['state'] != "DC"].copy().reset_index(drop=True)

################# UKCPR CLEANING #################

# Drop 1999 from UKCPR
ukcpr = ukcpr.loc[ukcpr.year >= 2000].reset_index(drop=True)

################# JOIN NCHS AND DEA #################

# Join NCHS and DEA on state and year
nchs_dea = pd.merge(
    nchs, 
    dea, 
    on=['year', 'state'], 
    how='left'
)

# Convert hydro_gms, oxy_gms to be rate per 100k population
# Convert hydro_gms, oxy_gms to be rate per 100k population
nchs_dea['hydro_gms'] = (nchs_dea['hydro_gms'] / nchs_dea['population']) * 100000 
nchs_dea['oxy_gms'] = (nchs_dea['oxy_gms'] / nchs_dea['population']) * 100000

################# JOIN UKCPR #################

# Merge with UKCPR on state and year
df_final = pd.merge(
    nchs_dea,
    ukcpr,
    left_on=['year', 'state'],
    right_on=['year', 'state_abbr'],
    how = 'left'
)

cols_to_keep = ['year', 'state', 'sex', 'age_group', 'age_group_detail', 'race', 'hydro_gms',
                'oxy_gms', 'unempl_rate','poverty_rate', 'gsp', 'min_wage',
                'snap_rate', 'medicaid_rate', 'aca_exp', 'gov_dem', 'death_rate']

df_final = df_final[cols_to_keep]

# Export final dataset
df_final.to_csv('../../data/death_rate.csv', index=False)